import unittest
from models.nguoi_dung import NguoiDung


class TestNguoiDung(unittest.TestCase):
    def tao_nguoi_dung(self, **kwargs):
        du_lieu = dict(ma_nguoi_dung="ND01", ho_ten="Nguyen An", email="an@example.com",
                       so_dien_thoai="0912345678", ten_dang_nhap="nguyenan",
                       mat_khau_hash="$2b$12$hash_da_bam", vai_tro="KHACH_HANG")
        du_lieu.update(kwargs)
        return NguoiDung(**du_lieu)

    def test_tao_hop_le_va_vai_tro(self):
        nd = self.tao_nguoi_dung()
        self.assertTrue(nd.co_vai_tro("khach_hang"))
        self.assertTrue(nd.dang_hoat_dong())

    def test_email_sai_dinh_dang(self):
        with self.assertRaisesRegex(ValueError, "Email"):
            self.tao_nguoi_dung(email="khong-phai-email")

    def test_email_rong_duoc_phep(self):
        self.assertEqual(self.tao_nguoi_dung(email="").email, "")

    def test_so_dien_thoai_sai_dinh_dang(self):
        with self.assertRaisesRegex(ValueError, "Số điện thoại"):
            self.tao_nguoi_dung(so_dien_thoai="12345")

    def test_vai_tro_sai(self):
        with self.assertRaisesRegex(ValueError, "Vai trò"):
            self.tao_nguoi_dung(vai_tro="SUPER_ADMIN")

    def test_repr_khong_lo_hash(self):
        nd = self.tao_nguoi_dung()
        self.assertNotIn(nd.mat_khau_hash, repr(nd))

    def test_cap_nhat_nguyen_tu(self):
        nd = self.tao_nguoi_dung()
        with self.assertRaises(ValueError):
            nd.cap_nhat_thong_tin(ho_ten="Ten moi", email="sai")
        self.assertEqual(nd.ho_ten, "Nguyen An")
        self.assertEqual(nd.email, "an@example.com")

    def test_khong_nhan_email_sai_kieu(self):
        with self.assertRaises(ValueError):
            self.tao_nguoi_dung(email=123)


if __name__ == "__main__":
    unittest.main()
