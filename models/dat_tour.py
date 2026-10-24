"""Domain class representing a tour booking for a specific departure."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal


CHO_XAC_NHAN = "CHO_XAC_NHAN"
DA_XAC_NHAN = "DA_XAC_NHAN"
DA_HUY = "DA_HUY"

TRANG_THAI_HOP_LE = {CHO_XAC_NHAN, DA_XAC_NHAN, DA_HUY}


class DatTour:
    """Đại diện 01 đơn đặt cho 01 đợt khởi hành."""

    CHO_XAC_NHAN = CHO_XAC_NHAN
    DA_XAC_NHAN = DA_XAC_NHAN
    DA_HUY = DA_HUY

    TRANG_THAI_HOP_LE = (CHO_XAC_NHAN, DA_XAC_NHAN, DA_HUY)
    QUY_TAC_CHUYEN_TRANG_THAI: dict[str, tuple[str, ...]] = {
        CHO_XAC_NHAN: (DA_XAC_NHAN, DA_HUY),
        DA_XAC_NHAN: (DA_HUY,),
        DA_HUY: (),
    }

    def __init__(
        self,
        ma_dat_tour: str,
        ma_nguoi_dung: str,
        ma_dot_khoi_hanh: str,
        ngay_dat: datetime,
        so_nguoi: int,
        don_gia_da_chot: Decimal,
        trang_thai: str = CHO_XAC_NHAN,
        han_giu_cho: datetime | None = None,
    ) -> None:
        self.ma_dat_tour: str = self._kiem_tra_chuoi_bat_buoc(
            ma_dat_tour, "Mã đặt tour"
        )
        self.ma_nguoi_dung: str = self._kiem_tra_chuoi_bat_buoc(
            ma_nguoi_dung, "Mã người dùng"
        )
        self.ma_dot_khoi_hanh: str = self._kiem_tra_chuoi_bat_buoc(
            ma_dot_khoi_hanh, "Mã đợt khởi hành"
        )
        self.ngay_dat: datetime = self._kiem_tra_ngay_gio(ngay_dat, "Ngày đặt")
        self.so_nguoi: int = self._kiem_tra_so_nguoi(so_nguoi)
        self.don_gia_da_chot: Decimal = self._kiem_tra_so_tien(
            don_gia_da_chot, "Đơn giá đã chốt"
        )
        self.trang_thai: str = self._kiem_tra_trang_thai(trang_thai)
        self.han_giu_cho: datetime | None = (
            None
            if han_giu_cho is None
            else self._kiem_tra_ngay_gio(han_giu_cho, "Hạn giữ chỗ")
        )
        if self.han_giu_cho is not None and self.han_giu_cho < self.ngay_dat:
            raise ValueError("Hạn giữ chỗ không được trước ngày đặt.")
        self.tong_tien: Decimal = self.tinh_tong_tien()

    @staticmethod
    def _kiem_tra_chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _kiem_tra_ngay_gio(gia_tri: datetime, ten_truong: str) -> datetime:
        if not isinstance(gia_tri, datetime):
            raise ValueError(f"{ten_truong} phải là datetime.")
        return gia_tri

    @staticmethod
    def _kiem_tra_so_nguoi(so_nguoi: int) -> int:
        if isinstance(so_nguoi, bool) or not isinstance(so_nguoi, int):
            raise ValueError("Số người phải là số nguyên (int).")
        if so_nguoi <= 0:
            raise ValueError("Số người phải lớn hơn 0.")
        return so_nguoi

    @staticmethod
    def _kiem_tra_so_tien(so_tien: Decimal, ten_truong: str) -> Decimal:
        if not isinstance(so_tien, Decimal):
            raise ValueError(f"{ten_truong} phải có kiểu decimal.Decimal.")
        if so_tien.is_nan() or so_tien.is_infinite() or so_tien <= Decimal("0"):
            raise ValueError(f"{ten_truong} phải lớn hơn 0.")
        return so_tien

    @classmethod
    def _kiem_tra_trang_thai(cls, trang_thai: str) -> str:
        trang_thai_hop_le = cls._kiem_tra_chuoi_bat_buoc(
            trang_thai, "Trạng thái"
        ).upper()
        if trang_thai_hop_le not in cls.TRANG_THAI_HOP_LE:
            raise ValueError(
                f"Trạng thái không hợp lệ: {trang_thai_hop_le}. "
                f"Chỉ chấp nhận: {', '.join(cls.TRANG_THAI_HOP_LE)}."
            )
        return trang_thai_hop_le

    def tinh_tong_tien(self) -> Decimal:
        """Tính tổng tiền của đơn đặt tour theo số người và đơn giá đã chốt."""
        return Decimal(self.so_nguoi) * self.don_gia_da_chot

    def kiem_tra_so_luong_hanh_khach(self, so_hanh_khach: int) -> bool:
        """Kiểm tra số lượng hành khách có khớp với so_nguoi của đơn đặt tour không."""
        if isinstance(so_hanh_khach, bool) or not isinstance(so_hanh_khach, int):
            raise ValueError("Số hành khách phải là số nguyên (int).")
        return so_hanh_khach == self.so_nguoi

    def co_the_huy(self) -> bool:
        """Kiểm tra điều kiện trạng thái tối thiểu xem đơn có thể hủy hay không."""
        return self.DA_HUY in self.QUY_TAC_CHUYEN_TRANG_THAI.get(self.trang_thai, ())

    def chuyen_trang_thai(self, trang_thai_moi: str) -> None:
        """Chuyển trạng thái đơn đặt tour theo quy tắc tối thiểu."""
        trang_thai_dich = self._kiem_tra_trang_thai(trang_thai_moi)
        cac_trang_thai_cho_phep = self.QUY_TAC_CHUYEN_TRANG_THAI.get(
            self.trang_thai, ()
        )
        if trang_thai_dich not in cac_trang_thai_cho_phep:
            raise ValueError(
                f"Không thể chuyển trạng thái từ {self.trang_thai} sang {trang_thai_dich}."
            )
        self.trang_thai = trang_thai_dich


if __name__ == "__main__":
    thoi_diem_dat = datetime(2026, 10, 24, 9, 0, 0)
    don_dat = DatTour(
        ma_dat_tour="DT001",
        ma_nguoi_dung="ND001",
        ma_dot_khoi_hanh="DKH001",
        ngay_dat=thoi_diem_dat,
        so_nguoi=3,
        don_gia_da_chot=Decimal("2000000"),
    )
    assert don_dat.tong_tien == Decimal("6000000")
    assert don_dat.kiem_tra_so_luong_hanh_khach(3) is True
    assert don_dat.kiem_tra_so_luong_hanh_khach(2) is False
    assert don_dat.co_the_huy() is True

    don_dat.chuyen_trang_thai(DatTour.DA_XAC_NHAN)
    assert don_dat.trang_thai == DatTour.DA_XAC_NHAN
    assert don_dat.co_the_huy() is True

    don_dat.chuyen_trang_thai(DatTour.DA_HUY)
    assert don_dat.trang_thai == DatTour.DA_HUY
    assert don_dat.co_the_huy() is False

    try:
        don_dat.chuyen_trang_thai(DatTour.DA_XAC_NHAN)
        raise AssertionError("Đơn DA_HUY không được chuyển ngược sang DA_XAC_NHAN.")
    except ValueError:
        pass

    for so_nguoi_sai, gia_sai in [(0, Decimal("2000000")), (2, Decimal("-1000"))]:
        try:
            DatTour(
                ma_dat_tour="DT002",
                ma_nguoi_dung="ND001",
                ma_dot_khoi_hanh="DKH001",
                ngay_dat=thoi_diem_dat,
                so_nguoi=so_nguoi_sai,
                don_gia_da_chot=gia_sai,
            )
            raise AssertionError("Dữ liệu không hợp lệ phải raise ValueError.")
        except ValueError:
            pass
