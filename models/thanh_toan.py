"""Domain class recording a payment transaction for a tour booking."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal


TIEN_MAT = "TIEN_MAT"
CHUYEN_KHOAN = "CHUYEN_KHOAN"
PHUONG_THUC_HOP_LE = {TIEN_MAT, CHUYEN_KHOAN}

CHO_XAC_MINH = "CHO_XAC_MINH"
THANH_CONG = "THANH_CONG"
THAT_BAI = "THAT_BAI"
TRANG_THAI_HOP_LE = {CHO_XAC_MINH, THANH_CONG, THAT_BAI}


class ThanhToan:
    """Ghi nhận 01 giao dịch thanh toán cho 01 đơn đặt tour."""

    TIEN_MAT = TIEN_MAT
    CHUYEN_KHOAN = CHUYEN_KHOAN
    PHUONG_THUC_HOP_LE = (TIEN_MAT, CHUYEN_KHOAN)

    CHO_XAC_MINH = CHO_XAC_MINH
    THANH_CONG = THANH_CONG
    THAT_BAI = THAT_BAI
    TRANG_THAI_HOP_LE = (CHO_XAC_MINH, THANH_CONG, THAT_BAI)

    def __init__(
        self,
        ma_thanh_toan: str,
        ma_dat_tour: str,
        so_tien: Decimal,
        phuong_thuc: str,
        thoi_diem_tao: datetime,
        trang_thai: str = CHO_XAC_MINH,
        ma_giao_dich_tham_chieu: str | None = None,
        thoi_diem_xac_minh: datetime | None = None,
    ) -> None:
        self.ma_thanh_toan: str = self._kiem_tra_chuoi_bat_buoc(
            ma_thanh_toan, "Mã thanh toán"
        )
        self.ma_dat_tour: str = self._kiem_tra_chuoi_bat_buoc(
            ma_dat_tour, "Mã đặt tour"
        )
        self.so_tien: Decimal = self._kiem_tra_so_tien(so_tien, "Số tiền")
        self.phuong_thuc: str = self._kiem_tra_phuong_thuc(phuong_thuc)
        self.thoi_diem_tao: datetime = self._kiem_tra_ngay_gio(
            thoi_diem_tao, "Thời điểm tạo"
        )
        self.trang_thai: str = self._kiem_tra_trang_thai(trang_thai)
        self.ma_giao_dich_tham_chieu: str | None = self._chuoi_tuy_chon(
            ma_giao_dich_tham_chieu, "Mã giao dịch tham chiếu"
        )
        self.thoi_diem_xac_minh: datetime | None = (
            None
            if thoi_diem_xac_minh is None
            else self._kiem_tra_ngay_gio(thoi_diem_xac_minh, "Thời điểm xác minh")
        )
        if self.trang_thai == self.CHO_XAC_MINH:
            if self.thoi_diem_xac_minh is not None:
                raise ValueError(
                    "Giao dịch CHO_XAC_MINH chưa được có thời điểm xác minh."
                )
        else:
            if self.thoi_diem_xac_minh is None:
                raise ValueError(
                    "Giao dịch đã xác minh phải có thời điểm xác minh."
                )
            if self.thoi_diem_xac_minh < self.thoi_diem_tao:
                raise ValueError(
                    "Thời điểm xác minh không được trước thời điểm tạo."
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
    def _kiem_tra_phuong_thuc(cls, phuong_thuc: str) -> str:
        phuong_thuc_hop_le = cls._kiem_tra_chuoi_bat_buoc(
            phuong_thuc, "Phương thức"
        ).upper()
        if phuong_thuc_hop_le not in cls.PHUONG_THUC_HOP_LE:
            raise ValueError(
                f"Phương thức không hợp lệ: {phuong_thuc_hop_le}. "
                f"Chỉ chấp nhận: {', '.join(cls.PHUONG_THUC_HOP_LE)}."
            )
        return phuong_thuc_hop_le

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

    def xac_nhan_thanh_cong(self, thoi_diem_xac_minh: datetime) -> None:
        """Xác nhận giao dịch thanh toán thành công một lần duy nhất từ CHO_XAC_MINH."""
        if self.trang_thai != self.CHO_XAC_MINH:
            raise ValueError(
                f"Chỉ có thể xác nhận thành công khi giao dịch ở trạng thái "
                f"{self.CHO_XAC_MINH} (hiện tại: {self.trang_thai})."
            )
        thoi_diem_hop_le = self._kiem_tra_ngay_gio(
            thoi_diem_xac_minh, "Thời điểm xác minh"
        )
        if thoi_diem_hop_le < self.thoi_diem_tao:
            raise ValueError("Thời điểm xác minh không được trước thời điểm tạo.")
        self.thoi_diem_xac_minh = thoi_diem_hop_le
        self.trang_thai = self.THANH_CONG

    def danh_dau_that_bai(self, thoi_diem_xac_minh: datetime) -> None:
        """Đánh dấu giao dịch thanh toán thất bại một lần duy nhất từ CHO_XAC_MINH."""
        if self.trang_thai != self.CHO_XAC_MINH:
            raise ValueError(
                f"Chỉ có thể đánh dấu thất bại khi giao dịch ở trạng thái "
                f"{self.CHO_XAC_MINH} (hiện tại: {self.trang_thai})."
            )
        thoi_diem_hop_le = self._kiem_tra_ngay_gio(
            thoi_diem_xac_minh, "Thời điểm xác minh"
        )
        if thoi_diem_hop_le < self.thoi_diem_tao:
            raise ValueError("Thời điểm xác minh không được trước thời điểm tạo.")
        self.thoi_diem_xac_minh = thoi_diem_hop_le
        self.trang_thai = self.THAT_BAI

    def da_thanh_cong(self) -> bool:
        """Kiểm tra giao dịch đã được xác minh thành công hay chưa."""
        return self.trang_thai == self.THANH_CONG


if __name__ == "__main__":
    luc_tao = datetime(2026, 10, 24, 9, 0, 0)
    luc_xac_minh = datetime(2026, 10, 24, 9, 15, 0)

    giao_dich = ThanhToan(
        ma_thanh_toan="TT001",
        ma_dat_tour="DT001",
        so_tien=Decimal("6000000"),
        phuong_thuc=ThanhToan.CHUYEN_KHOAN,
        thoi_diem_tao=luc_tao,
        ma_giao_dich_tham_chieu="REF_DEMO_001",
    )
    assert giao_dich.trang_thai == ThanhToan.CHO_XAC_MINH
    assert giao_dich.da_thanh_cong() is False

    giao_dich.xac_nhan_thanh_cong(luc_xac_minh)
    assert giao_dich.trang_thai == ThanhToan.THANH_CONG
    assert giao_dich.da_thanh_cong() is True
    assert giao_dich.thoi_diem_xac_minh == luc_xac_minh

    try:
        giao_dich.xac_nhan_thanh_cong(luc_xac_minh)
        raise AssertionError("Xác nhận lần hai phải raise ValueError.")
    except ValueError:
        pass

    for so_tien_sai, phuong_thuc_sai in [
        (Decimal("0"), ThanhToan.TIEN_MAT),
        (Decimal("100000"), "THE_TIN_DUNG"),
    ]:
        try:
            ThanhToan(
                ma_thanh_toan="TT002",
                ma_dat_tour="DT001",
                so_tien=so_tien_sai,
                phuong_thuc=phuong_thuc_sai,
                thoi_diem_tao=luc_tao,
            )
            raise AssertionError("Dữ liệu không hợp lệ phải raise ValueError.")
        except ValueError:
            pass
