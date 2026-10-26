"""Domain class mô tả một hoạt động trong lịch trình du lịch."""

from __future__ import annotations

from datetime import time


class HoatDongLichTrinh:
    """Một hoạt động trong ngày thứ N, dùng giờ địa phương không kèm múi giờ.

    LichTrinh kiểm tra trùng giờ giữa các hoạt động. Việc kiểm tra ngay_thu
    có vượt thời lượng DotKhoiHanh cụ thể thuộc tầng nghiệp vụ sau này.
    """

    def __init__(
        self,
        ma_hoat_dong: str,
        ma_lich_trinh: str,
        ngay_thu: int,
        gio_bat_dau: time,
        gio_ket_thuc: time,
        dia_diem: str,
        noi_dung: str,
    ) -> None:
        self.ma_hoat_dong: str = self._chuoi_bat_buoc(ma_hoat_dong, "Mã hoạt động")
        self.ma_lich_trinh: str = self._chuoi_bat_buoc(ma_lich_trinh, "Mã lịch trình")
        self._kiem_tra_thoi_gian(ngay_thu, gio_bat_dau, gio_ket_thuc)
        self.ngay_thu: int = ngay_thu
        self.gio_bat_dau: time = gio_bat_dau
        self.gio_ket_thuc: time = gio_ket_thuc
        self.dia_diem: str = self._chuoi_bat_buoc(dia_diem, "Địa điểm")
        self.noi_dung: str = self._chuoi_bat_buoc(noi_dung, "Nội dung")

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _kiem_tra_thoi_gian(ngay_thu: int, gio_bat_dau: time, gio_ket_thuc: time) -> None:
        if isinstance(ngay_thu, bool) or not isinstance(ngay_thu, int) or ngay_thu < 1:
            raise ValueError("Ngày thứ phải là số nguyên dương.")
        if not isinstance(gio_bat_dau, time) or not isinstance(gio_ket_thuc, time):
            raise ValueError("Giờ bắt đầu và kết thúc phải có kiểu datetime.time.")
        if gio_bat_dau.tzinfo is not None or gio_ket_thuc.tzinfo is not None:
            raise ValueError("Thời gian hoạt động dùng giờ địa phương không kèm múi giờ.")
        if gio_bat_dau >= gio_ket_thuc:
            raise ValueError("Giờ kết thúc phải sau giờ bắt đầu trong cùng ngày.")

    def kiem_tra_thoi_gian_hop_le(self) -> bool:
        """Kiểm tra thời gian sau khi đối tượng được tạo."""
        try:
            self._kiem_tra_thoi_gian(self.ngay_thu, self.gio_bat_dau, self.gio_ket_thuc)
            return True
        except ValueError:
            return False

    def cap_nhat_hoat_dong(
        self,
        ngay_thu: int | None = None,
        gio_bat_dau: time | None = None,
        gio_ket_thuc: time | None = None,
        dia_diem: str | None = None,
        noi_dung: str | None = None,
    ) -> None:
        """Cập nhật dữ liệu hợp lệ; khi thuộc lịch trình phải kiểm tra trùng giờ ở LichTrinh."""
        ngay_moi = self.ngay_thu if ngay_thu is None else ngay_thu
        bat_dau_moi = self.gio_bat_dau if gio_bat_dau is None else gio_bat_dau
        ket_thuc_moi = self.gio_ket_thuc if gio_ket_thuc is None else gio_ket_thuc
        self._kiem_tra_thoi_gian(ngay_moi, bat_dau_moi, ket_thuc_moi)
        dia_diem_moi = self.dia_diem if dia_diem is None else self._chuoi_bat_buoc(dia_diem, "Địa điểm")
        noi_dung_moi = self.noi_dung if noi_dung is None else self._chuoi_bat_buoc(noi_dung, "Nội dung")
        self.ngay_thu = ngay_moi
        self.gio_bat_dau = bat_dau_moi
        self.gio_ket_thuc = ket_thuc_moi
        self.dia_diem = dia_diem_moi
        self.noi_dung = noi_dung_moi
