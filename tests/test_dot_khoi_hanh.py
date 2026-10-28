"""Kiểm thử đợt khởi hành: ngày, giá, sức chứa và trạng thái mở bán."""

import unittest
from datetime import datetime
from decimal import Decimal

from models.dot_khoi_hanh import DotKhoiHanh


class TestDotKhoiHanh(unittest.TestCase):
    def tao_dot(self, **thay_doi):
        du_lieu = dict(
            ma_dot_khoi_hanh="DKH01",
            ma_tour="T01",
            ngay_di=datetime(2026, 12, 1, 7, 0),
            ngay_ve=datetime(2026, 12, 3, 18, 0),
            gia_ap_dung=Decimal("2000000"),
            suc_chua=20,
        )
        du_lieu.update(thay_doi)
        return DotKhoiHanh(**du_lieu)

    def test_tao_hop_le(self):
        dot = self.tao_dot(ma_dot_khoi_hanh=" DKH01 ", ma_tour=" T01 ", trang_thai=" mo_ban ")
        self.assertEqual((dot.ma_dot_khoi_hanh, dot.ma_tour), ("DKH01", "T01"))
        self.assertEqual(dot.trang_thai, DotKhoiHanh.MO_BAN)
        self.assertTrue(dot.co_dang_mo_ban())
        self.assertTrue(dot.kiem_tra_ngay_hop_le())

    def test_ngay_ve_truoc_hoac_bang_ngay_di(self):
        for ngay_ve in (datetime(2026, 11, 30), datetime(2026, 12, 1, 7, 0)):
            with self.subTest(ngay_ve=ngay_ve):
                with self.assertRaises(ValueError):
                    self.tao_dot(ngay_ve=ngay_ve)

    def test_ngay_sai_kieu(self):
        with self.assertRaises(ValueError):
            self.tao_dot(ngay_di="2026-12-01")

    def test_gia_khong_hop_le(self):
        for gia in (Decimal("0"), Decimal("-1"), Decimal("NaN"), Decimal("Infinity"), 2000000.0, 2000000):
            with self.subTest(gia=gia):
                with self.assertRaises(ValueError):
                    self.tao_dot(gia_ap_dung=gia)

    def test_suc_chua_khong_hop_le(self):
        for suc_chua in (0, -5, True, 10.0, "20"):
            with self.subTest(suc_chua=suc_chua):
                with self.assertRaises(ValueError):
                    self.tao_dot(suc_chua=suc_chua)

    def test_trang_thai_khong_hop_le(self):
        with self.assertRaises(ValueError):
            self.tao_dot(trang_thai="DANG_KINH_DOANH")

    def test_so_cho_con_lai_va_ban_vuot_cho(self):
        dot = self.tao_dot(suc_chua=10)
        self.assertEqual(dot.so_cho_con_lai(7), 3)
        self.assertTrue(dot.co_du_cho(3, 7))
        self.assertFalse(dot.co_du_cho(4, 7))
        with self.assertRaises(ValueError):
            dot.so_cho_con_lai(11)
        with self.assertRaises(ValueError):
            dot.so_cho_con_lai(-1)
        with self.assertRaises(ValueError):
            dot.co_du_cho(0, 0)

    def test_khong_du_cho_khi_khong_mo_ban(self):
        dot = self.tao_dot()
        dot.dong_mo_ban()
        self.assertFalse(dot.co_du_cho(1, 0))

    def test_cap_nhat_suc_chua(self):
        dot = self.tao_dot(suc_chua=10)
        dot.cap_nhat_suc_chua(15, 8)
        self.assertEqual(dot.suc_chua, 15)
        with self.assertRaises(ValueError):
            dot.cap_nhat_suc_chua(5, 8)
        self.assertEqual(dot.suc_chua, 15)
        with self.assertRaises(ValueError):
            dot.cap_nhat_suc_chua(-1, 0)

    def test_cap_nhat_gia(self):
        dot = self.tao_dot()
        dot.cap_nhat_gia(Decimal("2500000"))
        self.assertEqual(dot.gia_ap_dung, Decimal("2500000"))
        with self.assertRaises(ValueError):
            dot.cap_nhat_gia(Decimal("-1"))
        self.assertEqual(dot.gia_ap_dung, Decimal("2500000"))

    def test_dong_mo_ban_va_mo_lai(self):
        dot = self.tao_dot()
        dot.dong_mo_ban()
        self.assertEqual(dot.trang_thai, DotKhoiHanh.DONG_BAN)
        with self.assertRaises(ValueError):
            dot.dong_mo_ban()
        dot.mo_ban()
        self.assertTrue(dot.co_dang_mo_ban())
        with self.assertRaises(ValueError):
            dot.mo_ban()

    def test_dot_da_huy(self):
        dot = self.tao_dot()
        dot.huy_dot_khoi_hanh()
        self.assertEqual(dot.trang_thai, DotKhoiHanh.DA_HUY)
        self.assertFalse(dot.co_du_cho(1, 0))
        for thao_tac in (
            dot.mo_ban,
            dot.dong_mo_ban,
            dot.huy_dot_khoi_hanh,
            lambda: dot.cap_nhat_gia(Decimal("1")),
            lambda: dot.cap_nhat_suc_chua(30, 0),
        ):
            with self.subTest(thao_tac=thao_tac):
                with self.assertRaises(ValueError):
                    thao_tac()
        self.assertEqual(dot.trang_thai, DotKhoiHanh.DA_HUY)


if __name__ == "__main__":
    unittest.main()
