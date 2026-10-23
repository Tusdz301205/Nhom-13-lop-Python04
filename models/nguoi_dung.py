"""Domain class representing a user account."""

from __future__ import annotations


VAI_TRO_HOP_LE = {"KHACH_HANG", "NHAN_VIEN", "QUAN_TRI_VIEN"}
TRANG_THAI_HOP_LE = {"HOAT_DONG", "KHOA"}


class NguoiDung:
    """Lưu thông tin tài khoản, vai trò và trạng thái người dùng."""

    def __init__(
        self,
        ma_nguoi_dung: str,
        ho_ten: str,
        email: str,
        so_dien_thoai: str,
        ten_dang_nhap: str,
        mat_khau_hash: str,
        vai_tro: str,
        trang_thai: str = "HOAT_DONG",
    ) -> None:
        self.ma_nguoi_dung = self._chuoi_bat_buoc(ma_nguoi_dung, "Mã người dùng")
        self.ho_ten = self._chuoi_bat_buoc(ho_ten, "Họ tên")
        self.email = self._chuoi_tuy_chon(email)
        self.so_dien_thoai = self._chuoi_tuy_chon(so_dien_thoai)
        self.ten_dang_nhap = self._chuoi_bat_buoc(ten_dang_nhap, "Tên đăng nhập")
        self.mat_khau_hash = self._chuoi_tuy_chon(mat_khau_hash)
        self.vai_tro = self._kiem_tra_lua_chon(vai_tro, VAI_TRO_HOP_LE, "Vai trò")
        self.trang_thai = self._kiem_tra_lua_chon(
            trang_thai, TRANG_THAI_HOP_LE, "Trạng thái"
        )

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} không được để trống.")
        return gia_tri.strip()

    @staticmethod
    def _chuoi_tuy_chon(gia_tri: str | None) -> str:
        if gia_tri is None:
            return ""
        if not isinstance(gia_tri, str):
            raise ValueError("Giá trị phải là chuỗi.")
        return gia_tri.strip()

    @classmethod
    def _kiem_tra_lua_chon(cls, gia_tri: str, danh_sach: set[str], ten_truong: str) -> str:
        gia_tri = cls._chuoi_bat_buoc(gia_tri, ten_truong).upper()
        if gia_tri not in danh_sach:
            cac_gia_tri = ", ".join(sorted(danh_sach))
            raise ValueError(f"{ten_truong} không hợp lệ. Chọn một trong: {cac_gia_tri}.")
        return gia_tri

    def cap_nhat_thong_tin(
        self,
        ho_ten: str | None = None,
        email: str | None = None,
        so_dien_thoai: str | None = None,
    ) -> None:
        """Cập nhật các thông tin được cung cấp; None nghĩa là giữ nguyên."""
        if ho_ten is not None:
            self.ho_ten = self._chuoi_bat_buoc(ho_ten, "Họ tên")
        if email is not None:
            self.email = self._chuoi_tuy_chon(email)
        if so_dien_thoai is not None:
            self.so_dien_thoai = self._chuoi_tuy_chon(so_dien_thoai)

    def co_vai_tro(self, vai_tro: str) -> bool:
        """Trả về True nếu người dùng có vai trò được hỏi."""
        if not isinstance(vai_tro, str):
            return False
        return self.vai_tro == vai_tro.strip().upper()

    def dang_hoat_dong(self) -> bool:
        """Kiểm tra tài khoản có đang hoạt động hay không."""
        return self.trang_thai == "HOAT_DONG"

    def __repr__(self) -> str:
        # Không đưa mat_khau_hash vào chuỗi biểu diễn.
        return (
            f"NguoiDung(ma_nguoi_dung={self.ma_nguoi_dung!r}, "
            f"ho_ten={self.ho_ten!r}, ten_dang_nhap={self.ten_dang_nhap!r}, "
            f"vai_tro={self.vai_tro!r}, trang_thai={self.trang_thai!r})"
        )
