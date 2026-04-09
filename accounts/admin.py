from django.contrib import admin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('email', 'nom', 'prenom', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('email', 'nom', 'prenom')