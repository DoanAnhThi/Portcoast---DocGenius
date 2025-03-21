"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.chatbot.views import home, upload_document, chatbot_view, chatbot_api  # Import hàm home từ chatbot


# from django.shortcuts import redirect

# def home_redirect(request):
#     return redirect('/chatbot/')  # Chuyển hướng đến chatbot


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home),
    path("chatbot/upload/", upload_document, name="upload_document"),
    path("api/chatbot/", chatbot_api, name="chatbot_api"),
    path("chatbot/", chatbot_view, name="chatbot"),
]

# urlpatterns = [
#     path('', home_redirect),  # Thêm route này
#     path('admin/', admin.site.urls),
#     path('chatbot/', home),
# ]
