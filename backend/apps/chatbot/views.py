from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is Chatbot API!")

# # Gọi frontend của chatbot
# def chatbot_view(request):
#     return render(request, "chatbot/chatbot.html")

#Upload file
def upload_document(request):
    if request.method == "POST" and request.FILES.get("document"):
        file = request.FILES["document"]
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        return render(request, "chatbot/chatbot.html", {"message": "Tải tài liệu thành công!"})
    return render(request, "chatbot/chatbot.html")

#API Chatbot với LLM
import requests
import json

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = "your_api_key_here"  # Thay bằng API key của bạn

def chatbot_view(request):
    return render(request, "chatbot/chatbot.html")

def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        if not user_message:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",  # Hoặc deepseek-coder nếu dùng code
            "messages": [{"role": "user", "content": user_message}]
        }

        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")
            return JsonResponse({"reply": reply})
        else:
            return JsonResponse({"error": "Failed to connect to DeepSeek API"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
