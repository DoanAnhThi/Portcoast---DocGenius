from django.urls import path, include
from . import views  # Kiểm tra xem `views.py` có tồn tại không

urlpatterns = [
    path('dashboard/', include('apps.dashboard.urls')),
]