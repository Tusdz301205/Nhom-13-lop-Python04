import unittest
from datetime import datetime
from models.danh_gia_tour import DanhGiaTour


class TestDanhGiaTour(unittest.TestCase):
    def tao_danh_gia(self, **kwargs):
        du_lieu = dict(ma_danh_gia="DG01", ma_dat_tour="DT01", so_sao=5,
                       noi_dung="Chuyến đi rất tốt", thoi_diem_danh_gia=datetime(2026, 10, 10, 12, 0))
        du_lieu.update(kwargs)
        return DanhGiaTour(**du_lieu)

    def test_tao_hop_le(self):
        dg = self.tao_danh_gia()
        self.assertEqual(dg.so_sao, 5)
        self.assertEqual(dg.noi_dung, "Chuyến đi rất tốt")

    def test_so_sao_nho_hon_mot(self):
        with self.assertRaisesRegex(ValueError, "Số sao"):
            self.tao_danh_gia(so_sao=0)

    def test_so_sao_lon_hon_nam(self):
        with self.assertRaisesRegex(ValueError, "Số sao"):
            self.tao_danh_gia(so_sao=6)

    def test_bool_khong_duoc_coi_la_int(self):
        with self.assertRaisesRegex(ValueError, "Số sao"):
            self.tao_danh_gia(so_sao=True)

    def test_ma_trong(self):
        with self.assertRaisesRegex(ValueError, "Mã đặt tour"):
            self.tao_danh_gia(ma_dat_tour=" ")

    def test_sai_kieu_noi_dung(self):
        with self.assertRaisesRegex(ValueError, "Nội dung"):
            self.tao_danh_gia(noi_dung=123)

    def test_cap_nhat_so_sao(self):
        dg = self.tao_danh_gia()
        dg.cap_nhat_so_sao(4)
        self.assertEqual(dg.so_sao, 4)
        with self.assertRaises(ValueError):
            dg.cap_nhat_so_sao(9)
        self.assertEqual(dg.so_sao, 4)

    def test_cap_nhat_noi_dung(self):
        dg = self.tao_danh_gia()
        dg.cap_nhat_noi_dung("  Tốt  ")
        self.assertEqual(dg.noi_dung, "Tốt")


if __name__ == "__main__":
    unittest.main()
