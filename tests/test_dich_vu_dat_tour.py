"""Kiểm thử một dịch vụ khách chọn trong đơn đặt tour."""

import unittest
from decimal import Decimal

from models.dich_vu import DichVu
from models.dich_vu_dat_tour import DichVuDatTour


class TestDichVuDatTour(unittest.TestCase):
    def tao_chi_tiet(self, **thay_doi):
        du_lieu = dict(
            ma_dat_tour="DT01", ma_dich_vu="DV01",
            so_luong=2, don_gia_da_chot=Decimal("300000"),
        )
        du_lieu.update(thay_doi)
        return DichVuDatTour(**du_lieu)

    def test_tao_hop_le_va_thanh_tien(self):
        ct = self.tao_chi_tiet(ma_dat_tour=" DT01 ", ma_dich_vu=" DV01 ")
        self.assertEqual((ct.ma_dat_tour, ct.ma_dich_vu), ("DT01", "DV01"))
        self.assertEqual(ct.tinh_thanh_tien(), Decimal("600000"))

    def test_dich_vu_mien_phi(self):
        self.assertEqual(self.tao_chi_tiet(don_gia_da_chot=Decimal("0")).tinh_thanh_tien(), Decimal("0"))

    def test_so_luong_khong_hop_le(self):
        for so_luong in (0, -1, True, 1.5, "2"):
            with self.subTest(so_luong=so_luong):
                with self.assertRaises(ValueError):
                    self.tao_chi_tiet(so_luong=so_luong)

    def test_gia_va_ma_khong_hop_le(self):
        for truong, gia_tri in (
            ("don_gia_da_chot", Decimal("-1")), ("don_gia_da_chot", Decimal("NaN")),
            ("don_gia_da_chot", 300000.0), ("ma_dat_tour", " "), ("ma_dich_vu", None),
        ):
            with self.subTest(truong=truong, gia_tri=gia_tri):
                with self.assertRaises(ValueError):
                    self.tao_chi_tiet(**{truong: gia_tri})

    def test_cap_nhat_so_luong(self):
        ct = self.tao_chi_tiet()
        ct.cap_nhat_so_luong(5)
        self.assertEqual(ct.tinh_thanh_tien(), Decimal("1500000"))
        with self.assertRaises(ValueError):
            ct.cap_nhat_so_luong(0)
        self.assertEqual(ct.so_luong, 5)

    def test_khoa_va_gia_chot_chi_doc(self):
        ct = self.tao_chi_tiet()
        for truong in ("ma_dat_tour", "ma_dich_vu", "so_luong", "don_gia_da_chot"):
            with self.subTest(truong=truong):
                with self.assertRaises(AttributeError):
                    setattr(ct, truong, "X")

    def test_doi_gia_danh_muc_khong_doi_gia_da_chot(self):
        dv = DichVu("DV01", "Đưa đón", Decimal("300000"), "LAN")
        ct = self.tao_chi_tiet(don_gia_da_chot=dv.don_gia)
        dv.cap_nhat_gia(Decimal("500000"))
        self.assertEqual(ct.don_gia_da_chot, Decimal("300000"))
        self.assertEqual(ct.tinh_thanh_tien(), Decimal("600000"))


if __name__ == "__main__":
    unittest.main()
