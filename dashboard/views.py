from django.shortcuts import render

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

from django.http import JsonResponse
from .models import SensorData

def sensors_api(request):
    data = list(SensorData.objects.values().order_by('-created_at')[:10])
    return JsonResponse(data, safe=False)