import distributor, database, random


#Function to choose function
def chooseFunction(n, root, cursor, dicCommission):
    switcher = {
        1: inputNewDistributor,
        2: deleteDistributor,
        3: inputSales,
    }
    choosedFunction =  switcher.get(n,wrongInput)
    return choosedFunction(root, cursor, dicCommission)

def inputNewDistributor(root, cursor, dicCommission):
    newId, newName, newParentId = None,None,None
    while True:
        while True:
            if(root == None):
                print("\n =====  Nhập thông tin nhà phân phối cao nhất [nhấn 'q' hoặc 'Q' để thoát chức năng]")
                newId = input(" >> Nhap id: ")
                if(newId == 'q' or newId == 'Q'): 
                    return
                newName = input(" >> Nhap Ho ten: ")
                newParentId = None
                root = distributor.Distributor(newId, newName, newParentId)
                newNode = distributor.Distributor(newId, newName, newParentId)
                break
            else:
                print("\n =====  Nhập thông tin nhà phân phối mới [nhấn 'q' hoặc 'Q' để thoát chức năng]")
                newId = input(" >> Nhập id nhà phân phối mới: ")
                if(newId == 'q' or newId == 'Q'): 
                    return
                newName = input(" >> Nhập Họ Tên: ")
                newParentId = input(" >> Nhập id nhà phân phối cấp trên: ")

                #add new node in tree
                
                #Check if Id is existed and ParentId is existed
                #    if Id existed or ParentId is not existed: Give notice: change information
                if root:
                    node = root.findId(newId)
                    nodeParent = root.findId(newParentId)
                if(node == None and nodeParent): 
                    #Add node
                    newNode = distributor.Distributor(newId, newName, newParentId)
                    nodeParent.addNewDistributor(newNode)
                    break
                else:
                    #Change information
                    Notification = "\n <!>=<!> "
                    if(node):
                        Notification += "Id đã tồn tại, "
                    if(nodeParent == None):
                        Notification += "Id nhà cung cấp trên không tồn tại, "
                    Notification += "Hãy nhập lại thông tin <!>=<!>"
                    print(Notification)
        #Add new row to Distributor table
        queryForInsert = "insert into NhaPhanPhoi values (?,?,?)"
        parameters = [newNode.Id, newNode.Name, newNode.ParentId]
        cursor.execute(queryForInsert, parameters)
        cursor.commit()
        print("\n === Thực hiện thành công === ")

def deleteDistributor(root, cursor, dicCommission):
    while True:
        while True:
            print("\n =====  Nhập thông tin nhà phân phối muốn xóa [nhấn 'q' hoặc 'Q' để thoát chức năng]")
            id = input(" >> Nhập id nhà phân phối muốn xóa: ")
            if(id == 'q' or id == 'Q'): 
                return
            if(root==None):
                print("\n <!>=<!> Không còn nhà phân phối nào, Mời thoát chức năng <!>=<!>")
                continue
            node = root.findId(id)
            if(node==None):
                print("\n <!>=<!> Không tồn tại id trên, Mời nhập lại <!>=<!>")
                continue
            
            # temp = node

            #Choose children node for alternative and replace, update tree 
            node = deleteNode(node, cursor)
            
            #update file sql  
            cursor.execute("truncate table NhaPhanPhoi")
            cursor.commit()
            # if temp is root:
            #     loadData()
            #     return
            root.traversalAndUpdate(cursor)

            root, dicCommission = database.loadData(cursor) # can be remove 
            print("\n === Thực hiện thành công === ")
            break
 
def deleteNode(node, cursor):
    # Case 1: ParentNode doesn't have any children
    # -> Only need delete this node         
    # Case 2: ParentNode has one child
    # -> Replace this node by its child
    # Case 3: ParentNode has two children and 
    # choosed child doesn't have enough 2 children
    # -> Replace this node by choosed child
    # Case 4: ParentNode has two children and
    # choosed child have 2 children
    # -> After replace ParentNode, we must contimue replace for Choosed Node
    
    if node is None:
        return None
    #if nodeAlter (parentNode) is leaf node    
    if(node.left == None and node.right == None):
        node.Id = None
        node = None
        return node

    #if nodeAlter has one child node
    elif(node.left and node.right == None):
        node.Id = node.left.Id 
        node.Name = node.left.Name
        node.left.ParentId = node.left.Id 
        node.left = deleteNode(node.left,cursor)
        return node
        # nodeChose = node.left
        # flag = "left" 
    elif(node.right and node.left == None):
        node.Id = node.right.Id
        node.Name = node.right.Name
        node.right.ParentId = node.right.Id
        node.right = deleteNode(node.right,cursor)
        return node
        # nodeChose = node.right
        # flag = "right" 
    else:

        # cnt = number of sale table in database - 1 (1 for Distributor Table)
        cursor.execute("select count(TABLE_NAME) from INFORMATION_SCHEMA.TABLES")
        cnt = cursor.fetchone()[0]
        if cnt>1:
            #find information of nodeLeft and node Right 
            commissionLeft,saleLeft,commissionRight,saleRight = 0,0,0,0
            for row in cursor.execute("select * from DoanhSoDot_"+str(cnt-1)+" where Id like "+node.left.Id):
                commissionLeft = row.TienHoaHong
                saleLeft = row.SoSP
            for row in cursor.execute("select * from DoanhSoDot_"+str(cnt-1)+" where Id like "+node.right.Id):
                commissionRight = row.TienHoaHong
                saleRight = row.SoSP
            #Chose the child to replace the parent node 
            if(commissionLeft>commissionRight):
                nodeChose = node.left
                flag = "left"
            elif(commissionRight>commissionLeft):
                nodeChose = node.right
                flag = "right"
            else:
                if(saleLeft>saleRight):
                    nodeChose = node.left
                    flag = "left"
                elif(saleRight>saleLeft):
                    nodeChose = node.right
                    flag = "right"
                else:
                    if(random.randint(0,1)==1):
                        nodeChose = node.left
                        flag = "left"
                    else:
                        nodeChose = node.right
                        flag = "right"
        else:
            if(random.randint(0,1)==1):
                        nodeChose = node.left
                        flag = "left"
            else:
                nodeChose = node.right
                flag = "right"

        node.Id = nodeChose.Id
        node.Name = nodeChose.Name
        nodeChose.ParentId = nodeChose.Id
        if flag == "left":
            node.right.ParentId = nodeChose.Id
        else:
            node.left.ParentId = nodeChose.Id
        nodeChose = deleteNode(nodeChose, cursor)
        return node
  
