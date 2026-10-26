# Hệ thống quản lý Tour và Lịch trình Du lịch

**Học phần:** Lập trình Python (OOP) · **Lớp:** Python 04 · **Nhóm:** 13  
**Đề tài:** Số 19 trong `Quy_dinh_do_an.pdf`  
**Trạng thái:** Đang xây dựng, rà soát và kiểm thử các **Domain Class**; **chưa hoàn thành ứng dụng**.

## 1. Mục tiêu và phạm vi

Ứng dụng quản lý tour du lịch, điểm đến, lịch trình nhiều ngày, hoạt động trong lịch trình, đợt khởi hành, khách đăng ký và các dịch vụ tùy chọn.

Các chức năng cần đáp ứng theo đề tài 19:
- Xây dựng lịch trình nhiều ngày.
- Đăng ký khách tham gia tour và kiểm tra số chỗ còn lại.
- Tính giá theo dịch vụ được lựa chọn.
- Tìm kiếm tour theo ngày, điểm đến và mức giá.
- Thống kê doanh thu và tỷ lệ lấp đầy đợt khởi hành.

**Phạm vi đã điều chỉnh:** Không xây dựng quy trình giao dịch **thanh toán/hoàn tiền**. Vẫn quản lý giá tour, chi phí dịch vụ và tổng giá trị đơn đăng ký. Nếu không có dữ liệu tiền thực thu, kết quả thống kê phải ghi rõ là **giá trị đơn đăng ký đã xác nhận**, không gọi đó là doanh thu thực thu.

Ngoài yêu cầu riêng của đề tài 19, ứng dụng hoàn chỉnh về sau còn phải đáp ứng yêu cầu chung của học phần: **Tkinter, CRUD + tìm kiếm/lọc, JSON, xử lý lỗi, Regex, tài khoản/phân quyền, thống kê, Crawl/API, kiểm thử và đóng gói**. Phạm vi hiện tại chỉ là **thiết kế và xây dựng Class**.

## 2. Phân công nhóm — 12 Domain Class

| Thành viên | File | Class | Hiện trạng trên `main` |
|---|---|---|---|
| **Phạm Bảo Ngọc** | `models/nguoi_dung.py` | `NguoiDung` | Đã có; cần rà soát Regex, validation |
| | `models/hanh_khach.py` | `HanhKhach` | Đã có; cần rà soát |
| | `models/yeu_cau_huy.py` | `YeuCauHuy` | Đã có; cần rà soát |
| | `models/danh_gia_tour.py` | `DanhGiaTour` | **Cần tạo mới** (mở rộng) |
| **Trang Trung Tiến** | `models/dat_tour.py` | `DatTour` | Đã có; cần mở rộng tính giá dịch vụ |
| | `models/dot_khoi_hanh.py` | `DotKhoiHanh` | Đã có; chuyển người phụ trách sang Tiến |
| | `models/dich_vu.py` | `DichVu` | **Cần tạo mới** |
| | `models/dich_vu_dat_tour.py` | `DichVuDatTour` | **Cần tạo mới** |
| **Hồ Ngọc Tú** | `models/tour.py` | `Tour` | Đã có; cần điều chỉnh liên kết điểm đến |
| | `models/diem_den.py` | `DiemDen` | **Cần tạo mới** |
| | `models/lich_trinh.py` | `LichTrinh` | Đã có; cần rà soát |
| | `models/hoat_dong_lich_trinh.py` | `HoatDongLichTrinh` | Đã có; cần rà soát |

**Ghi chú:**
- Tổng cộng **12 Domain Class trong thiết kế mục tiêu**: **8 Class phù hợp phạm vi mới đã có**, **4 Class cần tạo mới**.
- Hai file cũ `models/thanh_toan.py` và `models/hoan_tien.py` **vẫn tồn tại trên `main` tại thời điểm cập nhật README**, nhưng **không nằm trong phạm vi triển khai mới**. Không tiếp tục phát triển hoặc import chúng. Việc xóa mã cũ sẽ được xử lý ở một thay đổi riêng.
- `DotKhoiHanh` đã được viết trước đây; Tiến tiếp nhận trách nhiệm chỉnh sửa, kiểm thử và tích hợp, **không tạo Class trùng**.
- `DanhGiaTour` là chức năng **mở rộng tự chọn**; các chức năng bắt buộc được ưu tiên trước.

## 3. Quan hệ nghiệp vụ dự kiến

- `Tour` tham chiếu `DiemDen` (điểm đến chính).
- Một `Tour` có lịch trình `LichTrinh` với nhiều `HoatDongLichTrinh`.
- Một `Tour` có thể có nhiều `DotKhoiHanh`.
- Một `NguoiDung` có thể tạo nhiều `DatTour`; mỗi đơn thuộc một `DotKhoiHanh`.
- Một `DatTour` có nhiều `HanhKhach` và nhiều dòng `DichVuDatTour` tham chiếu `DichVu`.
- `YeuCauHuy` gắn với đơn đặt tour; **hủy đăng ký không đồng nghĩa hoàn tiền**.
- `DanhGiaTour` gắn với `DatTour` để có thể xác minh hành trình liên quan khi tích hợp.

