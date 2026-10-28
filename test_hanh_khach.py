import unittest
from models.hanh_khach import HanhKhach


class TestHanhKhach(unittest.TestCase):
    def test_tao_hop_le(self):
        hk = HanhKhach("HK01", "DT01", "Tran Binh", "0987654321")
        self.assertTrue(hk.kiem_tra_hop_le())

    def test_thieu_ho_ten(self):
        with self.assertRaisesRegex(ValueError, "Họ tên"):
            HanhKhach("HK01", "DT01", "   ")

    def test_ma_dat_tour_trong(self):
        with self.assertRaisesRegex(ValueError, "Mã đặt tour"):
            HanhKhach("HK01", "   ", "Tran Binh")

    def test_so_dien_thoai_sai(self):
        with self.assertRaisesRegex(ValueError, "Số điện thoại"):
            HanhKhach("HK01", "DT01", "Tran Binh", "abc")

    def test_so_dien_thoai_tuy_chon(self):
        self.assertIsNone(HanhKhach("HK01", "DT01", "Tran Binh", "").so_dien_thoai)

    def test_cap_nhat_khong_cap_nhat_do(self):
        hk = HanhKhach("HK01", "DT01", "Tran Binh", "0987654321")
        with self.assertRaises(ValueError):
            hk.cap_nhat_thong_tin(ho_ten="Ten moi", so_dien_thoai="sai")
        self.assertEqual(hk.ho_ten, "Tran Binh")
        self.assertEqual(hk.so_dien_thoai, "0987654321")


if __name__ == "__main__":
    unittest.main()
