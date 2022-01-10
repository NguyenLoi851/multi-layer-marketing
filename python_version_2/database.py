import distributor

def getConnectionString():
    driver = "{ODBC Driver 17 for SQL Server}"
    server = "DESKTOP-4SO5SON\MSSQLSERVERR"
    database = "QuanLyNhaPhanPhoi"
    return "DRIVER=" + driver + ";SERVER=" + server + ";DATABASE=" + database + ";Trusted_Connection=yes;"

#Load data from file (Check if Distributor table doesn't exist)
def loadData(cursor):
    dicCommission = {}
    if cursor.execute("select count(TABLE_NAME) from INFORMATION_SCHEMA.TABLES where TABLE_NAME like 'NhaPhanPhoi'").fetchone()[0]: # Table exists
        root = None
        listRow = []
        for row in cursor.execute("select * from NhaPhanPhoi order by TimeStartInput asc"):
            listRow.append(row)
        while(len(listRow) > 0):
            row = listRow[0]
            if(row.ParentId == None):
                root = distributor.Distributor(row.Id,row.Name,row.ParentId)
            else:
                if root:
                    node =  root.findId(row.ParentId)
                    if node:
                        node.addNewDistributor(distributor.Distributor(row.Id,row.Name,row.ParentId))
                else:
                    listRow.append(row)
            listRow.pop(0)
            dicCommission[row.Id] = 0
    else:
        createNewDistributorTable(cursor)
        root = None
    return root, dicCommission

#create table for distributor in database if it was not already created
def createNewDistributorTable(cursor):
    #global cursor
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

#create new table for sale round
def createNewSaleTable(cursor, cnt):
    #global cursor, cnt
    cursor.execute('''
                    create table DoanhSoDot_''' + str(cnt) +'''
                    (
                        Id nvarchar(10),
                        SoSP int,
                        TienHoaHong float,
                    )
                    ''')
    cursor.commit()
