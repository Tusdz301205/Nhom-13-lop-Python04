"""Domain class recording a refund associated with a tour booking."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal


CHO_XU_LY = "CHO_XU_LY"
HOAN_TAT = "HOAN_TAT"
THAT_BAI = "THAT_BAI"
TRANG_THAI_HOP_LE = {CHO_XU_LY, HOAN_TAT, THAT_BAI}


class HoanTien:
    """Ghi nhận 01 khoản tiền hoàn lại liên quan đến đơn đặt tour."""

    CHO_XU_LY = CHO_XU_LY
    HOAN_TAT = HOAN_TAT
    THAT_BAI = THAT_BAI
    TRANG_THAI_HOP_LE = (CHO_XU_LY, HOAN_TAT, THAT_BAI)

    def __init__(
        self,
        ma_hoan_tien: str,
        ma_dat_tour: str,
        so_tien: Decimal,
        ly_do: str,
        thoi_diem_tao: datetime,
        trang_thai: str = CHO_XU_LY,
        ma_nguoi_xu_ly: str | None = None,
        thoi_diem_xu_ly: datetime | None = None,
    ) -> None:
        self.ma_hoan_tien: str = self._kiem_tra_chuoi_bat_buoc(
            ma_hoan_tien, "Mã hoàn tiền"
        )
        self.ma_dat_tour: str = self._kiem_tra_chuoi_bat_buoc(
            ma_dat_tour, "Mã đặt tour"
        )
        self.so_tien: Decimal = self._kiem_tra_so_tien(so_tien, "Số tiền hoàn")
        self.ly_do: str = self._kiem_tra_chuoi_bat_buoc(ly_do, "Lý do hoàn")
        self.thoi_diem_tao: datetime = self._kiem_tra_ngay_gio(
            thoi_diem_tao, "Thời điểm tạo"
        )
        self.trang_thai: str = self._kiem_tra_trang_thai(trang_thai)
        self.ma_nguoi_xu_ly: str | None = self._chuoi_tuy_chon(
            ma_nguoi_xu_ly, "Mã người xử lý"
        )
        self.thoi_diem_xu_ly: datetime | None = (
            None
            if thoi_diem_xu_ly is None
            else self._kiem_tra_ngay_gio(thoi_diem_xu_ly, "Thời điểm xử lý")
        )
        if self.trang_thai == self.CHO_XU_LY:
            if self.ma_nguoi_xu_ly is not None or self.thoi_diem_xu_ly is not None:
                raise ValueError(
                    "Khoản hoàn CHO_XU_LY chưa được có thông tin xử lý."
                )
        else:
            if not self.ma_nguoi_xu_ly or self.thoi_diem_xu_ly is None:
                raise ValueError(
                    "Khoản hoàn đã xử lý phải có người và thời điểm xử lý."
                )
            if self.thoi_diem_xu_ly < self.thoi_diem_tao:
                raise ValueError(
                    "Thời điểm xử lý không được trước thời điểm tạo."
                )

    @staticmethod
    def _kiem_tra_chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _chuoi_tuy_chon(gia_tri: str | None, ten_truong: str) -> str | None:
        if gia_tri is None:
            return None
        if not isinstance(gia_tri, str):
            raise ValueError(f"{ten_truong} phải là chuỗi hoặc None.")
        gia_tri = gia_tri.strip()
        return gia_tri or None

    @staticmethod
    def _kiem_tra_so_tien(so_tien: Decimal, ten_truong: str) -> Decimal:
        if not isinstance(so_tien, Decimal):
            raise ValueError(f"{ten_truong} phải có kiểu decimal.Decimal.")
        if so_tien.is_nan() or so_tien.is_infinite() or so_tien <= Decimal("0"):
            raise ValueError(f"{ten_truong} phải lớn hơn 0.")
        return so_tien

    @staticmethod
    def _kiem_tra_ngay_gio(gia_tri: datetime, ten_truong: str) -> datetime:
        if not isinstance(gia_tri, datetime):
            raise ValueError(f"{ten_truong} phải là datetime.")
        return gia_tri

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

    def xac_nhan_hoan_tat(
        self, ma_nguoi_xu_ly: str, thoi_diem_xu_ly: datetime
    ) -> None:
        """Xác nhận khoản hoàn tiền đã hoàn tất một lần duy nhất từ CHO_XU_LY."""
        if self.trang_thai != self.CHO_XU_LY:
            raise ValueError(
                f"Chỉ có thể xác nhận hoàn tất khi khoản hoàn ở trạng thái "
                f"{self.CHO_XU_LY} (hiện tại: {self.trang_thai})."
            )
        nguoi_xu_ly_hop_le = self._kiem_tra_chuoi_bat_buoc(
            ma_nguoi_xu_ly, "Mã người xử lý"
        )
        thoi_diem_hop_le = self._kiem_tra_ngay_gio(
            thoi_diem_xu_ly, "Thời điểm xử lý"
        )
        if thoi_diem_hop_le < self.thoi_diem_tao:
            raise ValueError("Thời điểm xử lý không được trước thời điểm tạo.")
        self.ma_nguoi_xu_ly = nguoi_xu_ly_hop_le
        self.thoi_diem_xu_ly = thoi_diem_hop_le
        self.trang_thai = self.HOAN_TAT

    def danh_dau_that_bai(
        self, ma_nguoi_xu_ly: str, thoi_diem_xu_ly: datetime
    ) -> None:
        """Đánh dấu khoản hoàn tiền thất bại một lần duy nhất từ CHO_XU_LY."""
        if self.trang_thai != self.CHO_XU_LY:
            raise ValueError(
                f"Chỉ có thể đánh dấu thất bại khi khoản hoàn ở trạng thái "
                f"{self.CHO_XU_LY} (hiện tại: {self.trang_thai})."
            )
        nguoi_xu_ly_hop_le = self._kiem_tra_chuoi_bat_buoc(
            ma_nguoi_xu_ly, "Mã người xử lý"
        )
        thoi_diem_hop_le = self._kiem_tra_ngay_gio(
            thoi_diem_xu_ly, "Thời điểm xử lý"
        )
        if thoi_diem_hop_le < self.thoi_diem_tao:
            raise ValueError("Thời điểm xử lý không được trước thời điểm tạo.")
        self.ma_nguoi_xu_ly = nguoi_xu_ly_hop_le
        self.thoi_diem_xu_ly = thoi_diem_hop_le
        self.trang_thai = self.THAT_BAI

    def da_hoan_tat(self) -> bool:
        """Kiểm tra khoản hoàn tiền đã hoàn tất hay chưa."""
        return self.trang_thai == self.HOAN_TAT


if __name__ == "__main__":
    luc_tao = datetime(2026, 10, 24, 10, 0, 0)
    luc_xu_ly = datetime(2026, 10, 24, 10, 30, 0)

    khoan_hoan = HoanTien(
        ma_hoan_tien="HT001",
        ma_dat_tour="DT001",
        so_tien=Decimal("3000000"),
        ly_do="Khách yêu cầu hủy đơn trước hạn",
        thoi_diem_tao=luc_tao,
    )
    assert khoan_hoan.trang_thai == HoanTien.CHO_XU_LY
    assert khoan_hoan.da_hoan_tat() is False
    assert khoan_hoan.ma_nguoi_xu_ly is None
    assert khoan_hoan.thoi_diem_xu_ly is None

    khoan_hoan.xac_nhan_hoan_tat("NV001", luc_xu_ly)
    assert khoan_hoan.trang_thai == HoanTien.HOAN_TAT
    assert khoan_hoan.da_hoan_tat() is True
    assert khoan_hoan.ma_nguoi_xu_ly == "NV001"
    assert khoan_hoan.thoi_diem_xu_ly == luc_xu_ly

    try:
        khoan_hoan.xac_nhan_hoan_tat("NV001", luc_xu_ly)
        raise AssertionError("Lặp thao tác hoàn tất phải raise ValueError.")
    except ValueError:
        pass

    for so_tien_sai, ly_do_sai in [
        (Decimal("-500000"), "Lý do hợp lệ"),
        (Decimal("500000"), "   "),
    ]:
        try:
            HoanTien(
                ma_hoan_tien="HT002",
                ma_dat_tour="DT001",
                so_tien=so_tien_sai,
                ly_do=ly_do_sai,
                thoi_diem_tao=luc_tao,
            )
            raise AssertionError("Dữ liệu không hợp lệ phải raise ValueError.")
        except ValueError:
            pass
