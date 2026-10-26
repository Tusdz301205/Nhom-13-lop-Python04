"""Kiểm thử thông tin điểm đến, tọa độ và cập nhật nguyên vẹn."""

import unittest
from decimal import Decimal

from models.diem_den import DiemDen


class TestDiemDen(unittest.TestCase):
    def tao_diem_den(self, **thay_doi):
        du_lieu = dict(ma_diem_den="DD01", ten_diem_den="Đà Lạt", tinh_thanh="Lâm Đồng")
        du_lieu.update(thay_doi)
        return DiemDen(**du_lieu)

    def test_tao_va_chuan_hoa_chuoi(self):
        diem = self.tao_diem_den(
            ma_diem_den=" DD01 ", ten_diem_den=" Đà Lạt ",
            tinh_thanh=" Lâm Đồng ", mo_ta=" Thành phố du lịch ",
        )
        self.assertEqual(
            (diem.ma_diem_den, diem.ten_diem_den, diem.tinh_thanh, diem.mo_ta),
            ("DD01", "Đà Lạt", "Lâm Đồng", "Thành phố du lịch"),
        )
        self.assertEqual((diem.vi_do, diem.kinh_do), (None, None))

    def test_chuoi_bat_buoc_khong_hop_le(self):
        for truong in ("ma_diem_den", "ten_diem_den", "tinh_thanh"):
            for gia_tri in ("", " \t ", None, 123, True, []):
                with self.subTest(truong=truong, gia_tri=gia_tri):
                    with self.assertRaises(ValueError):
                        self.tao_diem_den(**{truong: gia_tri})

    def test_mo_ta_phai_la_chuoi(self):
        for gia_tri in (None, 123, False, []):
            with self.subTest(gia_tri=gia_tri):
                with self.assertRaises(ValueError):
                    self.tao_diem_den(mo_ta=gia_tri)

    def test_toa_do_hop_le_va_cac_bien(self):
        for vi_do, kinh_do in ((11.94, 108.44), (0, 0), (-90, -180), (90, 180)):
            with self.subTest(vi_do=vi_do, kinh_do=kinh_do):
                diem = self.tao_diem_den(vi_do=vi_do, kinh_do=kinh_do)
                self.assertEqual((diem.vi_do, diem.kinh_do), (vi_do, kinh_do))
                self.assertIsInstance(diem.vi_do, float)
                self.assertIsInstance(diem.kinh_do, float)

    def test_thieu_mot_toa_do(self):
        for vi_do, kinh_do in ((None, 0), (0, None)):
            with self.subTest(vi_do=vi_do, kinh_do=kinh_do):
                with self.assertRaises(ValueError):
                    self.tao_diem_den(vi_do=vi_do, kinh_do=kinh_do)

    def test_toa_do_sai_kieu_mien_va_khong_huu_han(self):
        for truong, gioi_han in (("vi_do", 90), ("kinh_do", 180)):
            for gia_tri in (
                -gioi_han - 0.01, gioi_han + 0.01, float("nan"),
                float("inf"), -float("inf"), True, "12.5", [],
                Decimal("12.5"), 10**1000,
            ):
                with self.subTest(truong=truong, gia_tri=gia_tri):
                    toa_do = dict(vi_do=0, kinh_do=0)
                    toa_do[truong] = gia_tri
                    with self.assertRaises(ValueError):
                        self.tao_diem_den(**toa_do)

    def test_cap_nhat_thong_tin_va_giu_nguyen_ma(self):
        diem = self.tao_diem_den(vi_do=1, kinh_do=2)
        diem.cap_nhat_thong_tin(" Điểm mới ", " Tỉnh mới ", " Mô tả ")
        self.assertEqual(
            (diem.ma_diem_den, diem.ten_diem_den, diem.tinh_thanh, diem.mo_ta),
            ("DD01", "Điểm mới", "Tỉnh mới", "Mô tả"),
        )
        self.assertEqual((diem.vi_do, diem.kinh_do), (1, 2))
        truoc = vars(diem).copy()
        diem.cap_nhat_thong_tin()
        self.assertEqual(vars(diem), truoc)
        diem.cap_nhat_thong_tin(mo_ta="")
        self.assertEqual(diem.mo_ta, "")

    def test_cap_nhat_thong_tin_loi_khong_sua_do(self):
        for thay_doi in (
            dict(ten_diem_den=" "),
            dict(ten_diem_den="Tên mới", tinh_thanh=""),
            dict(ten_diem_den="Tên mới", tinh_thanh="Tỉnh mới", mo_ta=123),
        ):
            with self.subTest(thay_doi=thay_doi):
                diem = self.tao_diem_den()
                truoc = vars(diem).copy()
                with self.assertRaises(ValueError):
                    diem.cap_nhat_thong_tin(**thay_doi)
                self.assertEqual(vars(diem), truoc)

    def test_cap_nhat_va_xoa_toa_do(self):
        diem = self.tao_diem_den()
        diem.cap_nhat_toa_do(11.94, 108.44)
        self.assertEqual((diem.vi_do, diem.kinh_do), (11.94, 108.44))
        diem.cap_nhat_toa_do(None, None)
        self.assertEqual((diem.vi_do, diem.kinh_do), (None, None))

    def test_cap_nhat_toa_do_loi_giu_nguyen_ca_cap(self):
        diem = self.tao_diem_den(vi_do=10, kinh_do=20)
        for vi_do, kinh_do in ((30, 181), (91, 40), (None, 40), (30, None),
                              (30, float("nan")), (False, 40)):
            with self.subTest(vi_do=vi_do, kinh_do=kinh_do):
                with self.assertRaises(ValueError):
                    diem.cap_nhat_toa_do(vi_do, kinh_do)
                self.assertEqual((diem.vi_do, diem.kinh_do), (10, 20))


if __name__ == "__main__":
    unittest.main()
