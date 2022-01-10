# multilevel_model_python
This is my project 1 in university.

YÊU CẦU LẬP TRÌNH PROJECT 1

GV: Nguyễn Thị Thu Hương

Một công ty bán hàng đa cấp tổ chức các nhà phân phối  theo  mô hình  nhị phân
 

Mô hình này cho phép mỗi nhà phân phối được và chỉ được tuyển mộ thêm hai nhà phân phối thuộc tầng 1 (thế hệ thứ nhất) và bắt buộc hai nhánh của mình phải luôn phát triển đồng đều (số sản phẩm bán được của nhánh ít phải >= 90% số sản phẩm bán được của nhánh nhiều). Nếu không thực hiện được điều này thì nhà phân phối sẽ chỉ được chi trả hoa hồng theo nhánh yếu hơn.
Hãy viết chương trình cho phép thực hiện chức năng sau:
1.	Nhập thông tin về nhà phân phối mới , bao gồm (mã nhà phân phối, họ tên, mã nhà phân phối cấp trên). Nếu nhà phân phối cấp trên đã đủ 2 nhà phân phối ở tầng 1, nhà phân phối mới sẽ được thêm vào cấp dưới tiếp theo. Giả sử chỉ lập 1 cây phân phối, nhà cung cấp được nhập đầu tiên là nhà cung cấp ở cấp cao nhất. Không giới hạn số tầng của cây. Chú ý lưu thông tin các nhà cung cấp được lưu vào tệp văn bản, hoặc tệp CSDL.
2.	Xóa thông tin về nhà phân phối. Nhà phân phối cấp ngay dưới có mức hoa hồng cao hơn trong đợt phân phối gần nhất sẽ được chuyển lên cấp trên. Nếu hai nhà phân phối cấp dưới lượng hoa hồng ngang nhau thì chọn người có số lượng hàng bán nhiều hơn, nếu tất cả các tiêu chí của các nhà phân phối cấp dưới hoàn toàn giống nhau thì chọn ngẫu nhiên.
3.	Nhập thông tin về số sản phẩm bán được trong từng đợt, bao gồm (mã NCC, số luợng SP).  Tính hoa hồng cần trả cho tất cả các nhà phân phối. Biết tỷ lệ hoa hồng cho nhà phân phối bán trực tiếp là 10%, mỗi mức cấp trên tỷ lệ là 10% của mức cấp ngay dưới. Thông tin về hoa hồng được lưu vào một tệp văn bản hoặc tệp CSDL, bao gồm (Mã NCC, số SP, số tiền hoa hồng)
