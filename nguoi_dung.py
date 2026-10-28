"""Domain class quản lý tài khoản và quyền người dùng."""

from __future__ import annotations
import re

VAI_TRO_HOP_LE = {"KHACH_HANG", "NHAN_VIEN", "QUAN_TRI_VIEN"}
TRANG_THAI_HOP_LE = {"HOAT_DONG", "KHOA"}
# Chấp nhận số Việt Nam 10 chữ số bắt đầu bằng 0 hoặc mã quốc gia +84.
_REGEX_EMAIL = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+$")
_REGEX_SO_DIEN_THOAI = re.compile(r"^(?:0[35789]\d{8}|\\+84[35789]\d{8})$")


class NguoiDung:
    """Lưu thông tin tài khoản; không thực hiện đăng nhập hay lưu trữ dữ liệu."""

    def __init__(self, ma_nguoi_dung: str, ho_ten: str, email: str = "",
                 so_dien_thoai: str = "", ten_dang_nhap: str = "",
                 mat_khau_hash: str = "", vai_tro: str = "KHACH_HANG",
                 trang_thai: str = "HOAT_DONG") -> None:
        # Xác thực toàn bộ dữ liệu trước khi gán thuộc tính.
        ma = self._chuoi_bat_buoc(ma_nguoi_dung, "Mã người dùng")
        ten = self._chuoi_bat_buoc(ho_ten, "Họ tên")
        email_hop_le = self._email_tuy_chon(email)
        dien_thoai_hop_le = self._so_dien_thoai_tuy_chon(so_dien_thoai)
        ten_dn = self._chuoi_bat_buoc(ten_dang_nhap, "Tên đăng nhập")
        # Domain class chỉ nhận trường hash có sẵn, không nhận tham số mật khẩu riêng.
        hash_da_bam = self._chuoi_bat_buoc(mat_khau_hash, "Mã băm mật khẩu")
        vai_tro_hop_le = self._kiem_tra_lua_chon(vai_tro, VAI_TRO_HOP_LE, "Vai trò")
        trang_thai_hop_le = self._kiem_tra_lua_chon(trang_thai, TRANG_THAI_HOP_LE, "Trạng thái")

        self.ma_nguoi_dung = ma
        self.ho_ten = ten
        self.email = email_hop_le
        self.so_dien_thoai = dien_thoai_hop_le
        self.ten_dang_nhap = ten_dn
        self.mat_khau_hash = hash_da_bam
        self.vai_tro = vai_tro_hop_le
        self.trang_thai = trang_thai_hop_le

    @staticmethod
    def _chuoi_bat_buoc(gia_tri: str, ten_truong: str) -> str:
        if not isinstance(gia_tri, str) or not gia_tri.strip():
            raise ValueError(f"{ten_truong} phải là chuỗi và không được để trống.")
        return gia_tri.strip()

    @classmethod
    def _email_tuy_chon(cls, gia_tri: str | None) -> str:
        if gia_tri is None:
            return ""
        if not isinstance(gia_tri, str):
            raise ValueError("Email phải là chuỗi hoặc None.")
        gia_tri = gia_tri.strip()
        if gia_tri and not _REGEX_EMAIL.fullmatch(gia_tri):
            raise ValueError("Email không đúng định dạng.")
        return gia_tri

    @classmethod
    def _so_dien_thoai_tuy_chon(cls, gia_tri: str | None) -> str:
        if gia_tri is None:
            return ""
        if not isinstance(gia_tri, str):
            raise ValueError("Số điện thoại phải là chuỗi hoặc None.")
        gia_tri = gia_tri.strip()
        if gia_tri and not _REGEX_SO_DIEN_THOAI.fullmatch(gia_tri):
            raise ValueError("Số điện thoại không đúng định dạng Việt Nam.")
        return gia_tri

    @classmethod
    def _kiem_tra_lua_chon(cls, gia_tri: str, danh_sach: set[str], ten_truong: str) -> str:
        gia_tri = cls._chuoi_bat_buoc(gia_tri, ten_truong).upper()
        if gia_tri not in danh_sach:
            cac_gia_tri = ", ".join(sorted(danh_sach))
            raise ValueError(f"{ten_truong} không hợp lệ. Chọn một trong: {cac_gia_tri}.")
        return gia_tri

    def cap_nhat_thong_tin(self, ho_ten: str | None = None,
                           email: str | None = None,
                           so_dien_thoai: str | None = None) -> None:
        """Kiểm tra mọi giá trị mới trước khi cập nhật để tránh cập nhật dở."""
        ten_moi = self.ho_ten if ho_ten is None else self._chuoi_bat_buoc(ho_ten, "Họ tên")
        email_moi = self.email if email is None else self._email_tuy_chon(email)
        dien_thoai_moi = self.so_dien_thoai if so_dien_thoai is None else self._so_dien_thoai_tuy_chon(so_dien_thoai)
        self.ho_ten, self.email, self.so_dien_thoai = ten_moi, email_moi, dien_thoai_moi

    def co_vai_tro(self, vai_tro: str) -> bool:
        return isinstance(vai_tro, str) and self.vai_tro == vai_tro.strip().upper()

    def dang_hoat_dong(self) -> bool:
        return self.trang_thai == "HOAT_DONG"

    def __repr__(self) -> str:
        # Tuyệt đối không đưa mat_khau_hash vào repr.
        return (f"NguoiDung(ma_nguoi_dung={self.ma_nguoi_dung!r}, ho_ten={self.ho_ten!r}, "
                f"ten_dang_nhap={self.ten_dang_nhap!r}, vai_tro={self.vai_tro!r}, "
                f"trang_thai={self.trang_thai!r})")
