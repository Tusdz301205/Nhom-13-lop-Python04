"""Domain class lưu danh mục điểm đến và tọa độ tùy chọn."""

from __future__ import annotations

from math import isfinite


class DiemDen:
    """Dữ liệu điểm đến đã kiểm tra; không truy cập mạng hoặc lưu file."""

    def __init__(
        self,
        ma_diem_den: str,
        ten_diem_den: str,
        tinh_thanh: str,
        mo_ta: str = "",
        vi_do: float | None = None,
        kinh_do: float | None = None,
    ) -> None:
        self.ma_diem_den: str = self._chuoi_bat_buoc(ma_diem_den, "Mã điểm đến")
        self.ten_diem_den: str = self._chuoi_bat_buoc(ten_diem_den, "Tên điểm đến")
        self.tinh_thanh: str = self._chuoi_bat_buoc(tinh_thanh, "Tỉnh/thành")
        self.mo_ta: str = self._kiem_tra_mo_ta(mo_ta)
        self.vi_do, self.kinh_do = self._kiem_tra_toa_do(vi_do, kinh_do)

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _kiem_tra_mo_ta(mo_ta: str) -> str:
        if not isinstance(mo_ta, str):
            raise ValueError("Mô tả phải là chuỗi.")
        return mo_ta.strip()

    @staticmethod
    def _kiem_tra_mot_toa_do(gia_tri: float, gioi_han: int, ten_truong: str) -> float:
        if isinstance(gia_tri, bool) or not isinstance(gia_tri, (int, float)):
            raise ValueError(f"{ten_truong} phải là số int hoặc float.")
        # Kiểm tra miền trước khi chuyển kiểu để xử lý cả số nguyên quá lớn.
        if not -gioi_han <= gia_tri <= gioi_han or not isfinite(gia_tri):
            raise ValueError(
                f"{ten_truong} phải hữu hạn và nằm trong khoảng "
                f"{-gioi_han} đến {gioi_han}."
            )
        return float(gia_tri)

    @classmethod
    def _kiem_tra_toa_do(
        cls, vi_do: float | None, kinh_do: float | None
    ) -> tuple[float | None, float | None]:
        if vi_do is None and kinh_do is None:
            return None, None
        if vi_do is None or kinh_do is None:
            raise ValueError("Phải cung cấp cả vĩ độ và kinh độ, hoặc cả hai là None.")
        vi_do_hop_le = cls._kiem_tra_mot_toa_do(vi_do, 90, "Vĩ độ")
        kinh_do_hop_le = cls._kiem_tra_mot_toa_do(kinh_do, 180, "Kinh độ")
        return vi_do_hop_le, kinh_do_hop_le

    def cap_nhat_thong_tin(
        self,
        ten_diem_den: str | None = None,
        tinh_thanh: str | None = None,
        mo_ta: str | None = None,
    ) -> None:
        """None giữ nguyên trường; chỉ cập nhật khi tất cả dữ liệu hợp lệ."""
        ten_moi = (
            self.ten_diem_den
            if ten_diem_den is None
            else self._chuoi_bat_buoc(ten_diem_den, "Tên điểm đến")
        )
        tinh_moi = (
            self.tinh_thanh
            if tinh_thanh is None
            else self._chuoi_bat_buoc(tinh_thanh, "Tỉnh/thành")
        )
        mo_ta_moi = self.mo_ta if mo_ta is None else self._kiem_tra_mo_ta(mo_ta)
        self.ten_diem_den = ten_moi
        self.tinh_thanh = tinh_moi
        self.mo_ta = mo_ta_moi

    def cap_nhat_toa_do(self, vi_do: float | None, kinh_do: float | None) -> None:
        """Cập nhật cả cặp tọa độ; truyền (None, None) để xóa cả cặp."""
        vi_do_moi, kinh_do_moi = self._kiem_tra_toa_do(vi_do, kinh_do)
        self.vi_do = vi_do_moi
        self.kinh_do = kinh_do_moi
