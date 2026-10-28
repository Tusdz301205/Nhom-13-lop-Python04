import unittest
from datetime import datetime, timedelta
from models.yeu_cau_huy import YeuCauHuy


class TestYeuCauHuy(unittest.TestCase):
    def setUp(self):
        self.thoi_diem = datetime(2026, 10, 1, 9, 0)

    def tao_yc(self):
        return YeuCauHuy("YC01", "DT01", "Thay đổi kế hoạch", self.thoi_diem)

    def test_tao_cho_xu_ly(self):
        self.assertTrue(self.tao_yc().dang_cho_xu_ly())

    def test_chap_nhan_hop_le(self):
        yc = self.tao_yc()
        yc.chap_nhan("NV01", self.thoi_diem + timedelta(hours=1))
        self.assertEqual(yc.trang_thai, "CHAP_NHAN")

    def test_khong_duyet_hai_lan(self):
        yc = self.tao_yc()
        yc.chap_nhan("NV01", self.thoi_diem + timedelta(hours=1))
        with self.assertRaisesRegex(ValueError, "đã được xử lý"):
            yc.chap_nhan("NV02", self.thoi_diem + timedelta(hours=2))

    def test_thoi_diem_xu_ly_truoc_yeu_cau_khi_duyet(self):
        with self.assertRaisesRegex(ValueError, "không được trước"):
            self.tao_yc().chap_nhan("NV01", self.thoi_diem - timedelta(seconds=1))

    def test_constructor_tu_choi_thoi_gian_sai(self):
        with self.assertRaisesRegex(ValueError, "không được trước"):
            YeuCauHuy("YC01", "DT01", "Ly do", self.thoi_diem,
                      trang_thai="TU_CHOI", ma_nguoi_xu_ly="NV01",
                      thoi_diem_xu_ly=self.thoi_diem - timedelta(seconds=1),
                      ly_do_tu_choi="Không đủ điều kiện")

    def test_tu_choi_phai_co_ly_do(self):
        with self.assertRaisesRegex(ValueError, "Lý do từ chối"):
            self.tao_yc().tu_choi("NV01", self.thoi_diem + timedelta(hours=1), "  ")

    def test_constructor_tu_choi_thieu_ly_do(self):
        with self.assertRaisesRegex(ValueError, "lý do từ chối"):
            YeuCauHuy("YC01", "DT01", "Ly do", self.thoi_diem,
                      trang_thai="TU_CHOI", ma_nguoi_xu_ly="NV01",
                      thoi_diem_xu_ly=self.thoi_diem, ly_do_tu_choi=None)

    def test_tu_choi_hop_le(self):
        yc = self.tao_yc()
        yc.tu_choi("NV01", self.thoi_diem, "Ngoài thời hạn")
        self.assertEqual(yc.trang_thai, "TU_CHOI")
        self.assertEqual(yc.ly_do_tu_choi, "Ngoài thời hạn")


if __name__ == "__main__":
    unittest.main()
