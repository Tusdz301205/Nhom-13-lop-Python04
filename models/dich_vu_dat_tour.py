"""Domain class đại diện một dịch vụ khách chọn trong một đơn đặt tour."""

from __future__ import annotations

from decimal import Decimal


class DichVuDatTour:
    """Một dòng dịch vụ trong đơn, nhận diện bằng cặp (ma_dat_tour, ma_dich_vu).

    don_gia_da_chot được sao chép từ DichVu tại thời điểm chọn, nên đổi giá
    danh mục sau đó không ảnh hưởng đơn này. Class không tự tìm DatTour hay
    DichVu; kiểm tra mã có tồn tại thuộc về lớp quản lý nghiệp vụ.
    Chưa áp dụng chính sách nhân theo số người hoặc giảm giá (chưa thống nhất).
    """

    def __init__(
        self,
        ma_dat_tour: str,
        ma_dich_vu: str,
        so_luong: int,
        don_gia_da_chot: Decimal,
    ) -> None:
        self._ma_dat_tour: str = self._chuoi_bat_buoc(ma_dat_tour, "Mã đặt tour")
        self._ma_dich_vu: str = self._chuoi_bat_buoc(ma_dich_vu, "Mã dịch vụ")
        self._so_luong: int = self._kiem_tra_so_luong(so_luong)
        self._don_gia_da_chot: Decimal = self._kiem_tra_don_gia(don_gia_da_chot)

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _kiem_tra_so_luong(so_luong: int) -> int:
        if isinstance(so_luong, bool) or not isinstance(so_luong, int) or so_luong <= 0:
            raise ValueError("Số lượng dịch vụ phải là số nguyên dương.")
        return so_luong

    @staticmethod
    def _kiem_tra_don_gia(don_gia: Decimal) -> Decimal:
        if (
            not isinstance(don_gia, Decimal)
            or not don_gia.is_finite()
            or don_gia < Decimal("0")
        ):
            raise ValueError("Đơn giá đã chốt phải là Decimal hữu hạn, không âm.")
        return don_gia

    # Khóa nghiệp vụ và giá đã chốt chỉ đọc để không bị sửa ngầm sau khi tạo.
    @property
    def ma_dat_tour(self) -> str:
        return self._ma_dat_tour

    @property
    def ma_dich_vu(self) -> str:
        return self._ma_dich_vu

    @property
    def so_luong(self) -> int:
        return self._so_luong

    @property
    def don_gia_da_chot(self) -> Decimal:
        return self._don_gia_da_chot

    def tinh_thanh_tien(self) -> Decimal:
        """Thành tiền = số lượng × đơn giá đã chốt."""
        return Decimal(self._so_luong) * self._don_gia_da_chot

    def cap_nhat_so_luong(self, so_luong_moi: int) -> None:
        self._so_luong = self._kiem_tra_so_luong(so_luong_moi)
