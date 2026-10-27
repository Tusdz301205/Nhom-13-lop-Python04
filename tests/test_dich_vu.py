"""Kiểm thử danh mục dịch vụ tùy chọn."""

import unittest
from decimal import Decimal

from models.dich_vu import DichVu


class TestDichVu(unittest.TestCase):
    def tao_dich_vu(self, **thay_doi):
        du_lieu = dict(
            ma_dich_vu="DV01",
            ten_dich_vu="Đưa đón sân bay",
            don_gia=Decimal("300000"),
            don_vi_tinh="LAN",
        )
        du_lieu.update(thay_doi)
        return DichVu(**du_lieu)

    def test_tao_hop_le(self):
        dv = self.tao_dich_vu(
            ma_dich_vu=" DV01 ", ten_dich_vu=" Đưa đón ", mo_ta=" Xe 7 chỗ ",
            don_vi_tinh=" nguoi ",
        )
        self.assertEqual(
            (dv.ma_dich_vu, dv.ten_dich_vu, dv.mo_ta, dv.don_vi_tinh),
            ("DV01", "Đưa đón", "Xe 7 chỗ", DichVu.NGUOI),
        )
        self.assertEqual(dv.trang_thai, DichVu.DANG_CUNG_CAP)
        self.assertTrue(dv.dang_cung_cap())

    def test_cho_phep_dich_vu_mien_phi(self):
        self.assertEqual(self.tao_dich_vu(don_gia=Decimal("0")).don_gia, Decimal("0"))

    def test_gia_khong_hop_le(self):
        for gia in (Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), 300000.0, 300000, None):
            with self.subTest(gia=gia):
                with self.assertRaises(ValueError):
                    self.tao_dich_vu(don_gia=gia)

    def test_chuoi_bat_buoc_va_lua_chon_khong_hop_le(self):
        for truong, gia_tri in (
            ("ma_dich_vu", " "), ("ten_dich_vu", ""), ("ten_dich_vu", None),
            ("don_vi_tinh", "KG"), ("trang_thai", "MO_BAN"), ("mo_ta", None),
        ):
            with self.subTest(truong=truong, gia_tri=gia_tri):
                with self.assertRaises(ValueError):
                    self.tao_dich_vu(**{truong: gia_tri})

    def test_cap_nhat_thong_tin(self):
        dv = self.tao_dich_vu()
        dv.cap_nhat_thong_tin(ten_dich_vu=" Bữa tối ", mo_ta="Hải sản", don_vi_tinh="goi")
        self.assertEqual((dv.ten_dich_vu, dv.mo_ta, dv.don_vi_tinh), ("Bữa tối", "Hải sản", DichVu.GOI))

    def test_cap_nhat_loi_khong_sua_do(self):
        dv = self.tao_dich_vu()
        truoc = vars(dv).copy()
        with self.assertRaises(ValueError):
            dv.cap_nhat_thong_tin(ten_dich_vu="Tên mới", don_vi_tinh="KHONG_HOP_LE")
        self.assertEqual(vars(dv), truoc)

    def test_cap_nhat_gia(self):
        dv = self.tao_dich_vu()
        dv.cap_nhat_gia(Decimal("350000"))
        self.assertEqual(dv.don_gia, Decimal("350000"))
        with self.assertRaises(ValueError):
            dv.cap_nhat_gia(Decimal("-5"))
        self.assertEqual(dv.don_gia, Decimal("350000"))

    def test_ngung_cung_cap(self):
        dv = self.tao_dich_vu()
        dv.ngung_cung_cap()
        self.assertFalse(dv.dang_cung_cap())
        with self.assertRaises(ValueError):
            dv.ngung_cung_cap()


if __name__ == "__main__":
    unittest.main()
