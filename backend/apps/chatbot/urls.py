from django.urls import path
from . import views  # Kiểm tra xem `views.py` có tồn tại không

urlpatterns = [
    path('', views.index, name='chatbot_home'),  # Thay `index` bằng view phù hợp
]