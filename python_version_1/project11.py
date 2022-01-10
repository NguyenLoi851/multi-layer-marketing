import random
import pyodbc
import time

#database
#create table for distributor in database if it was not already created
def createNewDistributorTable():
    global cursor
    cursor.execute('''
                    create table NhaPhanPhoi(
                        Id nvarchar(10) primary key,
                        Name nvarchar(50),
                        ParentId nvarchar(10),
                        TimeStartInput datetime2 generated always as row start hidden,
                        TimeEndInput datetime2 generated always as row end hidden,
                        period for system_time(TimeStartInput, TimeEndInput)
                    )
                ''')
    cursor.commit()

#database
#create new table for sale round
def createNewSaleTable():
    global cursor, cnt
    cursor.execute('''
                    create table DoanhSoDot_''' + str(cnt) +'''
                    (
                        Id nvarchar(10),
                        SoSP int,
                        TienHoaHong float,
                    )
                    ''')
    cursor.commit()

#distributor
class Distributor:
    def __init__(self,Id,Name,ParentId):
        self.Id = Id
        self.Name = Name
        self.ParentId = ParentId
        self.left = None
        self.right = None
        self.parent = None
    
    def addNewDistributor(self,node):
        #Check if Parent node has already 2 children
        if(self.left and self.right):
            if(random.randint(0,1)==1):
                self.left.addNewDistributor(node)
            else:
                self.right.addNewDistributor(node)
        #Add new node if Parent node has 0 or 1 child
        elif(self.left == None and self.right == None):
            node.ParentId = self.Id    #Change parentId of Child node if change parent
            node.parent = self 
            if(random.randint(0,1)==1):
                self.left = node
            else:
                self.right = node
        else:
            node.ParentId = self.Id    #Change parentId of Child node if change parent
            node.parent = self 
            if(self.left == None):
                self.left = node
            else:
                self.right = node

    def findId(self,Id):
        res = None
        if(self == None):
            return None
        else:
            if(self.Id == Id):
                return self
            else:
                if self.left:
                    res = self.left.findId(Id)
                if (res == None):
                    if self.right:
                        res = self.right.findId(Id)
        return res

    def traversalAndUpdate(self):
        if self == None or self.Id == None:
            return
        time.sleep(0.003)
        query = "insert into NhaPhanPhoi values (?,?,?)"
        parameters = [self.Id, self.Name, self.ParentId]
        cursor.execute(query, parameters)
        cursor.commit()
        time.sleep(0.003)
        if self.left and self.left.Id:
            self.left.traversalAndUpdate()
        if self.right and self.right.Id:
            self.right.traversalAndUpdate()

#Function to choose function
def chooseFunction(n):
    switcher = {
        1: inputNewDistributor,
        2: deleteDistributor,
        3: inputSales,
    }
    function =  switcher.get(n,wrongInput)
    return function()

def inputNewDistributor():
    global root
    newId, newName, newParentId = None,None,None
    while True:
        while True:
            if(root == None):
                print("\n =====  Nhap thong tin nha phan phoi cao nhat [nhan 'q' hoac 'Q' de thoat chuc nang]")
                newId = input(" >> Nhap id: ")
                if(newId == 'q' or newId == 'Q'): 
                    return
                newName = input(" >> Nhap Ho ten: ")
                newParentId = None
                root = Distributor(newId, newName, newParentId)
                newNode = Distributor(newId, newName, newParentId)
                break
            else:
                print("\n =====  Nhap thong tin nha phan phoi moi [nhan 'q' hoac 'Q' de thoat chuc nang]")
                newId = input(" >> Nhap id nha phan phoi moi: ")
                if(newId == 'q' or newId == 'Q'): 
                    return
                newName = input(" >> Nhap Ho Ten: ")
                newParentId = input(" >> Nhap id nha phan phoi cap tren: ")

                #add new node in tree
                
                #Check if Id is existed and ParentId is existed
                #    if Id existed or ParentId is not existed: Give notice: change information
                if root:
                    node = root.findId(newId)
                    nodeParent = root.findId(newParentId)
                if(node == None and nodeParent): 
                    #Add node
                    newNode = Distributor(newId, newName, newParentId)
                    nodeParent.addNewDistributor(newNode)
                    break
                else:
                    #Change information
                    Notification = "\n <!>=<!> "
                    if(node):
                        Notification += "Id da ton tai, "
                    if(nodeParent == None):
                        Notification += "Id nha cung cap tren khong ton tai, "
                    Notification += "Hay nhap lai thong tin <!>=<!>"
                    print(Notification)
        #Add new row to Distributor table
        queryForInsert = "insert into NhaPhanPhoi values (?,?,?)"
        parameters = [newNode.Id, newNode.Name, newNode.ParentId]
        cursor.execute(queryForInsert, parameters)
        cursor.commit()

def deleteNode(node):
    global root
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
        node.left = None
        return node
    elif(node.right and node.left == None):
        node.Id = node.right.Id
        node.Name = node.right.Name
        node.right = None
        return node
    else:

        # cnt = number of sale table in database - 1 (1 for Distributor Table)
        cursor.execute("select count(TABLE_NAME) from INFORMATION_SCHEMA.TABLES")
        cnt = cursor.fetchone()[0]

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
        
        node.Id = nodeChose.Id
        node.Name = nodeChose.Name
        nodeChose.ParentId = nodeChose.Id
        if flag == "left":
            node.right.ParentId = nodeChose.Id
        else:
            node.left.ParentId = nodeChose.Id
        nodeChose = deleteNode(nodeChose)
        return node
    
