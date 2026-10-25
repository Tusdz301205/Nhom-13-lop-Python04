"""Domain class representing one passenger on a tour booking."""

from __future__ import annotations


class HanhKhach:
    """Đại diện một người thực sự tham gia chuyến đi."""

    def __init__(
        self,
        ma_hanh_khach: str,
        ma_dat_tour: str,
        ho_ten: str,
        so_dien_thoai: str | None = None,
    ) -> None:
        self.ma_hanh_khach = self._chuoi_bat_buoc(ma_hanh_khach, "Mã hành khách")
        self.ma_dat_tour = self._chuoi_bat_buoc(ma_dat_tour, "Mã đặt tour")
        self.ho_ten = self._chuoi_bat_buoc(ho_ten, "Họ tên")
        self.so_dien_thoai = self._so_dien_thoai_tuy_chon(so_dien_thoai)

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _so_dien_thoai_tuy_chon(gia_tri: str | None) -> str | None:
        if gia_tri is None:
            return None
        if not isinstance(gia_tri, str):
            raise ValueError("Số điện thoại phải là chuỗi hoặc None.")
        gia_tri = gia_tri.strip()
        return gia_tri or None

    def cap_nhat_thong_tin(
        self,
        ho_ten: str | None = None,
        so_dien_thoai: str | None = None,
    ) -> None:
        """Cập nhật họ tên và/hoặc số điện thoại nếu được cung cấp."""
        if ho_ten is not None:
            self.ho_ten = self._chuoi_bat_buoc(ho_ten, "Họ tên")
        if so_dien_thoai is not None:
            self.so_dien_thoai = self._so_dien_thoai_tuy_chon(so_dien_thoai)

    def kiem_tra_hop_le(self) -> bool:
        """Kiểm tra các trường bắt buộc hiện có hợp lệ."""
        return all(
            isinstance(gia_tri, str) and bool(gia_tri.strip())
            for gia_tri in (self.ma_hanh_khach, self.ma_dat_tour, self.ho_ten)
        )
