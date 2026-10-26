"""Domain class quản lý các hoạt động thuộc một lịch trình tour."""

from __future__ import annotations

from copy import deepcopy

from models.hoat_dong_lich_trinh import HoatDongLichTrinh


class LichTrinh:
    """Một lịch trình mặc định của tour, chứa nhiều hoạt động theo ngày/giờ."""

    def __init__(self, ma_lich_trinh: str, ma_tour: str) -> None:
        self.ma_lich_trinh: str = self._chuoi_bat_buoc(ma_lich_trinh, "Mã lịch trình")
        self.ma_tour: str = self._chuoi_bat_buoc(ma_tour, "Mã tour")
        self._danh_sach_hoat_dong: list[HoatDongLichTrinh] = []

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    def _kiem_tra_hoat_dong(self, hoat_dong: HoatDongLichTrinh) -> None:
        if not isinstance(hoat_dong, HoatDongLichTrinh):
            raise ValueError("Hoạt động phải là HoatDongLichTrinh.")
        # Đối tượng có thể đã bị gán lại thuộc tính sau constructor.
        self._chuoi_bat_buoc(hoat_dong.ma_hoat_dong, "Mã hoạt động")
        self._chuoi_bat_buoc(hoat_dong.dia_diem, "Địa điểm")
        self._chuoi_bat_buoc(hoat_dong.noi_dung, "Nội dung")
        if hoat_dong.ma_lich_trinh != self.ma_lich_trinh:
            raise ValueError("Hoạt động không thuộc lịch trình này.")
        if not hoat_dong.kiem_tra_thoi_gian_hop_le():
            raise ValueError("Thời gian hoạt động không hợp lệ.")

    @property
    def danh_sach_hoat_dong(self) -> tuple[HoatDongLichTrinh, ...]:
        """Trả về bản sao các hoạt động đã sắp xếp, không cho sửa ngầm dữ liệu nội bộ."""
        du_lieu = sorted(
            self._danh_sach_hoat_dong,
            key=lambda h: (h.ngay_thu, h.gio_bat_dau, h.ma_hoat_dong),
        )
        return tuple(deepcopy(du_lieu))

    def lay_danh_sach_hoat_dong(self) -> tuple[HoatDongLichTrinh, ...]:
        return self.danh_sach_hoat_dong

    def kiem_tra_trung_thoi_gian(
        self,
        hoat_dong: HoatDongLichTrinh,
        bo_qua_ma_hoat_dong: str | None = None,
    ) -> bool:
        """Trùng nếu hai hoạt động cùng ngày có khoảng giờ giao nhau."""
        self._kiem_tra_hoat_dong(hoat_dong)
        for hien_tai in self._danh_sach_hoat_dong:
            if hien_tai.ma_hoat_dong == bo_qua_ma_hoat_dong:
                continue
            if (
                hien_tai.ngay_thu == hoat_dong.ngay_thu
                and hoat_dong.gio_bat_dau < hien_tai.gio_ket_thuc
                and hoat_dong.gio_ket_thuc > hien_tai.gio_bat_dau
            ):
                return True
        return False

    def them_hoat_dong(self, hoat_dong: HoatDongLichTrinh) -> None:
        self._kiem_tra_hoat_dong(hoat_dong)
        if any(h.ma_hoat_dong == hoat_dong.ma_hoat_dong for h in self._danh_sach_hoat_dong):
            raise ValueError("Mã hoạt động đã tồn tại trong lịch trình.")
        if self.kiem_tra_trung_thoi_gian(hoat_dong):
            raise ValueError("Thời gian hoạt động bị trùng với hoạt động khác.")
        self._danh_sach_hoat_dong.append(deepcopy(hoat_dong))

    def sua_hoat_dong(self, hoat_dong_moi: HoatDongLichTrinh) -> None:
        """Thay thế hoạt động cùng mã chỉ khi dữ liệu mới hoàn toàn hợp lệ."""
        self._kiem_tra_hoat_dong(hoat_dong_moi)
        vi_tri = next(
            (i for i, h in enumerate(self._danh_sach_hoat_dong)
             if h.ma_hoat_dong == hoat_dong_moi.ma_hoat_dong),
            None,
        )
        if vi_tri is None:
            raise ValueError("Không tìm thấy hoạt động để sửa.")
        if self.kiem_tra_trung_thoi_gian(
            hoat_dong_moi, bo_qua_ma_hoat_dong=hoat_dong_moi.ma_hoat_dong
        ):
            raise ValueError("Thời gian mới bị trùng với hoạt động khác.")
        self._danh_sach_hoat_dong[vi_tri] = deepcopy(hoat_dong_moi)

    def xoa_hoat_dong(self, ma_hoat_dong: str) -> None:
        ma_hop_le = self._chuoi_bat_buoc(ma_hoat_dong, "Mã hoạt động")
        for vi_tri, hoat_dong in enumerate(self._danh_sach_hoat_dong):
            if hoat_dong.ma_hoat_dong == ma_hop_le:
                del self._danh_sach_hoat_dong[vi_tri]
                return
        raise ValueError("Không tìm thấy hoạt động để xóa.")
