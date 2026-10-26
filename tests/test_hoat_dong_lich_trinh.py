"""Kiểm thử hoạt động theo ngày và cập nhật dữ liệu an toàn."""

import unittest
from datetime import time, timezone

from models.hoat_dong_lich_trinh import HoatDongLichTrinh


class TestHoatDongLichTrinh(unittest.TestCase):
    def tao_hoat_dong(self, **thay_doi):
        du_lieu = dict(
            ma_hoat_dong="HD01", ma_lich_trinh="LT01", ngay_thu=1,
            gio_bat_dau=time(8), gio_ket_thuc=time(9),
            dia_diem="Hồ Xuân Hương", noi_dung="Tham quan",
        )
        du_lieu.update(thay_doi)
        return HoatDongLichTrinh(**du_lieu)

    def test_tao_hoat_dong_va_chuan_hoa_chuoi(self):
        hd = self.tao_hoat_dong(
            ma_hoat_dong=" HD01 ", ma_lich_trinh=" LT01 ",
            dia_diem=" Hồ Xuân Hương ", noi_dung=" Tham quan ",
        )
        self.assertEqual(
            (hd.ma_hoat_dong, hd.ma_lich_trinh, hd.dia_diem, hd.noi_dung),
            ("HD01", "LT01", "Hồ Xuân Hương", "Tham quan"),
        )
        self.assertTrue(hd.kiem_tra_thoi_gian_hop_le())

    def test_chuoi_bat_buoc_khong_hop_le(self):
        for truong in ("ma_hoat_dong", "ma_lich_trinh", "dia_diem", "noi_dung"):
            for gia_tri in ("", " \t ", None, 123, True):
                with self.subTest(truong=truong, gia_tri=gia_tri):
                    with self.assertRaises(ValueError):
                        self.tao_hoat_dong(**{truong: gia_tri})

    def test_ngay_thu_sai_kieu_hoac_khong_duong(self):
        for gia_tri in (0, -1, True, False, 1.5, "1", None):
            with self.subTest(gia_tri=gia_tri):
                with self.assertRaises(ValueError):
                    self.tao_hoat_dong(ngay_thu=gia_tri)

    def test_gio_sai_kieu_hoac_co_mui_gio(self):
        for truong in ("gio_bat_dau", "gio_ket_thuc"):
            for gia_tri in ("08:00", 8, None, time(8, tzinfo=timezone.utc)):
                with self.subTest(truong=truong, gia_tri=gia_tri):
                    with self.assertRaises(ValueError):
                        self.tao_hoat_dong(**{truong: gia_tri})

    def test_ket_thuc_phai_sau_bat_dau_trong_cung_ngay(self):
        for bat_dau, ket_thuc in ((time(8), time(8)), (time(9), time(8)),
                                  (time(23), time(1))):
            with self.subTest(bat_dau=bat_dau, ket_thuc=ket_thuc):
                with self.assertRaises(ValueError):
                    self.tao_hoat_dong(gio_bat_dau=bat_dau, gio_ket_thuc=ket_thuc)

    def test_khoang_thoi_gian_bien_va_ngay_lon(self):
        hd = self.tao_hoat_dong(
            ngay_thu=30, gio_bat_dau=time.min, gio_ket_thuc=time.max,
        )
        self.assertTrue(hd.kiem_tra_thoi_gian_hop_le())

    def test_cap_nhat_hop_le(self):
        hd = self.tao_hoat_dong()
        hd.cap_nhat_hoat_dong(2, time(10), time(11), " Điểm mới ", " Ăn trưa ")
        self.assertEqual(
            (hd.ngay_thu, hd.gio_bat_dau, hd.gio_ket_thuc, hd.dia_diem, hd.noi_dung),
            (2, time(10), time(11), "Điểm mới", "Ăn trưa"),
        )
        self.assertEqual((hd.ma_hoat_dong, hd.ma_lich_trinh), ("HD01", "LT01"))
        truoc = vars(hd).copy()
        hd.cap_nhat_hoat_dong()
        self.assertEqual(vars(hd), truoc)

    def test_cap_nhat_loi_khong_sua_do(self):
        for thay_doi in (
            dict(ngay_thu=0), dict(ngay_thu=True),
            dict(ngay_thu=2, gio_bat_dau=time(10)),
            dict(ngay_thu=2, dia_diem=""),
            dict(ngay_thu=2, dia_diem="Điểm mới", noi_dung=123),
        ):
            with self.subTest(thay_doi=thay_doi):
                hd = self.tao_hoat_dong()
                truoc = vars(hd).copy()
                with self.assertRaises(ValueError):
                    hd.cap_nhat_hoat_dong(**thay_doi)
                self.assertEqual(vars(hd), truoc)

    def test_kiem_tra_lai_sau_khi_thuoc_tinh_bi_gan_sai(self):
        hd = self.tao_hoat_dong()
        hd.ngay_thu = 0
        self.assertFalse(hd.kiem_tra_thoi_gian_hop_le())


if __name__ == "__main__":
    unittest.main()
