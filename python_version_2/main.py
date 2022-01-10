import database, pyodbc, function

conn = pyodbc.connect(database.getConnectionString())

cursor = conn.cursor()

root = None

# cnt = number of sale table in database - 1 (1 for Distributor Table)
cnt = 0

#dictionary of Commission 
dicCommission = {}

root, dicCommission = database.loadData(cursor)

while True:   
    print() 
    print(" =======================================================")
    print(" =====  Mời bạn chọn chức năng bằng phím 1,2,3,4   =====")
    print(" =====  1. Nhập thông tin nhà phân phối mới        =====")
    print(" =====  2. Xóa thông tin về nhà phân phối          =====")
    print(" =====  3. Nhập thông tin về số sản phẩm bán được  =====")
    print(" =====  4. Thoát chương trình                      =====")
    print(" =======================================================")
    n = int(input(" >> Chọn chức năng: "))
    if(n==4):
        break
    root, dicCommission = database.loadData(cursor)
    function.chooseFunction(n, root, cursor, dicCommission)
    text = input("\n >> Tiếp tục [phím bất kỳ] hay thoát [q||Q] chương trình: ")
    if(text=='q' or text=='Q'):
        break
