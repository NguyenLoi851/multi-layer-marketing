import random, time

class Distributor:
    def __init__(self,Id,Name,ParentId):
        self.Id = Id
        self.Name = Name
        self.ParentId = ParentId
        self.left = None
        self.right = None
    
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

    def traversalAndUpdate(self, cursor):
        if self == None or self.Id == None:
            return
        time.sleep(0.003)
        query = "insert into NhaPhanPhoi values (?,?,?)"
        parameters = [self.Id, self.Name, self.ParentId]
        cursor.execute(query, parameters)
        cursor.commit()
        time.sleep(0.003)
        if self.left and self.left.Id:
            self.left.traversalAndUpdate(cursor)
        if self.right and self.right.Id:
            self.right.traversalAndUpdate(cursor)