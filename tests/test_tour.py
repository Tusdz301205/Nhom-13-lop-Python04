"""Kiểm thử sản phẩm tour tham chiếu điểm đến qua mã."""

import unittest

from models.tour import Tour


class TestTour(unittest.TestCase):
    def tao_tour(self, **thay_doi):
        du_lieu = dict(ma_tour="T01", ten_tour="Tour Đà Lạt", ma_diem_den="DD01")
        du_lieu.update(thay_doi)
        return Tour(**du_lieu)

    def test_tao_tour_tham_chieu_bang_ma(self):
        tour = self.tao_tour(
            ma_tour=" T01 ", ten_tour=" Tour Đà Lạt ",
            ma_diem_den=" DD01 ", mo_ta=" 3 ngày 2 đêm ",
            trang_thai=" dang_kinh_doanh ",
        )
        self.assertEqual(
            (tour.ma_tour, tour.ten_tour, tour.ma_diem_den, tour.mo_ta),
            ("T01", "Tour Đà Lạt", "DD01", "3 ngày 2 đêm"),
        )
        self.assertTrue(tour.dang_kinh_doanh())
        self.assertFalse(hasattr(tour, "diem_den"))

    def test_chuoi_bat_buoc_khong_hop_le(self):
        for truong in ("ma_tour", "ten_tour", "ma_diem_den"):
            for gia_tri in ("", " \t ", None, 123, True, []):
                with self.subTest(truong=truong, gia_tri=gia_tri):
                    with self.assertRaises(ValueError):
                        self.tao_tour(**{truong: gia_tri})

    def test_trang_thai_khong_hop_le(self):
        for gia_tri in ("MO_BAN", "", None, 123, []):
            with self.subTest(gia_tri=gia_tri):
                with self.assertRaises(ValueError):
                    self.tao_tour(trang_thai=gia_tri)

    def test_mo_ta_khong_hop_le(self):
        for gia_tri in (None, 123, []):
            with self.subTest(gia_tri=gia_tri):
                with self.assertRaises(ValueError):
                    self.tao_tour(mo_ta=gia_tri)

    def test_cap_nhat_thong_tin(self):
        tour = self.tao_tour()
        tour.cap_nhat_thong_tin(" Tour mới ", " DD02 ", " Mô tả mới ")
        self.assertEqual(
            (tour.ma_tour, tour.ten_tour, tour.ma_diem_den, tour.mo_ta),
            ("T01", "Tour mới", "DD02", "Mô tả mới"),
        )
        truoc = vars(tour).copy()
        tour.cap_nhat_thong_tin()
        self.assertEqual(vars(tour), truoc)
        tour.cap_nhat_thong_tin(mo_ta="")
        self.assertEqual(tour.mo_ta, "")

    def test_cap_nhat_loi_khong_sua_do(self):
        for thay_doi in (
            dict(ten_tour=""),
            dict(ten_tour="Tên mới", ma_diem_den=" "),
            dict(ten_tour="Tên mới", ma_diem_den="DD02", mo_ta=123),
        ):
            with self.subTest(thay_doi=thay_doi):
                tour = self.tao_tour()
                truoc = vars(tour).copy()
                with self.assertRaises(ValueError):
                    tour.cap_nhat_thong_tin(**thay_doi)
                self.assertEqual(vars(tour), truoc)

    def test_ngung_kinh_doanh_va_chan_thao_tac_lap(self):
        tour = self.tao_tour()
        tour.ngung_kinh_doanh()
        self.assertFalse(tour.dang_kinh_doanh())
        self.assertEqual(tour.trang_thai, Tour.NGUNG_KINH_DOANH)
        with self.assertRaises(ValueError):
            tour.ngung_kinh_doanh()

    def test_khoi_tao_tour_da_ngung(self):
        tour = self.tao_tour(trang_thai=Tour.NGUNG_KINH_DOANH)
        self.assertFalse(tour.dang_kinh_doanh())


if __name__ == "__main__":
    unittest.main()
