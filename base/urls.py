# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),      # Đường dẫn gốc (Trang chủ)
#     path('chat/', views.chat_ai, name='chat_ai'), # Đường dẫn trang Chat
# ]

from django.urls import path
from django.contrib.auth import views as auth_views # Import view có sẵn của Django
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('chat/', views.chat_ai, name='chat_ai'),
    
    # --- PHẦN TÀI KHOẢN MỚI THÊM ---
    path('register/', views.register, name='register'), # Trang đăng ký (Tự viết)
    path('login/', auth_views.LoginView.as_view(template_name='base/login.html'), name='login'), # Trang đăng nhập (Có sẵn)
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'), # Đăng xuất xong về trang chủ
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('redirect/', views.post_login_redirect, name='post_login_redirect'), # <-- Đường dẫn điều hướng
    path('dat-lich/<int:pk>/', views.dat_lich, name='dat_lich'), # <int:pk> là ID của bác sĩ
]