"""Kiểm thử đơn đặt tour: trạng thái, dịch vụ đã chọn và tổng tiền."""

import unittest
from datetime import datetime
from decimal import Decimal

from models.dat_tour import DatTour
from models.dich_vu import DichVu
from models.dich_vu_dat_tour import DichVuDatTour
from models.dot_khoi_hanh import DotKhoiHanh


class TestDatTour(unittest.TestCase):
    def tao_don(self, **thay_doi):
        du_lieu = dict(
            ma_dat_tour="DT01",
            ma_nguoi_dung="ND01",
            ma_dot_khoi_hanh="DKH01",
            ngay_dat=datetime(2026, 10, 24, 9, 0),
            so_nguoi=3,
            don_gia_da_chot=Decimal("2000000"),
        )
        du_lieu.update(thay_doi)
        return DatTour(**du_lieu)

    def tao_chi_tiet(self, ma_dich_vu="DV01", so_luong=2, gia="300000", ma_dat_tour="DT01"):
        return DichVuDatTour(ma_dat_tour, ma_dich_vu, so_luong, Decimal(gia))

    # ----- Khởi tạo -----

    def test_tao_hop_le(self):
        don = self.tao_don(ma_dat_tour=" DT01 ", trang_thai=" cho_xac_nhan ")
        self.assertEqual(don.ma_dat_tour, "DT01")
        self.assertEqual(don.trang_thai, DatTour.CHO_XAC_NHAN)
        self.assertEqual(don.tong_tien, Decimal("6000000"))
        self.assertEqual(don.tinh_tong_tien(), Decimal("6000000"))
        self.assertEqual(don.danh_sach_dich_vu, ())
        self.assertIsNone(don.han_giu_cho)

    def test_du_lieu_khong_hop_le(self):
        for truong, gia_tri in (
            ("so_nguoi", 0), ("so_nguoi", -1), ("so_nguoi", True), ("so_nguoi", 2.0),
            ("don_gia_da_chot", Decimal("0")), ("don_gia_da_chot", Decimal("-1")),
            ("don_gia_da_chot", Decimal("NaN")), ("don_gia_da_chot", 2000000.0),
            ("ma_dat_tour", " "), ("ma_nguoi_dung", None), ("ma_dot_khoi_hanh", ""),
            ("ngay_dat", "2026-10-24"), ("trang_thai", "MO_BAN"),
            ("han_giu_cho", datetime(2026, 10, 23)),
        ):
            with self.subTest(truong=truong, gia_tri=gia_tri):
                with self.assertRaises(ValueError):
                    self.tao_don(**{truong: gia_tri})

    def test_khoi_tao_kem_dich_vu(self):
        don = self.tao_don(danh_sach_dich_vu=[self.tao_chi_tiet()])
        self.assertEqual(don.tong_tien, Decimal("6600000"))
        with self.assertRaises(ValueError):
            self.tao_don(danh_sach_dich_vu=[self.tao_chi_tiet(), self.tao_chi_tiet()])
        with self.assertRaises(ValueError):
            self.tao_don(danh_sach_dich_vu=[self.tao_chi_tiet(ma_dat_tour="DT99")])

    # ----- Hành khách và trạng thái -----

    def test_kiem_tra_so_luong_hanh_khach(self):
        don = self.tao_don()
        self.assertTrue(don.kiem_tra_so_luong_hanh_khach(3))
        self.assertFalse(don.kiem_tra_so_luong_hanh_khach(2))
        with self.assertRaises(ValueError):
            don.kiem_tra_so_luong_hanh_khach(True)

    def test_chuyen_trang_thai(self):
        don = self.tao_don()
        self.assertTrue(don.co_the_huy())
        don.chuyen_trang_thai(DatTour.DA_XAC_NHAN)
        self.assertTrue(don.co_the_huy())
        with self.assertRaises(ValueError):
            don.chuyen_trang_thai(DatTour.CHO_XAC_NHAN)
        don.chuyen_trang_thai(DatTour.DA_HUY)
        self.assertFalse(don.co_the_huy())

    def test_don_da_huy_khong_phuc_hoi(self):
        don = self.tao_don(trang_thai=DatTour.DA_HUY)
        for trang_thai in (DatTour.CHO_XAC_NHAN, DatTour.DA_XAC_NHAN, DatTour.DA_HUY):
            with self.subTest(trang_thai=trang_thai):
                with self.assertRaises(ValueError):
                    don.chuyen_trang_thai(trang_thai)
        self.assertEqual(don.trang_thai, DatTour.DA_HUY)

    # ----- Dịch vụ đã chọn -----

    def test_them_dich_vu_cap_nhat_tong_tien(self):
        don = self.tao_don()
        don.them_dich_vu(self.tao_chi_tiet("DV01", 2, "300000"))
        don.them_dich_vu(self.tao_chi_tiet("DV02", 1, "0"))
        self.assertEqual(len(don.danh_sach_dich_vu), 2)
        self.assertEqual(don.tong_tien, Decimal("6600000"))

    def test_trung_dich_vu_trong_don(self):
        don = self.tao_don()
        don.them_dich_vu(self.tao_chi_tiet("DV01"))
        with self.assertRaises(ValueError):
            don.them_dich_vu(self.tao_chi_tiet("DV01", 5))
        self.assertEqual(len(don.danh_sach_dich_vu), 1)
        self.assertEqual(don.danh_sach_dich_vu[0].so_luong, 2)

    def test_dich_vu_thuoc_sai_don(self):
        don = self.tao_don()
        with self.assertRaises(ValueError):
            don.them_dich_vu(self.tao_chi_tiet(ma_dat_tour="DT99"))
        with self.assertRaises(ValueError):
            don.them_dich_vu("DV01")
        self.assertEqual(don.danh_sach_dich_vu, ())

    def test_cap_nhat_so_luong_lam_tong_tien_cap_nhat(self):
        don = self.tao_don()
        don.them_dich_vu(self.tao_chi_tiet("DV01", 2, "300000"))
        don.cap_nhat_dich_vu(" DV01 ", 4)
        self.assertEqual(don.tong_tien, Decimal("7200000"))
        with self.assertRaises(ValueError):
            don.cap_nhat_dich_vu("DV01", 0)
        self.assertEqual(don.tong_tien, Decimal("7200000"))
        with self.assertRaises(ValueError):
            don.cap_nhat_dich_vu("DV99", 1)

    def test_xoa_dich_vu(self):
        don = self.tao_don()
        don.them_dich_vu(self.tao_chi_tiet("DV01"))
        don.xoa_dich_vu("DV01")
        self.assertEqual(don.tong_tien, Decimal("6000000"))
        with self.assertRaises(ValueError):
            don.xoa_dich_vu("DV01")

    def test_khong_sua_ngam_danh_sach_noi_bo(self):
        don = self.tao_don()
        chi_tiet = self.tao_chi_tiet("DV01", 2)
        don.them_dich_vu(chi_tiet)
        chi_tiet.cap_nhat_so_luong(10)
        don.danh_sach_dich_vu[0].cap_nhat_so_luong(10)
        self.assertEqual(don.danh_sach_dich_vu[0].so_luong, 2)
        self.assertIsInstance(don.danh_sach_dich_vu, tuple)
        self.assertEqual(don.tong_tien, Decimal("6600000"))

    def test_khong_doi_dich_vu_cua_don_da_huy(self):
        don = self.tao_don()
        don.them_dich_vu(self.tao_chi_tiet("DV01"))
        don.chuyen_trang_thai(DatTour.DA_HUY)
        for thao_tac in (
            lambda: don.them_dich_vu(self.tao_chi_tiet("DV02")),
            lambda: don.cap_nhat_dich_vu("DV01", 3),
            lambda: don.xoa_dich_vu("DV01"),
        ):
            with self.subTest(thao_tac=thao_tac):
                with self.assertRaises(ValueError):
                    thao_tac()
        self.assertEqual(don.tong_tien, Decimal("6600000"))

    # ----- Tổng tiền -----

    def test_tong_tien_chi_doc(self):
        don = self.tao_don()
        with self.assertRaises(AttributeError):
            don.tong_tien = Decimal("1")

    def test_tong_tien_dong_bo_khi_doi_du_lieu(self):
        don = self.tao_don()
        don.so_nguoi = 4
        self.assertEqual(don.tong_tien, Decimal("8000000"))

    def test_doi_gia_danh_muc_va_dot_khong_doi_gia_don(self):
        dot = DotKhoiHanh(
            "DKH01", "T01", datetime(2026, 12, 1), datetime(2026, 12, 3),
            Decimal("2000000"), 20,
        )
        dich_vu = DichVu("DV01", "Đưa đón", Decimal("300000"), "LAN")
        don = self.tao_don(don_gia_da_chot=dot.gia_ap_dung)
        don.them_dich_vu(DichVuDatTour("DT01", "DV01", 2, dich_vu.don_gia))

        dot.cap_nhat_gia(Decimal("3000000"))
        dich_vu.cap_nhat_gia(Decimal("900000"))

        self.assertEqual(don.don_gia_da_chot, Decimal("2000000"))
        self.assertEqual(don.danh_sach_dich_vu[0].don_gia_da_chot, Decimal("300000"))
        self.assertEqual(don.tong_tien, Decimal("6600000"))


if __name__ == "__main__":
    unittest.main()
