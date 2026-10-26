# Hệ thống quản lý Tour và Lịch trình Du lịch

Môn học: Lập trình Python - OOP  
Lớp: Python 04  
Nhóm: 13

## Mục tiêu đồ án

Quản lý tour, lịch trình nhiều ngày, đợt khởi hành, khách đăng ký và các dịch vụ tùy chọn. Hướng tới chức năng tìm kiếm tour theo ngày/điểm đến/giá, tính giá theo dịch vụ lựa chọn và thống kê giá trị đơn đăng ký cùng tỷ lệ lấp đầy.

## Phân công các Class hiện có

Phạm Bảo Ngọc:
- NguoiDung
- HanhKhach
- YeuCauHuy

Trang Trung Tiến:
- DatTour

Hồ Ngọc Tú:
- Tour
- LichTrinh
- HoatDongLichTrinh
- DotKhoiHanh

## Điều chỉnh phạm vi

- Loại bỏ hai Domain Class `ThanhToan` và `HoanTien`: ứng dụng không thực hiện giao dịch thanh toán hoặc hoàn tiền.
- Giữ nghiệp vụ tính giá, thông tin giá của đợt khởi hành và tổng giá trị đơn đặt tour. Không đồng nhất tổng giá trị đơn với tiền đã thực thu.
- `YeuCauHuy` vẫn dùng để theo dõi việc hủy đăng ký, không đồng nghĩa hoàn tiền.

## Đề xuất Class bổ sung (chưa triển khai, cần thống nhất trước khi viết)

- `DichVu`: danh mục dịch vụ tùy chọn, giá dịch vụ, trạng thái cung cấp.
- `DichVuDatTour`: dịch vụ được chọn trong một đơn, số lượng và đơn giá chốt tại thời điểm đặt.

Hai Class trên dự kiến giao Trang Trung Tiến phụ trách, để phân công Domain Class dự kiến trở lại 3–3–4 sau khi được chốt.

## Quy ước

- Python 3
- Class: PascalCase
- File, thuộc tính, phương thức: snake_case
- Mỗi Domain Class đặt trong một file Python thuộc `models/`
- Thành viên làm việc trên nhánh riêng, tích hợp qua Pull Request
- Dữ liệu chính dự kiến lưu bằng JSON theo tài liệu yêu cầu của học phần (chưa triển khai ở giai đoạn viết Class)

## Trạng thái

Hiện đang ở **giai đoạn xây dựng và rà soát Class**. Chưa có Tkinter, Repository đọc/ghi JSON, luồng nghiệp vụ hoàn chỉnh hoặc bộ kiểm thử tích hợp.
