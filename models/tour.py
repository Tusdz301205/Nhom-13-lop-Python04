"""Domain class đại diện sản phẩm tour du lịch."""

from __future__ import annotations


class Tour:
    """Quản lý thông tin và trạng thái kinh doanh của một tour."""

    DANG_KINH_DOANH = "DANG_KINH_DOANH"
    NGUNG_KINH_DOANH = "NGUNG_KINH_DOANH"
    TRANG_THAI_HOP_LE = (DANG_KINH_DOANH, NGUNG_KINH_DOANH)

    def __init__(
        self,
        ma_tour: str,
        ten_tour: str,
        diem_den: str,
        mo_ta: str = "",
        trang_thai: str = DANG_KINH_DOANH,
    ) -> None:
        self.ma_tour: str = self._chuoi_bat_buoc(ma_tour, "Mã tour")
        self.ten_tour: str = self._chuoi_bat_buoc(ten_tour, "Tên tour")
        self.diem_den: str = self._chuoi_bat_buoc(diem_den, "Điểm đến")
        self.mo_ta: str = self._chuoi_tuy_chon(mo_ta)
        self.trang_thai: str = self._kiem_tra_trang_thai(trang_thai)

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _chuoi_tuy_chon(gia_tri: str) -> str:
        if not isinstance(gia_tri, str):
            raise ValueError("Mô tả phải là chuỗi.")
        return gia_tri.strip()

    @classmethod
    def _kiem_tra_trang_thai(cls, trang_thai: str) -> str:
        ket_qua = cls._chuoi_bat_buoc(trang_thai, "Trạng thái").upper()
        if ket_qua not in cls.TRANG_THAI_HOP_LE:
            raise ValueError("Trạng thái tour không hợp lệ.")
        return ket_qua

    def cap_nhat_thong_tin(
        self,
        ten_tour: str | None = None,
        diem_den: str | None = None,
        mo_ta: str | None = None,
    ) -> None:
        """Kiểm tra đầy đủ trước khi cập nhật; None nghĩa là giữ nguyên."""
        ten_moi = self.ten_tour if ten_tour is None else self._chuoi_bat_buoc(ten_tour, "Tên tour")
        diem_moi = self.diem_den if diem_den is None else self._chuoi_bat_buoc(diem_den, "Điểm đến")
        mo_ta_moi = self.mo_ta if mo_ta is None else self._chuoi_tuy_chon(mo_ta)
        self.ten_tour = ten_moi
        self.diem_den = diem_moi
        self.mo_ta = mo_ta_moi

    def dang_kinh_doanh(self) -> bool:
        """Kiểm tra trạng thái tour; đợt khởi hành còn phải được kiểm tra riêng."""
        return self.trang_thai == self.DANG_KINH_DOANH

    def ngung_kinh_doanh(self) -> None:
        """Ngừng kinh doanh tour thay vì xóa dữ liệu lịch sử."""
        if not self.dang_kinh_doanh():
            raise ValueError("Tour đã ngừng kinh doanh.")
        self.trang_thai = self.NGUNG_KINH_DOANH
