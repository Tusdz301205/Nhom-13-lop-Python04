"""Domain class theo dõi yêu cầu hủy đăng ký tour, không xử lý hoàn tiền."""

from __future__ import annotations
from datetime import datetime

TRANG_THAI_HOP_LE = {"CHO_XU_LY", "CHAP_NHAN", "TU_CHOI"}


class YeuCauHuy:
    """Lưu trạng thái và thông tin xử lý của một yêu cầu hủy."""

    def __init__(self, ma_yeu_cau: str, ma_dat_tour: str, ly_do: str,
                 thoi_diem_yeu_cau: datetime, trang_thai: str = "CHO_XU_LY",
                 ma_nguoi_xu_ly: str | None = None,
                 thoi_diem_xu_ly: datetime | None = None,
                 ly_do_tu_choi: str | None = None) -> None:
        ma_yc = self._chuoi_bat_buoc(ma_yeu_cau, "Mã yêu cầu")
        ma_dat = self._chuoi_bat_buoc(ma_dat_tour, "Mã đặt tour")
        ly_do_sach = self._chuoi_bat_buoc(ly_do, "Lý do yêu cầu")
        if not isinstance(thoi_diem_yeu_cau, datetime):
            raise ValueError("Thời điểm yêu cầu phải là datetime.")
        trang_thai_sach = self._kiem_tra_trang_thai(trang_thai)
        nguoi_xu_ly = self._chuoi_tuy_chon(ma_nguoi_xu_ly, "Mã người xử lý")
        if thoi_diem_xu_ly is not None and not isinstance(thoi_diem_xu_ly, datetime):
            raise ValueError("Thời điểm xử lý phải là datetime hoặc None.")
        ly_do_tu_choi_sach = self._chuoi_tuy_chon(ly_do_tu_choi, "Lý do từ chối")

        if trang_thai_sach == "CHO_XU_LY":
            if nguoi_xu_ly or thoi_diem_xu_ly is not None or ly_do_tu_choi_sach:
                raise ValueError("Yêu cầu CHO_XU_LY chưa được có thông tin xử lý.")
        else:
            if not nguoi_xu_ly or thoi_diem_xu_ly is None:
                raise ValueError("Yêu cầu đã xử lý phải có người và thời điểm xử lý.")
            self._kiem_tra_quan_he_thoi_gian(thoi_diem_yeu_cau, thoi_diem_xu_ly)
            if trang_thai_sach == "TU_CHOI" and not ly_do_tu_choi_sach:
                raise ValueError("Yêu cầu bị từ chối phải có lý do từ chối.")
            if trang_thai_sach == "CHAP_NHAN" and ly_do_tu_choi_sach:
                raise ValueError("Yêu cầu CHAP_NHAN không cần lý do từ chối.")

        self.ma_yeu_cau = ma_yc
        self.ma_dat_tour = ma_dat
        self.ly_do = ly_do_sach
        self.thoi_diem_yeu_cau = thoi_diem_yeu_cau
        self.trang_thai = trang_thai_sach
        self.ma_nguoi_xu_ly = nguoi_xu_ly
        self.thoi_diem_xu_ly = thoi_diem_xu_ly
        self.ly_do_tu_choi = ly_do_tu_choi_sach

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} phải là chuỗi và không được để trống.")
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
            raise ValueError("Trạng thái không hợp lệ. Chọn một trong: CHO_XU_LY, CHAP_NHAN, TU_CHOI.")
        return trang_thai

    @staticmethod
    def _kiem_tra_quan_he_thoi_gian(thoi_diem_yeu_cau: datetime,
                                   thoi_diem_xu_ly: datetime) -> None:
        try:
            if thoi_diem_xu_ly < thoi_diem_yeu_cau:
                raise ValueError("Thời điểm xử lý không được trước thời điểm yêu cầu.")
        except TypeError as exc:
            raise ValueError("Hai thời điểm phải cùng kiểu múi giờ (đều có hoặc đều không có timezone).") from exc

    def dang_cho_xu_ly(self) -> bool:
        return self.trang_thai == "CHO_XU_LY"

    def _kiem_tra_co_the_xu_ly(self, ma_nguoi_xu_ly: str,
                               thoi_diem_xu_ly: datetime) -> tuple[str, datetime]:
        if not self.dang_cho_xu_ly():
            raise ValueError("Yêu cầu này đã được xử lý, không thể xử lý lần nữa.")
        nguoi = self._chuoi_bat_buoc(ma_nguoi_xu_ly, "Mã người xử lý")
        if not isinstance(thoi_diem_xu_ly, datetime):
            raise ValueError("Thời điểm xử lý phải là datetime.")
        self._kiem_tra_quan_he_thoi_gian(self.thoi_diem_yeu_cau, thoi_diem_xu_ly)
        return nguoi, thoi_diem_xu_ly

    def chap_nhan(self, ma_nguoi_xu_ly: str, thoi_diem_xu_ly: datetime) -> None:
        """Chấp nhận yêu cầu hủy; không đổi trạng thái DatTour và không hoàn tiền."""
        nguoi, thoi_diem = self._kiem_tra_co_the_xu_ly(ma_nguoi_xu_ly, thoi_diem_xu_ly)
        self.trang_thai = "CHAP_NHAN"
        self.ma_nguoi_xu_ly = nguoi
        self.thoi_diem_xu_ly = thoi_diem
        self.ly_do_tu_choi = None

    def tu_choi(self, ma_nguoi_xu_ly: str, thoi_diem_xu_ly: datetime,
                ly_do_tu_choi: str) -> None:
        """Từ chối yêu cầu và lưu lý do từ chối."""
        ly_do = self._chuoi_bat_buoc(ly_do_tu_choi, "Lý do từ chối")
        nguoi, thoi_diem = self._kiem_tra_co_the_xu_ly(ma_nguoi_xu_ly, thoi_diem_xu_ly)
        self.trang_thai = "TU_CHOI"
        self.ma_nguoi_xu_ly = nguoi
        self.thoi_diem_xu_ly = thoi_diem
        self.ly_do_tu_choi = ly_do
