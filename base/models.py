from django.db import models
from django.contrib.auth.models import User

# 1. Bảng Sản phẩm (Thuốc & Thực phẩm chức năng)
class SanPham(models.Model):
    ten_san_pham = models.CharField(max_length=200, verbose_name="Tên thuốc/TPCN")
    gia = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá bán (VNĐ)")
    mo_ta = models.TextField(blank=True, verbose_name="Công dụng/Mô tả")
    hinh_anh = models.ImageField(upload_to='san_pham/', blank=True, null=True, verbose_name="Ảnh sản phẩm")
    
    def __str__(self):
        return self.ten_san_pham

# 2. Bảng Bác sĩ (Liên kết với tài khoản User)
class BacSi(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Tài khoản")
    chuyen_khoa = models.CharField(max_length=100, verbose_name="Chuyên khoa")
    gioi_thieu = models.TextField(blank=True, verbose_name="Giới thiệu bác sĩ")
    anh_dai_dien = models.ImageField(upload_to='bac_si/', blank=True, null=True)

    def __str__(self):
        return f"Bác sĩ {self.user.last_name} {self.user.first_name}"

# 3. Bảng Lịch hẹn khám
class LichHen(models.Model):
    TRANG_THAI_CHOICES = [
        ('CHO_DUYET', 'Chờ duyệt'),
        ('DA_DUYET', 'Đã duyệt'),
        ('DA_KHAM', 'Đã khám'),
        ('HUY', 'Hủy bỏ'),
    ]
    
    benh_nhan = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lich_kham', verbose_name="Bệnh nhân")
    bac_si = models.ForeignKey(BacSi, on_delete=models.SET_NULL, null=True, verbose_name="Bác sĩ phụ trách")
    ngay_gio = models.DateTimeField(verbose_name="Ngày giờ khám")
    trieu_chung = models.TextField(verbose_name="Triệu chứng ban đầu")
    trang_thai = models.CharField(max_length=20, choices=TRANG_THAI_CHOICES, default='CHO_DUYET')
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lịch khám: {self.benh_nhan.username} - {self.ngay_gio}"

# 4. Bảng Hồ sơ bệnh án (Quan trọng cho đề tài y tế)
class HoSoBenhAn(models.Model):
    lich_hen = models.OneToOneField(LichHen, on_delete=models.CASCADE, verbose_name="Theo lịch hẹn")
    chuan_doan = models.TextField(verbose_name="Chẩn đoán của bác sĩ")
    don_thuoc = models.TextField(verbose_name="Đơn thuốc / Lời dặn")
    file_ket_qua = models.FileField(upload_to='ket_qua_kham/', blank=True, null=True, verbose_name="File kết quả (X-Quang/Siêu âm)")
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Hồ sơ: {self.lich_hen.benh_nhan.username}"