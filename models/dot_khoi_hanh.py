"""Domain class đại diện một đợt khởi hành cụ thể của tour."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal


class DotKhoiHanh:
    """Quản lý ngày đi/về, giá, sức chứa và trạng thái mở bán của một đợt.

    Class được tiếp nhận bảo trì từ mã hiện hữu (giữ nguyên thuộc tính,
    trạng thái và phương thức). Class không tự đọc danh sách DatTour:
    so_cho_da_chiem do lớp quản lý nghiệp vụ tính rồi truyền vào. Việc đếm
    đơn CHO_XAC_NHAN hay chỉ DA_XAC_NHAN là quy tắc cần chốt khi tích hợp.
    """

    MO_BAN = "MO_BAN"
    DONG_BAN = "DONG_BAN"
    DA_HUY = "DA_HUY"
    TRANG_THAI_HOP_LE = (MO_BAN, DONG_BAN, DA_HUY)

    def __init__(
        self,
        ma_dot_khoi_hanh: str,
        ma_tour: str,
        ngay_di: datetime,
        ngay_ve: datetime,
        gia_ap_dung: Decimal,
        suc_chua: int,
        trang_thai: str = MO_BAN,
    ) -> None:
        self.ma_dot_khoi_hanh: str = self._chuoi_bat_buoc(ma_dot_khoi_hanh, "Mã đợt khởi hành")
        self.ma_tour: str = self._chuoi_bat_buoc(ma_tour, "Mã tour")
        self._kiem_tra_ngay(ngay_di, ngay_ve)
        self.ngay_di: datetime = ngay_di
        self.ngay_ve: datetime = ngay_ve
        self.gia_ap_dung: Decimal = self._kiem_tra_gia(gia_ap_dung)
        self.suc_chua: int = self._kiem_tra_suc_chua(suc_chua)
        self.trang_thai: str = self._kiem_tra_trang_thai(trang_thai)

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _kiem_tra_ngay(ngay_di: datetime, ngay_ve: datetime) -> None:
        if not isinstance(ngay_di, datetime) or not isinstance(ngay_ve, datetime):
            raise ValueError("Ngày đi và ngày về phải có kiểu datetime.")
        if (ngay_di.tzinfo is None) != (ngay_ve.tzinfo is None):
            raise ValueError("Ngày đi và về phải dùng cùng kiểu múi giờ.")
        try:
            if ngay_ve <= ngay_di:
                raise ValueError("Ngày về phải sau ngày đi.")
        except TypeError as exc:
            raise ValueError("Ngày đi và ngày về không cùng hệ múi giờ.") from exc

    @staticmethod
    def _kiem_tra_gia(gia: Decimal) -> Decimal:
        if not isinstance(gia, Decimal) or not gia.is_finite() or gia <= Decimal("0"):
            raise ValueError("Giá áp dụng phải là Decimal dương, hữu hạn.")
        return gia

    @staticmethod
    def _kiem_tra_suc_chua(suc_chua: int) -> int:
        if isinstance(suc_chua, bool) or not isinstance(suc_chua, int) or suc_chua <= 0:
            raise ValueError("Sức chứa phải là số nguyên dương.")
        return suc_chua

    @classmethod
    def _kiem_tra_trang_thai(cls, trang_thai: str) -> str:
        ket_qua = cls._chuoi_bat_buoc(trang_thai, "Trạng thái").upper()
        if ket_qua not in cls.TRANG_THAI_HOP_LE:
            raise ValueError("Trạng thái đợt khởi hành không hợp lệ.")
        return ket_qua

    def kiem_tra_ngay_hop_le(self) -> bool:
        try:
            self._kiem_tra_ngay(self.ngay_di, self.ngay_ve)
            return True
        except ValueError:
            return False

    def co_dang_mo_ban(self) -> bool:
        return self.trang_thai == self.MO_BAN

    def so_cho_con_lai(self, so_cho_da_chiem: int) -> int:
        """Tính từ các đơn còn hiệu lực do tầng nghiệp vụ truy xuất."""
        if isinstance(so_cho_da_chiem, bool) or not isinstance(so_cho_da_chiem, int):
            raise ValueError("Số chỗ đã chiếm phải là số nguyên.")
        if not 0 <= so_cho_da_chiem <= self.suc_chua:
            raise ValueError("Số chỗ đã chiếm không hợp lệ với sức chứa.")
        return self.suc_chua - so_cho_da_chiem

    def co_du_cho(self, so_nguoi: int, so_cho_da_chiem: int) -> bool:
        if isinstance(so_nguoi, bool) or not isinstance(so_nguoi, int) or so_nguoi <= 0:
            raise ValueError("Số người phải là số nguyên dương.")
        cho_con_lai = self.so_cho_con_lai(so_cho_da_chiem)
        return self.co_dang_mo_ban() and cho_con_lai >= so_nguoi

    def cap_nhat_gia(self, gia_moi: Decimal) -> None:
        """Chỉ cập nhật giá đợt; không thay đổi đơn giá đã chốt ở DatTour."""
        if self.trang_thai == self.DA_HUY:
            raise ValueError("Không thể cập nhật giá đợt đã hủy.")
        self.gia_ap_dung = self._kiem_tra_gia(gia_moi)

    def cap_nhat_suc_chua(self, suc_chua_moi: int, so_cho_da_chiem: int) -> None:
        """Không được giảm sức chứa xuống thấp hơn số chỗ đang chiếm."""
        if self.trang_thai == self.DA_HUY:
            raise ValueError("Không thể thay đổi sức chứa đợt đã hủy.")
        suc_chua_hop_le = self._kiem_tra_suc_chua(suc_chua_moi)
        if isinstance(so_cho_da_chiem, bool) or not isinstance(so_cho_da_chiem, int) or so_cho_da_chiem < 0:
            raise ValueError("Số chỗ đã chiếm phải là số nguyên không âm.")
        if suc_chua_hop_le < so_cho_da_chiem:
            raise ValueError("Sức chứa mới không đủ cho các chỗ đã đặt.")
        self.suc_chua = suc_chua_hop_le

    def dong_mo_ban(self) -> None:
        if self.trang_thai != self.MO_BAN:
            raise ValueError("Chỉ có thể đóng bán đợt đang mở bán.")
        self.trang_thai = self.DONG_BAN

    def mo_ban(self) -> None:
        if self.trang_thai != self.DONG_BAN:
            raise ValueError("Chỉ có thể mở bán lại đợt đang đóng bán.")
        self.trang_thai = self.MO_BAN

    def huy_dot_khoi_hanh(self) -> None:
        """Chỉ đổi trạng thái; hủy các đơn liên quan do tầng nghiệp vụ điều phối."""
        if self.trang_thai == self.DA_HUY:
            raise ValueError("Đợt khởi hành đã bị hủy.")
        self.trang_thai = self.DA_HUY
