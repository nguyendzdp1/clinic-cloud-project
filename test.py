import google.generativeai as genai
import os

# 1. Điền trực tiếp Key của bạn vào đây để test (thay thế dòng trong ngoặc)
MY_API_KEY = "AIzaSyAc6MeCQaAE7KmS-tDbbRJzyOypfkFqy6o"  
genai.configure(api_key=MY_API_KEY)

print("Dang ket noi voi Google AI...")

try:
    print("Danh sach cac Model ban duoc phep dung:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            
    # Test thu mot phat
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Xin chao")
    print(f"\nTest thu nghiem thanh cong: {response.text}")

except Exception as e:
    print(f"\nLOI ROI: {e}")