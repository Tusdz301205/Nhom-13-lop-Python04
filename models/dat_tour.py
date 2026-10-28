"""Domain class representing a tour booking for a specific departure."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from decimal import Decimal
from typing import Iterable

from models.dich_vu_dat_tour import DichVuDatTour


CHO_XAC_NHAN = "CHO_XAC_NHAN"
DA_XAC_NHAN = "DA_XAC_NHAN"
DA_HUY = "DA_HUY"

TRANG_THAI_HOP_LE = {CHO_XAC_NHAN, DA_XAC_NHAN, DA_HUY}


class DatTour:
    """Đại diện 01 đơn đặt cho 01 đợt khởi hành.

    Giá tour và giá dịch vụ đều được chốt trong đơn (don_gia_da_chot và
    DichVuDatTour.don_gia_da_chot), nên đổi giá DotKhoiHanh hoặc DichVu sau
    này không làm thay đổi đơn. tong_tien luôn được tính lại từ dữ liệu
    hiện tại, không lưu một con số có thể lệch.
    Giá trị đơn không đồng nghĩa với số tiền đã thu.
    """

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
        danh_sach_dich_vu: Iterable[DichVuDatTour] | None = None,
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
        # Giữ trường cũ; chưa có logic giữ chỗ theo thời gian (chính sách chưa chốt).
        self.han_giu_cho: datetime | None = (
            None
            if han_giu_cho is None
            else self._kiem_tra_ngay_gio(han_giu_cho, "Hạn giữ chỗ")
        )
        if self.han_giu_cho is not None:
            try:
                truoc_ngay_dat = self.han_giu_cho < self.ngay_dat
            except TypeError as exc:
                raise ValueError(
                    "Hạn giữ chỗ và ngày đặt phải cùng kiểu múi giờ."
                ) from exc
            if truoc_ngay_dat:
                raise ValueError("Hạn giữ chỗ không được trước ngày đặt.")

        self._danh_sach_dich_vu: list[DichVuDatTour] = []
        if danh_sach_dich_vu is not None:
            for chi_tiet in danh_sach_dich_vu:
                self._kiem_tra_chi_tiet_moi(chi_tiet)
                self._danh_sach_dich_vu.append(deepcopy(chi_tiet))

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

    # ----- Quản lý dịch vụ đã chọn -----

    def _kiem_tra_co_the_sua_dich_vu(self) -> None:
        # Điểm cần nhóm xác nhận: đơn DA_XAC_NHAN có được đổi dịch vụ không.
        if self.trang_thai == self.DA_HUY:
            raise ValueError("Không thể thay đổi dịch vụ của đơn đã hủy.")

    def _tim_vi_tri_dich_vu(self, ma_dich_vu: str) -> int | None:
        for vi_tri, chi_tiet in enumerate(self._danh_sach_dich_vu):
            if chi_tiet.ma_dich_vu == ma_dich_vu:
                return vi_tri
        return None

    def _kiem_tra_chi_tiet_moi(self, chi_tiet: DichVuDatTour) -> None:
        if not isinstance(chi_tiet, DichVuDatTour):
            raise ValueError("Chi tiết dịch vụ phải là DichVuDatTour.")
        if chi_tiet.ma_dat_tour != self.ma_dat_tour:
            raise ValueError("Chi tiết dịch vụ không thuộc đơn đặt tour này.")
        if self._tim_vi_tri_dich_vu(chi_tiet.ma_dich_vu) is not None:
            raise ValueError(
                "Dịch vụ đã có trong đơn; hãy cập nhật số lượng thay vì thêm dòng mới."
            )

    @property
    def danh_sach_dich_vu(self) -> tuple[DichVuDatTour, ...]:
        """Trả về bản sao, không cho caller sửa ngầm danh sách nội bộ."""
        return tuple(deepcopy(self._danh_sach_dich_vu))

    def lay_danh_sach_dich_vu(self) -> tuple[DichVuDatTour, ...]:
        return self.danh_sach_dich_vu

    def them_dich_vu(self, chi_tiet: DichVuDatTour) -> None:
        self._kiem_tra_co_the_sua_dich_vu()
        self._kiem_tra_chi_tiet_moi(chi_tiet)
        self._danh_sach_dich_vu.append(deepcopy(chi_tiet))

    def cap_nhat_dich_vu(self, ma_dich_vu: str, so_luong_moi: int) -> None:
        """Đổi số lượng của dịch vụ đã chọn; giữ nguyên đơn giá đã chốt."""
        self._kiem_tra_co_the_sua_dich_vu()
        ma_hop_le = self._kiem_tra_chuoi_bat_buoc(ma_dich_vu, "Mã dịch vụ")
        vi_tri = self._tim_vi_tri_dich_vu(ma_hop_le)
        if vi_tri is None:
            raise ValueError("Không tìm thấy dịch vụ trong đơn để cập nhật.")
        self._danh_sach_dich_vu[vi_tri].cap_nhat_so_luong(so_luong_moi)

    def xoa_dich_vu(self, ma_dich_vu: str) -> None:
        self._kiem_tra_co_the_sua_dich_vu()
        ma_hop_le = self._kiem_tra_chuoi_bat_buoc(ma_dich_vu, "Mã dịch vụ")
        vi_tri = self._tim_vi_tri_dich_vu(ma_hop_le)
        if vi_tri is None:
            raise ValueError("Không tìm thấy dịch vụ trong đơn để xóa.")
        del self._danh_sach_dich_vu[vi_tri]

    # ----- Tính tiền -----

    def tinh_tong_tien(self) -> Decimal:
        """so_nguoi × don_gia_da_chot + tổng thành tiền các dịch vụ đã chọn."""
        tien_tour = Decimal(self.so_nguoi) * self.don_gia_da_chot
        tien_dich_vu = sum(
            (chi_tiet.tinh_thanh_tien() for chi_tiet in self._danh_sach_dich_vu),
            Decimal("0"),
        )
        return tien_tour + tien_dich_vu

    @property
    def tong_tien(self) -> Decimal:
        """Luôn tính từ dữ liệu hiện tại; chỉ đọc."""
        return self.tinh_tong_tien()

    # ----- Hành khách và trạng thái -----

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
