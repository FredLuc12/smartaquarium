from django.contrib import admin
from .models import Capteur, Mesure, Actionneur, HistoriqueCommande, Alerte

# admin.site.register(Capteur)
# admin.site.register(Mesure)
# admin.site.register(Actionneur)
# admin.site.register(HistoriqueCommande)
# admin.site.register(Alerte)


@admin.register(Capteur)
class CapteurAdmin(admin.ModelAdmin):
    list_display = ("nom", "type_capteur", "actif")
    list_filter = ("actif", "type_capteur")
    search_fields = ("nom",)

@admin.register(Mesure)
class MesureAdmin(admin.ModelAdmin):
    list_display = ("capteur", "valeur", "horodatage")
    list_filter = ("capteur",)
    date_hierarchy = "horodatage"

@admin.register(Actionneur)
class ActionneurAdmin(admin.ModelAdmin):
    list_display = ("nom", "type_actionneur", "etat")

@admin.register(HistoriqueCommande)
class HistoriqueCommandeAdmin(admin.ModelAdmin):
    list_display = ("actionneur", "commande", "source", "horodatage")
    list_filter = ("source",)

@admin.register(Alerte)
class AlerteAdmin(admin.ModelAdmin):
    list_display = ("capteur", "niveau", "resolue", "horodatage")
    list_filter = ("niveau", "resolue")