def deleteDistributor():
    global root
    while True:
        while True:
            print("\n =====  Nhap thong tin nha phan phoi muon xoa [nhan 'q' hoac 'Q' de thoat chuc nang]")
            id = input(" >> Nhap id nha phan phoi muon xoa: ")
            if(id == 'q' or id == 'Q'): 
                return
            if(root==None):
                print("\n <!>=<!> Khong con nha phan phoi nao, Moi thoat chuc nang  <!>=<!>")
                continue
            node = root.findId(id)
            if(node==None):
                print("\n <!>=<!> Khong ton tai id tren, Moi nhap lai <!>=<!>")
                continue
            
            # temp = node

            #Choose children node for alternative and replace, update tree 
            node = deleteNode(node)

            #update file sql  
            cursor.execute("truncate table NhaPhanPhoi")
            cursor.commit()
            # if temp is root:
            #     loadData()
            #     return
            root.traversalAndUpdate()

            loadData() # can be remove 
            break
        
def calculateCommission(id, dicSale):
    global commission
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
        dicCommission[node.right.Id] = calculateCommission(node.right.Id,dicSale)
        dicCommission[id] += dicCommission[node.right.Id] / 10
        return dicCommission[id]
    elif(node.left and node.right is None):
        dicCommission[node.left.Id] = calculateCommission(node.left.Id,dicSale)
        dicCommission[id] += dicCommission[node.left.Id] / 10
        return dicCommission[id]
    else:
        dicCommission[node.right.Id] = calculateCommission(node.right.Id,dicSale)
        dicCommission[node.left.Id] = calculateCommission(node.left.Id,dicSale)
        if(dicCommission[node.right.Id] < 0.9*dicCommission[node.left.Id]):
            dicCommission[id] += dicCommission[node.right.Id] / 10
        elif(dicCommission[node.left.Id] < 0.9*dicCommission[node.right.Id]):
            dicCommission[id] += dicCommission[node.left.Id] / 10
        else:
            dicCommission[id] += dicCommission[node.right.Id] / 10
            dicCommission[id] += dicCommission[node.left.Id] / 10
        return dicCommission[id]

def inputSales():
    global cnt, cursor 
    # cnt = number of sale table in database - 1 (1 for Distributor Table)
    cursor.execute("select count(TABLE_NAME) from INFORMATION_SCHEMA.TABLES")
    cnt = cursor.fetchone()[0]

    #dictionary to save sale of each distributor (id)
    dicSale = {}
    print("\n =====  Nhap thong tin doanh thu dot " + str(cnt) + " [nhan 'q' hoac 'Q' de thoat chuc nang]")
    while True and root:
        id = input(" >> Nhap id: ")
        if id=='q' or id=='Q':
            return
        if(root.findId(id)==None):
            print("\n <!><!> Id khong ton tai, Hay nhap lai id <!><!>")
            continue
        sale = int(input(" >> Nhap so san pham ban duoc: "))
        dicSale[id] = sale
        text = input("\n ===== Tiep tuc [phim bat ky] hay dung [d||D]: ")
        if(text == 'd' or text == 'D'):
            break
    
    #Calculate commission
    for i in dicSale:
        dicCommission[i] = calculateCommission(i,dicSale)

    #create New Sale Table
    createNewSaleTable()

    #insert value to sale table
    queryForInsert = "insert into DoanhSoDot_"+str(cnt)+" values (?,?,?)"
    for i in dicSale:
        parameters = [i,dicSale[i],dicCommission[i]]
        cursor.execute(queryForInsert, parameters)
        cursor.commit()
    
    cnt += 1 # increment number of sale tables

def wrongInput():
    print("\n <!><!> Chon lai chuc nang tu 1 den 4 <!><!>")

#Load data from file (Check if Distributor table doesn't exist)
def loadData():
    global root, cursor
    if cursor.execute("select count(TABLE_NAME) from INFORMATION_SCHEMA.TABLES where TABLE_NAME like 'NhaPhanPhoi'").fetchone()[0]: # Table exists
        root = None
        listRow = []
        for row in cursor.execute("select * from NhaPhanPhoi order by TimeStartInput asc"):
            listRow.append(row)
        while(len(listRow) > 0):
            row = listRow[0]
            if(row.ParentId == None):
                root = Distributor(row.Id,row.Name,row.ParentId)
            else:
                if root:
                    node =  root.findId(row.ParentId)
                    if node:
                        node.addNewDistributor(Distributor(row.Id,row.Name,row.ParentId))
                else:
                    listRow.append(row)
            listRow.pop(0)
            dicCommission[row.Id] = 0
    else:
        createNewDistributorTable()
        root = None




#set up for database connection
driver = "{ODBC Driver 17 for SQL Server}"
server = "DESKTOP-4SO5SON\MSSQLSERVERR"
database = "QuanLyNhaPhanPhoi"
conn = pyodbc.connect("DRIVER=" + driver
                      + ";SERVER=" + server
                      + ";DATABASE=" + database
                      + ";Trusted_Connection=yes;")

cursor = conn.cursor()

root = None

#dictionary of Commission 
dicCommission = {}

loadData()

while True:   
    print() 
    print(" =======================================================")
    print(" =====  Moi ban chon chuc nang bang phim 1,2,3,4   =====")
    print(" =====  1. Nhap thong tin nha phan phoi moi        =====")
    print(" =====  2. Xoa thong tin ve nha phan phoi          =====")
    print(" =====  3. Nhap thong tin ve so san pham ban duoc  =====")
    print(" =====  4. Thoat chuong trinh                      =====")
    print(" =======================================================")
    n = int(input(" >> Chon chuc nang: "))
    if(n==4):
        break
    chooseFunction(n)
    text = input("\n >> Tiep tuc [phim bat ky] hay thoat [q||Q] chuong trinh: ")
    if(text=='q' or text=='Q'):
        break

