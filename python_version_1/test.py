# import pyodbc

# driver = "{ODBC Driver 17 for SQL Server}"
# server = "DESKTOP-4SO5SON\MSSQLSERVERR"
# database = "QuanLyMonHoc"
# conn = pyodbc.connect("DRIVER=" + driver
#                       + ";SERVER=" + server
#                       + ";DATABASE=" + database
#                       + ";Trusted_Connection=yes;")

# # conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};\
# #                       SERVER=DESKTOP-4SO5SON\MSSQLSERVERR;\
# #                       DATABASE=QuanLyMonHoc;\
# #                       Trusted_Connection=yes;")

# cursor = conn.cursor()

# cnt =0

# # cursor.execute("select COUNT(TABLE_NAME) from INFORMATION_SCHEMA.TABLES")
# # print(cursor.fetchall())

# # cursor.execute("insert into SinhVien values ('45','h','n','g')")
# # cursor.commit()
# # row =  cursor.execute("select * from SinhVien where MaSV like '45'")
# # print(row.MaSV)
# temp = 0
# a=cursor.execute("select * from SinhVien where MaSV like '45'")
# for x in a:
#   temp = x.MaSV
# print(temp)


# #print(test)
# # query = "insert into MonHoc(Ma, Ten, SoTinChi) values (?,?,?)"
# # parameters=['34','hh',4]

# # cursor.execute(query,parameters)
# # result = cursor.fetchone()

# # def createNewTable():
# #     cursor.execute('''
# #                         create table SinhVien(
# #                             MaSV nvarchar(50) primary key,
# #                             TenSV nvarchar(50),
# #                             GioiTinh nvarchar(50)
# #                         )
# #                     ''')
# #     conn.commit

# # if(result is not None):
# #     print("Table exists")
# #     while result is not None:
# #         print(result)
# #         result = cursor.fetchone()
# # else:
# #     print("Table does not exist")
    
# #     print("Done")



# # for driver in pyodbc.drivers():
# #     print(driver)

# # thisdict =	{
# #   "brand": "Ford",
# #   "model": "Mustang",
# #   "year": 1964
# # }
# # # for i in thisdict:
# # #     print(i)
# # # print(thisdict["year"])
# # #print(thisdict["brd"])

# # if "brd" not in thisdict:
# #     print("He")

class Node:
  def __init__(self,data):
    self.data = data
    self.left = None
    self.right = None

root = Node(5)
a = Node(4)
b = Node(6)
root.left=a
root.right = b

temp = a
temp.data = 9
print(a.data)
print(root.left.data)