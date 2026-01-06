from django.contrib import admin
from .models import SanPham, BacSi, LichHen, HoSoBenhAn

# Đăng ký các bảng để quản lý
admin.site.register(SanPham)
admin.site.register(BacSi)
admin.site.register(LichHen)
admin.site.register(HoSoBenhAn)