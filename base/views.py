from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import SanPham, BacSi # <-- Quan trọng: Phải import model để trang chủ dùng
import google.generativeai as genai
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BacSi, LichHen

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

# ==========================================
# 3. CHỨC NĂNG ĐĂNG KÝ TÀI KHOẢN
# ==========================================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Lưu người dùng mới vào Database
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản {username} đã được tạo! Hãy đăng nhập.')
            return redirect('login') # Chuyển hướng sang trang đăng nhập
    else:
        form = UserCreationForm()
    
    return render(request, 'base/register.html', {'form': form})



@login_required
def doctor_dashboard(request):
    # 1. Kiểm tra có phải bác sĩ không
    if not hasattr(request.user, 'bacsi'):
        return redirect('home')
    
    bac_si = request.user.bacsi # Lấy thông tin bác sĩ đang đăng nhập
    
    # 2. Lấy danh sách lịch hẹn CỦA RIÊNG BÁC SĨ ĐÓ
    # Sắp xếp lịch mới nhất lên đầu (-ngay_tao)
    ds_lich_hen = LichHen.objects.filter(bac_si=bac_si).order_by('-ngay_gio')
    
    context = {
        'bac_si': bac_si,
        'ds_lich_hen': ds_lich_hen
    }
    return render(request, 'base/doctor_dashboard.html', context)

# --- Hàm mới: Xử lý nút Duyệt/Hủy ---
@login_required
def duyet_lich(request, pk, trang_thai):
    # Lấy lịch hẹn theo ID
    lich_hen = get_object_or_404(LichHen, pk=pk)
    
    # Bảo mật: Chỉ bác sĩ phụ trách mới được duyệt
    if not hasattr(request.user, 'bacsi') or lich_hen.bac_si != request.user.bacsi:
        messages.error(request, "Bạn không có quyền duyệt lịch này!")
        return redirect('doctor_dashboard')

    # Cập nhật trạng thái
    if trang_thai == 'duyet':
        lich_hen.trang_thai = 'DA_DUYET'
        messages.success(request, f"Đã duyệt lịch khám cho {lich_hen.benh_nhan.username}")
    elif trang_thai == 'huy':
        lich_hen.trang_thai = 'HUY'
        messages.warning(request, "Đã hủy lịch khám.")
        
    lich_hen.save()
    return redirect('doctor_dashboard')
    
    
@login_required
def post_login_redirect(request):
    user = request.user

    # 1. Nếu là Admin -> Vào trang quản trị
    if user.is_superuser:
        return redirect('/admin/')
    
    # 2. Nếu là Bác sĩ -> Vào Dashboard bác sĩ
    # (Kiểm tra xem user này có liên kết với bảng BacSi không)
    elif hasattr(user, 'bacsi'): 
        return redirect('doctor_dashboard')
    
    # 3. Còn lại là Khách hàng -> Về trang chủ đặt lịch
    else:
        return redirect('home')
    
    

@login_required(login_url='login') # Chưa đăng nhập thì đá về trang login
def dat_lich(request, pk):
    bac_si = get_object_or_404(BacSi, pk=pk) # Lấy thông tin bác sĩ theo ID
    
    if request.method == 'POST':
        ngay_gio = request.POST.get('ngay_gio')
        trieu_chung = request.POST.get('trieu_chung')
        
        # Lưu vào Database
        LichHen.objects.create(
            benh_nhan=request.user,
            bac_si=bac_si,
            ngay_gio=ngay_gio,
            trieu_chung=trieu_chung,
            trang_thai='CHO_DUYET' # Mặc định là chờ duyệt
        )
        
        messages.success(request, 'Đã gửi yêu cầu đặt lịch thành công!')
        return redirect('home') # Hoặc chuyển hướng đến trang quản lý lịch cá nhân
        
    return render(request, 'base/booking_form.html', {'bac_si': bac_si})