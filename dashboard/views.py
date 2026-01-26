from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SensorData


@login_required
def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")


def sensors_api(request):
    data = list(SensorData.objects.values().order_by("-created_at")[:10])
    return JsonResponse(data, safe=False)
