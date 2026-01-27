
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Capteur(models.Model):
    nom = models.CharField(max_length=100)
    type_capteur = models.CharField(max_length=50)
    unite = models.CharField(max_length=20, blank=True)
    localisation = models.CharField(max_length=100, blank=True)

    seuil_min = models.FloatField(null=True, blank=True)
    seuil_max = models.FloatField(null=True, blank=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom
class Actionneur(models.Model):
    nom = models.CharField(max_length=100)
    type_actionneur = models.CharField(max_length=50)
    etat = models.BooleanField(default=False)
    derniere_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
class Mesure(models.Model):
    capteur = models.ForeignKey(
        Capteur,
        on_delete=models.CASCADE,
        related_name="mesures",
    )
    valeur = models.FloatField()
    horodatage = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["capteur"]),
            models.Index(fields=["horodatage"]),
        ]
    def __str__(self):
        return f"{self.capteur.nom} - {self.valeur} ({self.horodatage})"

class HistoriqueCommande(models.Model):
    actionneur = models.ForeignKey(
        Actionneur,
        on_delete=models.CASCADE,
        related_name="commandes",
    )
    commande = models.CharField(max_length=10)       # "ON" / "OFF"
    source = models.CharField(max_length=50)         # "front" / "auto" / "system"
    horodatage = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["actionneur"]),
            models.Index(fields=["horodatage"]),
        ]
    def __str__(self):
        return f"{self.actionneur.nom} - {self.commande} ({self.horodatage})"

class Alerte(models.Model):
    NIVEAU_CHOICES = [
        ("warning", "Warning"),
        ("critical", "Critical"),
    ]

    capteur = models.ForeignKey(
        Capteur,
        on_delete=models.CASCADE,
        related_name="alertes",
    )
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    message = models.CharField(max_length=255)
    horodatage = models.DateTimeField(auto_now_add=True)

    acquitte_par = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="alertes_acquittees",
    )
    acquitte_le = models.DateTimeField(null=True, blank=True)
    resolue = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["capteur"]),
            models.Index(fields=["niveau"]),
        ]
    def __str__(self):
        return f"{self.capteur.nom} - {self.niveau} ({self.horodatage})"