def inputSales(root, cursor, dicCommission):
    #global cnt, cursor 
    # cnt = number of sale table in database - 1 (1 for Distributor Table)
    cursor.execute("select count(TABLE_NAME) from INFORMATION_SCHEMA.TABLES")
    cnt = cursor.fetchone()[0]

    if root is None:
        print('\n <!><!> Không tồn tại nhà phân phối nào trong hệ thống <!><!>')
        return

    #dictionary to save sale of each distributor (id)
    dicSale = {}
    while True and root:
        print("\n =====  Nhập thông tin doanh thu đợt " + str(cnt) + " [nhấn 'q' hoặc 'Q' để thoát chức năng] [nhấn d||D để dừng]")
        id = input(" >> Nhập id: ")
        if id=='q' or id=='Q':
            return
        if id=='d' or id=='D':
            break
        if(root.findId(id)==None):
            print("\n <!><!> Id không tồn tại, Hãy nhập lại id <!><!>")
            continue
        sale = int(input(" >> Nhập số sản phẩm bán được: "))
        dicSale[id] = sale
        print("\n === Thực hiện thành công === ")
        text = input("\n ===== Tiếp tục [phím bất kỳ] hay dừng [d||D]: ")
        if(text == 'd' or text == 'D'):
            break
    
    #Calculate commission
    for i in dicSale:
        dicCommission[i] = calculateCommission(root,i,dicSale, dicCommission)

    #create New Sale Table
    database.createNewSaleTable(cursor, cnt)

    #insert value to sale table
    queryForInsert = "insert into DoanhSoDot_"+str(cnt)+" values (?,?,?)"
    for i in dicSale:
        parameters = [i,dicSale[i],dicCommission[i]]
        cursor.execute(queryForInsert, parameters)
        cursor.commit()
    
    cnt += 1 # increment number of sale tables

def calculateCommission(root, id, dicSale, dicCommission):
    #global commission
    if root:
        node = root.findId(id)

    #Check if New Sale Table has id
    if id in dicSale:
        dicCommission[id] = dicSale[id] / 10
    else:
        dicCommission[id] = 0

    #Check if sale of children Node is large different > 10%
    if(node.left == None and node.right == None):
        return dicCommission[id]
    elif(node.left is None and node.right):
        dicCommission[node.right.Id] = calculateCommission(node, node.right.Id,dicSale, dicCommission)
        dicCommission[id] += dicCommission[node.right.Id] / 10
        return dicCommission[id]
    elif(node.left and node.right is None):
        dicCommission[node.left.Id] = calculateCommission(node, node.left.Id,dicSale, dicCommission)
        dicCommission[id] += dicCommission[node.left.Id] / 10
        return dicCommission[id]
    else:
        dicCommission[node.right.Id] = calculateCommission(node, node.right.Id,dicSale, dicCommission)
        dicCommission[node.left.Id] = calculateCommission(node, node.left.Id,dicSale, dicCommission)
        if(dicCommission[node.right.Id] < 0.9*dicCommission[node.left.Id]):
            dicCommission[id] += dicCommission[node.right.Id] / 10
        elif(dicCommission[node.left.Id] < 0.9*dicCommission[node.right.Id]):
            dicCommission[id] += dicCommission[node.left.Id] / 10
        else:
            dicCommission[id] += dicCommission[node.right.Id] / 10
            dicCommission[id] += dicCommission[node.left.Id] / 10
        return dicCommission[id]

def wrongInput():
    print("\n <!><!> Chọn lại chức năng từ 1 đến 4 <!><!>")
