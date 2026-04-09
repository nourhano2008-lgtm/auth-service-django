from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('inscription/', views.InscriptionView.as_view(), name='inscription'),
    path('connexion/', views.ConnexionView.as_view(), name='connexion'),
    path('profil/', views.ProfilView.as_view(), name='profil'),
    path('health/', views.HealthCheckView.as_view(), name='health'),
]