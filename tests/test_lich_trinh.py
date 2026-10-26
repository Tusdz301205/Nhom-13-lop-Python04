"""Kiểm thử ràng buộc lịch trình và cách ly tham chiếu hoạt động."""

import unittest
from datetime import time

from models.hoat_dong_lich_trinh import HoatDongLichTrinh
from models.lich_trinh import LichTrinh


class TestLichTrinh(unittest.TestCase):
    def setUp(self):
        self.lich = LichTrinh("LT01", "T01")

    def tao_hoat_dong(self, ma="HD01", ngay=1, bat_dau=8, ket_thuc=9, **thay_doi):
        du_lieu = dict(
            ma_hoat_dong=ma, ma_lich_trinh="LT01", ngay_thu=ngay,
            gio_bat_dau=time(bat_dau), gio_ket_thuc=time(ket_thuc),
            dia_diem="Đà Lạt", noi_dung="Tham quan",
        )
        du_lieu.update(thay_doi)
        return HoatDongLichTrinh(**du_lieu)

    def du_lieu_hien_tai(self):
        return [vars(hd).copy() for hd in self.lich.danh_sach_hoat_dong]

    def test_tao_lich_trinh(self):
        lich = LichTrinh(" LT01 ", " T01 ")
        self.assertEqual((lich.ma_lich_trinh, lich.ma_tour), ("LT01", "T01"))
        self.assertEqual(lich.danh_sach_hoat_dong, ())

    def test_ma_khong_hop_le(self):
        for truong in ("ma_lich_trinh", "ma_tour"):
            for gia_tri in ("", " ", None, 123, True):
                with self.subTest(truong=truong, gia_tri=gia_tri):
                    du_lieu = dict(ma_lich_trinh="LT01", ma_tour="T01")
                    du_lieu[truong] = gia_tri
                    with self.assertRaises(ValueError):
                        LichTrinh(**du_lieu)

    def test_them_va_sap_xep_theo_ngay_gio(self):
        for hd in (
            self.tao_hoat_dong("HD03", ngay=2),
            self.tao_hoat_dong("HD02", bat_dau=10, ket_thuc=11),
            self.tao_hoat_dong("HD01"),
        ):
            self.lich.them_hoat_dong(hd)
        self.assertEqual(
            [hd.ma_hoat_dong for hd in self.lich.lay_danh_sach_hoat_dong()],
            ["HD01", "HD02", "HD03"],
        )

    def test_khong_cho_trung_ma_du_khac_ngay(self):
        self.lich.them_hoat_dong(self.tao_hoat_dong())
        with self.assertRaises(ValueError):
            self.lich.them_hoat_dong(self.tao_hoat_dong(ngay=2))
        self.assertEqual(len(self.lich.danh_sach_hoat_dong), 1)

    def test_tu_choi_hoat_dong_sai_lich_trinh_va_sai_kieu(self):
        for hd in (None, "HD01", self.tao_hoat_dong(ma_lich_trinh="LT02")):
            for thao_tac in (self.lich.them_hoat_dong, self.lich.sua_hoat_dong,
                            self.lich.kiem_tra_trung_thoi_gian):
                with self.subTest(hd=hd, thao_tac=thao_tac.__name__):
                    with self.assertRaises(ValueError):
                        thao_tac(hd)
        self.assertEqual(self.lich.danh_sach_hoat_dong, ())

    def test_tu_choi_cac_dang_giao_nhau(self):
        self.lich.them_hoat_dong(self.tao_hoat_dong(bat_dau=9, ket_thuc=11))
        for bat_dau, ket_thuc in ((8, 10), (10, 12), (9, 11), (8, 12), (9, 10)):
            with self.subTest(bat_dau=bat_dau, ket_thuc=ket_thuc):
                hd = self.tao_hoat_dong("HD02", bat_dau=bat_dau, ket_thuc=ket_thuc)
                self.assertTrue(self.lich.kiem_tra_trung_thoi_gian(hd))
                with self.assertRaises(ValueError):
                    self.lich.them_hoat_dong(hd)
                self.assertEqual(len(self.lich.danh_sach_hoat_dong), 1)

    def test_cho_phep_noi_tiep_va_cung_gio_khac_ngay(self):
        for hd in (
            self.tao_hoat_dong("HD01", bat_dau=9, ket_thuc=10),
            self.tao_hoat_dong("HD02", bat_dau=8, ket_thuc=9),
            self.tao_hoat_dong("HD03", bat_dau=10, ket_thuc=11),
            self.tao_hoat_dong("HD04", ngay=2, bat_dau=9, ket_thuc=10),
        ):
            self.assertFalse(self.lich.kiem_tra_trung_thoi_gian(hd))
            self.lich.them_hoat_dong(hd)
        self.assertEqual(len(self.lich.danh_sach_hoat_dong), 4)

    def test_sua_hoat_dong_bo_qua_chinh_no_va_sap_xep_lai(self):
        self.lich.them_hoat_dong(self.tao_hoat_dong())
        self.lich.them_hoat_dong(self.tao_hoat_dong("HD02", ngay=2))
        ban_sua = self.tao_hoat_dong(noi_dung="Nội dung mới")
        self.lich.sua_hoat_dong(ban_sua)
        self.assertEqual(self.lich.danh_sach_hoat_dong[0].noi_dung, "Nội dung mới")
        ban_sua.cap_nhat_hoat_dong(ngay_thu=3)
        self.lich.sua_hoat_dong(ban_sua)
        self.assertEqual(
            [hd.ma_hoat_dong for hd in self.lich.danh_sach_hoat_dong],
            ["HD02", "HD01"],
        )
        ban_sua.noi_dung = "Sửa tham chiếu bên ngoài"
        self.assertEqual(self.lich.danh_sach_hoat_dong[1].noi_dung, "Nội dung mới")

    def test_sua_that_bai_giu_nguyen_du_lieu(self):
        self.lich.them_hoat_dong(self.tao_hoat_dong())
        self.lich.them_hoat_dong(self.tao_hoat_dong("HD02", bat_dau=10, ket_thuc=12))
        truoc = self.du_lieu_hien_tai()
        for hd in (
            self.tao_hoat_dong(bat_dau=11, ket_thuc=13),
            self.tao_hoat_dong("KHONG_CO"),
            self.tao_hoat_dong(ma_lich_trinh="LT02"),
        ):
            with self.subTest(ma=hd.ma_hoat_dong, gio=hd.gio_bat_dau):
                with self.assertRaises(ValueError):
                    self.lich.sua_hoat_dong(hd)
                self.assertEqual(self.du_lieu_hien_tai(), truoc)

    def test_kiem_tra_lai_hoat_dong_bi_gan_sai_truoc_them_sua(self):
        self.lich.them_hoat_dong(self.tao_hoat_dong())
        truoc = self.du_lieu_hien_tai()
        for truong, gia_tri in (
            ("ma_hoat_dong", " "), ("ma_hoat_dong", None),
            ("dia_diem", ""), ("dia_diem", 123),
            ("noi_dung", " "), ("noi_dung", []),
            ("ngay_thu", 0), ("gio_ket_thuc", time(7)),
        ):
            for thao_tac in (self.lich.them_hoat_dong, self.lich.sua_hoat_dong):
                with self.subTest(truong=truong, gia_tri=gia_tri,
                                  thao_tac=thao_tac.__name__):
                    ma = "HD02" if thao_tac.__name__ == "them_hoat_dong" else "HD01"
                    hd = self.tao_hoat_dong(ma, ngay=2)
                    setattr(hd, truong, gia_tri)
                    with self.assertRaises(ValueError):
                        thao_tac(hd)
                    self.assertEqual(self.du_lieu_hien_tai(), truoc)

    def test_cach_ly_tham_chieu_dau_vao_va_danh_sach_tra_ve(self):
        hd = self.tao_hoat_dong()
        self.lich.them_hoat_dong(hd)
        hd.cap_nhat_hoat_dong(ngay_thu=2, noi_dung="Sửa bên ngoài")
        for danh_sach in (self.lich.danh_sach_hoat_dong,
                         self.lich.lay_danh_sach_hoat_dong()):
            self.assertIsInstance(danh_sach, tuple)
            self.assertEqual(danh_sach[0].ngay_thu, 1)
            danh_sach[0].noi_dung = "Sửa bản sao"
        self.assertEqual(self.lich.danh_sach_hoat_dong[0].noi_dung, "Tham quan")

    def test_xoa_hoat_dong(self):
        self.lich.them_hoat_dong(self.tao_hoat_dong())
        self.lich.them_hoat_dong(self.tao_hoat_dong("HD02", ngay=2))
        self.lich.xoa_hoat_dong(" HD01 ")
        self.assertEqual(
            [hd.ma_hoat_dong for hd in self.lich.danh_sach_hoat_dong], ["HD02"],
        )

    def test_xoa_khong_hop_le_giu_nguyen_du_lieu(self):
        self.lich.them_hoat_dong(self.tao_hoat_dong())
        truoc = self.du_lieu_hien_tai()
        for ma in ("", " ", None, 123, "KHONG_CO"):
            with self.subTest(ma=ma):
                with self.assertRaises(ValueError):
                    self.lich.xoa_hoat_dong(ma)
                self.assertEqual(self.du_lieu_hien_tai(), truoc)


if __name__ == "__main__":
    unittest.main()
