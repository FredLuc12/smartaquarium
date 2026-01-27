from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import SensorData


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SensorData
from .forms import ProfileForm

@login_required
def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")

@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès")
            return redirect("profile")  # 🔴 TRÈS IMPORTANT
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "dashboard/profile.html", {"form": form})

@login_required
def capteur_view(request):
    """
    Vue purement front pour l’instant : on affiche juste la page capteurs.
    Le backend branchera plus tard la vraie liste via le contexte ou une API.
    """
    # pour l’instant on ne passe rien de spécial, le template gèrera l’état “vide”
    return render(request, "dashboard/sensors.html")

@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html")

def sensors_api(request):
    data = list(SensorData.objects.values().order_by("-created_at")[:10])
    return JsonResponse(data, safe=False)
