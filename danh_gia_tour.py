"""Domain class lưu đánh giá của một đơn đặt tour."""

from __future__ import annotations
from datetime import datetime


class DanhGiaTour:
    """Đánh giá sau chuyến đi; không tự truy cập các Domain Class khác."""

    def __init__(self, ma_danh_gia: str, ma_dat_tour: str, so_sao: int,
                 noi_dung: str, thoi_diem_danh_gia: datetime) -> None:
        ma_dg = self._chuoi_bat_buoc(ma_danh_gia, "Mã đánh giá")
        ma_dat = self._chuoi_bat_buoc(ma_dat_tour, "Mã đặt tour")
        sao = self._kiem_tra_so_sao(so_sao)
        if not isinstance(noi_dung, str):
            raise ValueError("Nội dung đánh giá phải là chuỗi.")
        if not isinstance(thoi_diem_danh_gia, datetime):
            raise ValueError("Thời điểm đánh giá phải là datetime.")
        self.ma_danh_gia = ma_dg
        self.ma_dat_tour = ma_dat
        self.so_sao = sao
        self.noi_dung = noi_dung.strip()
        self.thoi_diem_danh_gia = thoi_diem_danh_gia

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} phải là chuỗi và không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _kiem_tra_so_sao(so_sao: int) -> int:
        if isinstance(so_sao, bool) or not isinstance(so_sao, int) or not 1 <= so_sao <= 5:
            raise ValueError("Số sao phải là số nguyên từ 1 đến 5.")
        return so_sao

    def cap_nhat_noi_dung(self, noi_dung_moi: str) -> None:
        if not isinstance(noi_dung_moi, str):
            raise ValueError("Nội dung đánh giá phải là chuỗi.")
        self.noi_dung = noi_dung_moi.strip()

    def cap_nhat_so_sao(self, so_sao_moi: int) -> None:
        sao_moi = self._kiem_tra_so_sao(so_sao_moi)
        self.so_sao = sao_moi
