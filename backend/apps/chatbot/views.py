from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# 🏷️ 1️⃣ **Chọn mô hình DeepSeek từ Hugging Face**
MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"  # Đổi tên mô hình nếu cần
print("🔄 Đang tải mô hình:", MODEL_NAME)

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")
    print("✅ Mô hình tải thành công!")
except Exception as e:
    print("❌ Lỗi khi tải mô hình:", e)

# 🏷️ 2️⃣ **Tạo pipeline xử lý ngôn ngữ tự nhiên**
# text_pipeline = pipeline(
#     "text-generation", model=model, tokenizer=tokenizer, 
#     max_new_tokens=200, do_sample=True, temperature=0.7
# )
text_pipeline = pipeline(
    "text-generation", 
    model=model, 
    tokenizer=tokenizer, 
    max_new_tokens=100,  # Giới hạn số token đầu ra
    do_sample=True, 
    temperature=0.7,
    top_k=50,  # Giảm mức độ "hành văn lặp lại"
    top_p=0.9  # Giúp mô hình tạo ra phản hồi tự nhiên hơn
)

llm = HuggingFacePipeline(pipeline=text_pipeline)

# 🏷️ 3️⃣ **Thiết lập bộ nhớ hội thoại**
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# 🏷️ 4️⃣ **Hàm xử lý hội thoại**
# def chatbot_response(user_input):
#     response = conversation.invoke(user_input)  # Sử dụng .invoke() thay vì .run()
#     return response
def chatbot_response(user_input):
    response = text_pipeline(user_input, max_new_tokens=100)[0]["generated_text"]
    
    # 🛠 Xóa phần nội dung prompt mặc định nếu có
    if "Current conversation" in response:
        response = response.split("Current conversation:")[-1].strip()

    return response


# ✅ **API chính**
@csrf_exempt  # Loại bỏ kiểm tra CSRF để dễ test
def chatbot_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            if not user_message:
                return JsonResponse({"error": "Message cannot be empty"}, status=400)

            bot_response = chatbot_response(user_message)  # Gọi mô hình LLM để trả lời

            return JsonResponse({"reply": bot_response})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

# ✅ **Giao diện chatbot**
def chatbot_view(request):
    return render(request, "chatbot/chatbot.html")

# ✅ **Upload tài liệu**
def upload_document(request):
    if request.method == "POST" and request.FILES.get("document"):
        file = request.FILES["document"]
        fs = FileSystemStorage()
        fs.save(file.name, file)
        return render(request, "chatbot/chatbot.html", {"message": "Tải tài liệu thành công!"})
    return render(request, "chatbot/chatbot.html")

# ✅ **Test chạy mô hình bằng Terminal**
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = chatbot_response(user_input)
        print(f"Bot: {response}")
