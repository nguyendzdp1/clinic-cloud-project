from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),      # Đường dẫn gốc (Trang chủ)
    path('chat/', views.chat_ai, name='chat_ai'), # Đường dẫn trang Chat
]