**Hợp đồng dữ liệu đang cần hoàn thiện:**
- `Tour` hiện có `diem_den: str`; thiết kế mới **dự kiến thay bằng `ma_diem_den: str`**. Đây là thay đổi interface, người phụ trách phải trao đổi và đồng bộ test trước khi merge.
- `DotKhoiHanh.gia_ap_dung` là giá tại đợt khởi hành; `DatTour.don_gia_da_chot` giữ giá tour tại thời điểm đặt.
- `DichVuDatTour` giữ `so_luong` và giá dịch vụ đã chốt. Công thức dự kiến:
  `tong_tien = so_nguoi * don_gia_da_chot + sum(so_luong_dich_vu * don_gia_dich_vu_da_chot)`.
- Quy tắc giá theo người/lần sử dụng, trạng thái đơn nào chiếm chỗ và cách xác định thống kê doanh thu vẫn cần thống nhất trước khi triển khai nghiệp vụ tích hợp. **Không tự suy đoán chính sách.**

## 4. Quy tắc chung khi viết Class

1. **Một Domain Class một file** trong `models/`. Tên Class dùng `PascalCase`; tên file, thuộc tính và phương thức dùng `snake_case`.
2. **Kiểu dữ liệu:** mã định danh dùng `str` không rỗng; tiền dùng `decimal.Decimal` hữu hạn (không dùng `float` cho tiền); ngày/giờ dùng `datetime.datetime` hoặc `datetime.time`; số lượng dùng `int` hợp lệ, từ chối `bool` giả dạng `int`.
3. **Liên kết bằng mã định danh** như `ma_tour`, `ma_dat_tour`, `ma_dot_khoi_hanh`. Không tự truy cập file, tìm toàn bộ các đối tượng hoặc kiểm tra tồn tại mã ngoài phạm vi đối tượng. Những ràng buộc giữa nhiều đối tượng do lớp quản lý nghiệp vụ thực hiện sau.
4. **Không tự đổi các mã trạng thái đã thống nhất:** `Tour` (`DANG_KINH_DOANH`, `NGUNG_KINH_DOANH`), `DotKhoiHanh` (`MO_BAN`, `DONG_BAN`, `DA_HUY`), `DatTour` (`CHO_XAC_NHAN`, `DA_XAC_NHAN`, `DA_HUY`), `YeuCauHuy` (`CHO_XU_LY`, `CHAP_NHAN`, `TU_CHOI`).
5. **Validation và lỗi:** kiểm tra dữ liệu trước khi cập nhật; dữ liệu hoặc thao tác sai phát sinh `ValueError` có thông báo rõ nghĩa. Tránh cập nhật dở dang một đối tượng nếu thao tác thất bại. Không dùng `except:` trống để bỏ qua lỗi.
6. **Bảo mật và định dạng:** không lưu mật khẩu rõ trong Class hay để lộ `mat_khau_hash` qua `repr`; áp dụng Regex cho email và số điện thoại khi phù hợp.
7. **Tách trách nhiệm:** Domain Class không gọi `input()`, `print()`, Tkinter, API hoặc đọc/ghi JSON. Lưu trữ bằng **JSON** sẽ nằm trong lớp repository ở giai đoạn sau.
8. **Không tự bổ sung nghiệp vụ thanh toán/hoàn tiền** hoặc tự đặt quy tắc phạt hủy, chính sách giá, giữ chỗ khi chưa được nhóm thống nhất.
9. **Kiểm thử độc lập:** dự kiến đặt test trong `tests/test_<ten_file>.py`, sử dụng `unittest`; bao phủ dữ liệu đúng, dữ liệu sai và trường hợp biên. Các file test này **chưa có trên `main`** tại thời điểm cập nhật.
10. **GitHub:** mỗi thành viên làm trên nhánh riêng, chỉ sửa phần được giao; thay đổi constructor, thuộc tính hoặc trạng thái ảnh hưởng Class khác phải trao đổi trước. Tạo Pull Request để review, không tự merge khi chưa thống nhất.

## 5. Cấu trúc repository hiện tại

```text
Nhom-13-lop-Python04/
├── .gitignore
├── README.md
└── models/
    ├── __init__.py
    ├── nguoi_dung.py
    ├── hanh_khach.py
    ├── yeu_cau_huy.py
    ├── dat_tour.py
    ├── dot_khoi_hanh.py
    ├── tour.py
    ├── lich_trinh.py
    ├── hoat_dong_lich_trinh.py
    ├── thanh_toan.py       # File cũ, không thuộc phạm vi mới
    └── hoan_tien.py        # File cũ, không thuộc phạm vi mới
```

**Chưa có:** `DiemDen`, `DichVu`, `DichVuDatTour`, `DanhGiaTour`, thư mục `tests/`, giao diện Tkinter, lưu trữ JSON, các lớp quản lý nghiệp vụ và luồng ứng dụng hoàn chỉnh.

## 6. Điều kiện hoàn thành giai đoạn Class

- Có đầy đủ **12 Domain Class mục tiêu** theo phân công mới (bao gồm các Class cần tạo mới).
- Mỗi Class có constructor, thuộc tính, phương thức và validation phù hợp trách nhiệm.
- Quan hệ/mã tham chiếu thống nhất, không để thay đổi interface gây lỗi tích hợp.
- Có test độc lập cho từng Class, bao gồm các trường hợp lỗi và biên.
- Mỗi thành viên mở PR cho phần việc của mình; nhóm review trước khi merge.

**Sau giai đoạn Class:** xây dựng lớp quản lý nghiệp vụ, CRUD và tìm kiếm; lưu trữ JSON với xử lý lỗi; giao diện Tkinter; tài khoản/phân quyền; thống kê; Crawl/API; kiểm thử tích hợp và đóng gói theo tài liệu môn học.
