from django.shortcuts import render

from django.http import JsonResponse

def document_list(request):
    return JsonResponse({"message": "Danh sách tài liệu"})
