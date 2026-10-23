"""Domain class tracking a request to cancel a tour booking."""

from __future__ import annotations

from datetime import datetime


TRANG_THAI_HOP_LE = {"CHO_XU_LY", "CHAP_NHAN", "TU_CHOI"}


class YeuCauHuy:
    """Theo dõi yêu cầu hủy đơn và kết quả xử lý."""

    def __init__(
        self,
        ma_yeu_cau: str,
        ma_dat_tour: str,
        ly_do: str,
        thoi_diem_yeu_cau: datetime,
        trang_thai: str = "CHO_XU_LY",
        ma_nguoi_xu_ly: str | None = None,
        thoi_diem_xu_ly: datetime | None = None,
        ly_do_tu_choi: str | None = None,
    ) -> None:
        self.ma_yeu_cau = self._chuoi_bat_buoc(ma_yeu_cau, "Mã yêu cầu")
        self.ma_dat_tour = self._chuoi_bat_buoc(ma_dat_tour, "Mã đặt tour")
        self.ly_do = self._chuoi_bat_buoc(ly_do, "Lý do yêu cầu")
        if not isinstance(thoi_diem_yeu_cau, datetime):
            raise ValueError("Thời điểm yêu cầu phải là datetime.")
        self.thoi_diem_yeu_cau = thoi_diem_yeu_cau
        self.trang_thai = self._kiem_tra_trang_thai(trang_thai)
        self.ma_nguoi_xu_ly = self._chuoi_tuy_chon(ma_nguoi_xu_ly, "Mã người xử lý")
        if thoi_diem_xu_ly is not None and not isinstance(thoi_diem_xu_ly, datetime):
            raise ValueError("Thời điểm xử lý phải là datetime hoặc None.")
        self.thoi_diem_xu_ly = thoi_diem_xu_ly
        self.ly_do_tu_choi = self._chuoi_tuy_chon(ly_do_tu_choi, "Lý do từ chối")

        if self.trang_thai == "CHO_XU_LY":
            if any((self.ma_nguoi_xu_ly, self.thoi_diem_xu_ly, self.ly_do_tu_choi)):
                raise ValueError("Yêu cầu CHO_XU_LY chưa được có thông tin xử lý.")
        else:
            if not self.ma_nguoi_xu_ly or self.thoi_diem_xu_ly is None:
                raise ValueError("Yêu cầu đã xử lý phải có người và thời điểm xử lý.")
            if self.trang_thai == "TU_CHOI" and not self.ly_do_tu_choi:
                raise ValueError("Yêu cầu bị từ chối phải có lý do từ chối.")
            if self.trang_thai == "CHAP_NHAN" and self.ly_do_tu_choi:
                raise ValueError("Yêu cầu CHAP_NHAN không cần lý do từ chối.")

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
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

    @classmethod
    def _kiem_tra_trang_thai(cls, trang_thai: str) -> str:
        trang_thai = cls._chuoi_bat_buoc(trang_thai, "Trạng thái").upper()
        if trang_thai not in TRANG_THAI_HOP_LE:
            cac_gia_tri = ", ".join(sorted(TRANG_THAI_HOP_LE))
            raise ValueError(f"Trạng thái không hợp lệ. Chọn một trong: {cac_gia_tri}.")
        return trang_thai

    def dang_cho_xu_ly(self) -> bool:
        return self.trang_thai == "CHO_XU_LY"

    def _kiem_tra_co_the_xu_ly(self, ma_nguoi_xu_ly: str, thoi_diem_xu_ly: datetime) -> tuple[str, datetime]:
        if not self.dang_cho_xu_ly():
            raise ValueError("Yêu cầu này đã được xử lý, không thể xử lý lần nữa.")
        ma_nguoi_xu_ly = self._chuoi_bat_buoc(ma_nguoi_xu_ly, "Mã người xử lý")
        if not isinstance(thoi_diem_xu_ly, datetime):
            raise ValueError("Thời điểm xử lý phải là datetime.")
        if thoi_diem_xu_ly < self.thoi_diem_yeu_cau:
            raise ValueError("Thời điểm xử lý không được trước thời điểm yêu cầu.")
        return ma_nguoi_xu_ly, thoi_diem_xu_ly

    def chap_nhan(self, ma_nguoi_xu_ly: str, thoi_diem_xu_ly: datetime) -> None:
        """Chấp nhận yêu cầu hủy; không tự thay đổi trạng thái đơn đặt tour."""
        ma_nguoi_xu_ly, thoi_diem_xu_ly = self._kiem_tra_co_the_xu_ly(
            ma_nguoi_xu_ly, thoi_diem_xu_ly
        )
        self.trang_thai = "CHAP_NHAN"
        self.ma_nguoi_xu_ly = ma_nguoi_xu_ly
        self.thoi_diem_xu_ly = thoi_diem_xu_ly
        self.ly_do_tu_choi = None

    def tu_choi(
        self,
        ma_nguoi_xu_ly: str,
        thoi_diem_xu_ly: datetime,
        ly_do_tu_choi: str,
    ) -> None:
        """Từ chối yêu cầu hủy và lưu lý do từ chối."""
        ly_do_tu_choi = self._chuoi_bat_buoc(ly_do_tu_choi, "Lý do từ chối")
        ma_nguoi_xu_ly, thoi_diem_xu_ly = self._kiem_tra_co_the_xu_ly(
            ma_nguoi_xu_ly, thoi_diem_xu_ly
        )
        self.trang_thai = "TU_CHOI"
        self.ma_nguoi_xu_ly = ma_nguoi_xu_ly
        self.thoi_diem_xu_ly = thoi_diem_xu_ly
        self.ly_do_tu_choi = ly_do_tu_choi
