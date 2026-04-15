from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentification
    path('inscription/', views.InscriptionView.as_view(), name='inscription'),
    path('connexion/', views.ConnexionView.as_view(), name='connexion'),
    path('profil/', views.ProfilView.as_view(), name='profil'),
    path('health/', views.HealthCheckView.as_view(), name='health'),
    
    # Email Verification
    path('send-verification-code/', views.SendVerificationCodeView.as_view(), name='send_verification_code'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),
    
    # Forgot / Reset Password
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
]