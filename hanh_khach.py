"""Domain class đại diện một hành khách trong đơn đặt tour."""

from __future__ import annotations
import re

_REGEX_SO_DIEN_THOAI = re.compile(r"^(?:0[35789]\d{8}|\\+84[35789]\d{8})$")


class HanhKhach:
    """Đại diện người thực sự tham gia tour, không nhất thiết là người đặt tour."""

    def __init__(self, ma_hanh_khach: str, ma_dat_tour: str, ho_ten: str,
                 so_dien_thoai: str | None = None) -> None:
        ma_hk = self._chuoi_bat_buoc(ma_hanh_khach, "Mã hành khách")
        ma_dat = self._chuoi_bat_buoc(ma_dat_tour, "Mã đặt tour")
        ten = self._chuoi_bat_buoc(ho_ten, "Họ tên")
        dien_thoai = self._so_dien_thoai_tuy_chon(so_dien_thoai)
        self.ma_hanh_khach = ma_hk
        self.ma_dat_tour = ma_dat
        self.ho_ten = ten
        self.so_dien_thoai = dien_thoai

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} phải là chuỗi và không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _so_dien_thoai_tuy_chon(gia_tri: str | None) -> str | None:
        if gia_tri is None:
            return None
        if not isinstance(gia_tri, str):
            raise ValueError("Số điện thoại phải là chuỗi hoặc None.")
        gia_tri = gia_tri.strip()
        if not gia_tri:
            return None
        if not _REGEX_SO_DIEN_THOAI.fullmatch(gia_tri):
            raise ValueError("Số điện thoại không đúng định dạng Việt Nam.")
        return gia_tri

    def cap_nhat_thong_tin(self, ho_ten: str | None = None,
                           so_dien_thoai: str | None = None) -> None:
        ten_moi = self.ho_ten if ho_ten is None else self._chuoi_bat_buoc(ho_ten, "Họ tên")
        dien_thoai_moi = self.so_dien_thoai if so_dien_thoai is None else self._so_dien_thoai_tuy_chon(so_dien_thoai)
        self.ho_ten, self.so_dien_thoai = ten_moi, dien_thoai_moi

    def kiem_tra_hop_le(self) -> bool:
        return (isinstance(self.ma_hanh_khach, str) and bool(self.ma_hanh_khach.strip())
                and isinstance(self.ma_dat_tour, str) and bool(self.ma_dat_tour.strip())
                and isinstance(self.ho_ten, str) and bool(self.ho_ten.strip()))
