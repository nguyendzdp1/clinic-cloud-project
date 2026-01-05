from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import SanPham, BacSi # <-- Quan trọng: Phải import model để trang chủ dùng
import google.generativeai as genai

# Cấu hình AI
try:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
except AttributeError:
    print("Cảnh báo: Chưa cấu hình GOOGLE_API_KEY trong settings.py")

# ==========================================
# 1. CHỨC NĂNG TRANG CHỦ (HOME)
# ==========================================
def home(request):
    # Lấy dữ liệu từ Database để hiển thị
    ds_bac_si = BacSi.objects.all()
    ds_san_pham = SanPham.objects.all()
    
    context = {
        'ds_bac_si': ds_bac_si,
        'ds_san_pham': ds_san_pham
    }
    return render(request, 'base/home.html', context)

# ==========================================
# 2. CHỨC NĂNG CHAT AI (GEMINI)
# ==========================================
def chat_ai(request):
    # Nếu là yêu cầu gửi câu hỏi (POST)
    if request.method == 'POST':
        user_message = request.POST.get('message')
        
        try:
            # A. Khởi tạo mô hình
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # B. Tạo ngữ cảnh cho bác sĩ ảo
            context = """
            Bạn là trợ lý y tế ảo của Phòng khám Cloud. 
            Hãy trả lời ngắn gọn, thân thiện và tập trung vào vấn đề sức khỏe.
            Luôn kèm theo câu: "Lời khuyên này chỉ mang tính tham khảo."
            """
            
            # C. Gửi câu hỏi cho AI
            full_prompt = f"{context}\nNgười dùng hỏi: {user_message}"
            response = model.generate_content(full_prompt)
            
            # D. Trả về kết quả
            return JsonResponse({'status': 'success', 'reply': response.text})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'reply': f'Lỗi kết nối AI: {str(e)}'})

    # Nếu là truy cập bình thường (GET) -> Hiện giao diện chat
    return render(request, 'base/chat.html')