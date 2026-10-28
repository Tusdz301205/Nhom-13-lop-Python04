"""Domain class đại diện một dịch vụ tùy chọn trong danh mục."""

from __future__ import annotations

from decimal import Decimal


class DichVu:
    """Danh mục dịch vụ tùy chọn khách có thể chọn thêm khi đặt tour.

    don_gia là giá niêm yết hiện tại. Giá đã chốt cho từng đơn được lưu tại
    DichVuDatTour, nên đổi giá ở đây không làm thay đổi các đơn đã đặt.
    """

    NGUOI = "NGUOI"
    LAN = "LAN"
    GOI = "GOI"
    DON_VI_TINH_HOP_LE = (NGUOI, LAN, GOI)

    DANG_CUNG_CAP = "DANG_CUNG_CAP"
    NGUNG_CUNG_CAP = "NGUNG_CUNG_CAP"
    TRANG_THAI_HOP_LE = (DANG_CUNG_CAP, NGUNG_CUNG_CAP)

    def __init__(
        self,
        ma_dich_vu: str,
        ten_dich_vu: str,
        don_gia: Decimal,
        don_vi_tinh: str,
        mo_ta: str = "",
        trang_thai: str = DANG_CUNG_CAP,
    ) -> None:
        self.ma_dich_vu: str = self._chuoi_bat_buoc(ma_dich_vu, "Mã dịch vụ")
        self.ten_dich_vu: str = self._chuoi_bat_buoc(ten_dich_vu, "Tên dịch vụ")
        self.mo_ta: str = self._kiem_tra_mo_ta(mo_ta)
        self.don_gia: Decimal = self._kiem_tra_don_gia(don_gia)
        self.don_vi_tinh: str = self._kiem_tra_don_vi_tinh(don_vi_tinh)
        self.trang_thai: str = self._kiem_tra_trang_thai(trang_thai)

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _kiem_tra_mo_ta(mo_ta: str) -> str:
        if not isinstance(mo_ta, str):
            raise ValueError("Mô tả dịch vụ phải là chuỗi.")
        return mo_ta.strip()

    @staticmethod
    def _kiem_tra_don_gia(don_gia: Decimal) -> Decimal:
        """Cho phép 0 (dịch vụ miễn phí) nhưng không cho âm hoặc không hữu hạn."""
        if (
            not isinstance(don_gia, Decimal)
            or not don_gia.is_finite()
            or don_gia < Decimal("0")
        ):
            raise ValueError("Đơn giá dịch vụ phải là Decimal hữu hạn, không âm.")
        return don_gia

    @classmethod
    def _kiem_tra_don_vi_tinh(cls, don_vi_tinh: str) -> str:
        ket_qua = cls._chuoi_bat_buoc(don_vi_tinh, "Đơn vị tính").upper()
        if ket_qua not in cls.DON_VI_TINH_HOP_LE:
            raise ValueError(
                "Đơn vị tính không hợp lệ. Chọn một trong: "
                f"{', '.join(cls.DON_VI_TINH_HOP_LE)}."
            )
        return ket_qua

    @classmethod
    def _kiem_tra_trang_thai(cls, trang_thai: str) -> str:
        ket_qua = cls._chuoi_bat_buoc(trang_thai, "Trạng thái").upper()
        if ket_qua not in cls.TRANG_THAI_HOP_LE:
            raise ValueError(
                "Trạng thái dịch vụ không hợp lệ. Chọn một trong: "
                f"{', '.join(cls.TRANG_THAI_HOP_LE)}."
            )
        return ket_qua

    def cap_nhat_thong_tin(
        self,
        ten_dich_vu: str | None = None,
        mo_ta: str | None = None,
        don_vi_tinh: str | None = None,
    ) -> None:
        """Kiểm tra toàn bộ trước khi cập nhật; None nghĩa là giữ nguyên."""
        ten_moi = (
            self.ten_dich_vu
            if ten_dich_vu is None
            else self._chuoi_bat_buoc(ten_dich_vu, "Tên dịch vụ")
        )
        mo_ta_moi = self.mo_ta if mo_ta is None else self._kiem_tra_mo_ta(mo_ta)
        don_vi_moi = (
            self.don_vi_tinh
            if don_vi_tinh is None
            else self._kiem_tra_don_vi_tinh(don_vi_tinh)
        )
        self.ten_dich_vu = ten_moi
        self.mo_ta = mo_ta_moi
        self.don_vi_tinh = don_vi_moi

    def cap_nhat_gia(self, gia_moi: Decimal) -> None:
        """Chỉ đổi giá danh mục; không thay đổi giá đã chốt ở DichVuDatTour."""
        self.don_gia = self._kiem_tra_don_gia(gia_moi)

    def dang_cung_cap(self) -> bool:
        return self.trang_thai == self.DANG_CUNG_CAP

    def ngung_cung_cap(self) -> None:
        """Ngừng cung cấp thay vì xóa để giữ lịch sử các đơn đã chọn dịch vụ."""
        if not self.dang_cung_cap():
            raise ValueError("Dịch vụ đã ngừng cung cấp.")
        self.trang_thai = self.NGUNG_CUNG_CAP
