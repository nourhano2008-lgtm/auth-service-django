from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Utilisateur
from .utils import send_verification_email, send_reset_password_email, is_code_valid
from .serializers import VerifyEmailSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .serializers import (
    UtilisateurSerializer, InscriptionSerializer, ConnexionSerializer,
    EmailVerificationSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
)

# ========== Authentification ==========

class InscriptionView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = InscriptionSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'message': 'Inscription réussie',
                'user': UtilisateurSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ConnexionView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ConnexionSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success': True,
                    'user': UtilisateurSerializer(user).data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            return Response({'success': False, 'message': 'Email ou mot de passe incorrect'}, status=401)
        return Response({'success': False, 'errors': serializer.errors}, status=400)


class ProfilView(APIView):
    def get(self, request):
        return Response({'success': True, 'user': UtilisateurSerializer(request.user).data})


class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({'status': 'healthy', 'service': 'auth-service'})


# ========== Email Verification ==========

class SendVerificationCodeView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'success': False, 'message': 'Email requis'}, status=400)
        
        try:
            user = Utilisateur.objects.get(email=email)
            # Simulation d'envoi de code
            print(f"Code de vérification pour {email}: 123456")
            return Response({'success': True, 'message': 'Code de vérification envoyé'})
        except Utilisateur.DoesNotExist:
            return Response({'success': False, 'message': 'Utilisateur non trouvé'}, status=404)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
        if not email or not code:
            return Response({'success': False, 'message': 'Email et code requis'}, status=400)
        
        # Simulation de vérification (code accepté: 123456)
        if code == "123456":
            try:
                user = Utilisateur.objects.get(email=email)
                user.email_verified = True
                user.save()
                return Response({'success': True, 'message': 'Email vérifié avec succès'})
            except Utilisateur.DoesNotExist:
                pass
        
        return Response({'success': False, 'message': 'Code invalide'}, status=400)


# ========== Forgot / Reset Password ==========

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'success': False, 'message': 'Email requis'}, status=400)
        
        try:
            user = Utilisateur.objects.get(email=email)
            # Simulation d'envoi de code
            print(f"Code de réinitialisation pour {email}: 123456")
            return Response({'success': True, 'message': 'Code de réinitialisation envoyé'})
        except Utilisateur.DoesNotExist:
            # Sécurité: ne pas révéler si l'email existe
            return Response({'success': True, 'message': 'Si l\'email existe, un code a été envoyé'})


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        
        if not email or not code or not new_password:
            return Response({'success': False, 'message': 'Email, code et nouveau mot de passe requis'}, status=400)
        
        # Simulation (code accepté: 123456)
        if code == "123456":
            try:
                user = Utilisateur.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return Response({'success': True, 'message': 'Mot de passe réinitialisé avec succès'})
            except Utilisateur.DoesNotExist:
                pass
        
        return Response({'success': False, 'message': 'Code invalide'}, status=400)
    


 #========== Email Verification (حقيقي) ==========

class SendVerificationCodeView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'success': False, 'message': 'Email requis'}, status=400)
        
        try:
            user = Utilisateur.objects.get(email=email)
            if user.email_verified:
                return Response({'success': False, 'message': 'البريد مؤكد بالفعل'}, status=400)
            
            send_verification_email(user)
            return Response({'success': True, 'message': 'تم إرسال رمز التحقق إلى بريدك الإلكتروني'})
        except Utilisateur.DoesNotExist:
            return Response({'success': False, 'message': 'المستخدم غير موجود'}, status=404)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        
        if not email or not code:
            return Response({'success': False, 'message': 'Email et code requis'}, status=400)
        
        try:
            user = Utilisateur.objects.get(email=email)
            
            if user.verification_code != code:
                return Response({'success': False, 'message': 'رمز غير صحيح'}, status=400)
            
            if not is_code_valid(user.verification_code_created_at):
                return Response({'success': False, 'message': 'انتهت صلاحية الرمز'}, status=400)
            
            user.email_verified = True
            user.verification_code = None
            user.verification_code_created_at = None
            user.save()
            
            return Response({'success': True, 'message': 'تم تأكيد بريدك الإلكتروني بنجاح'})
        except Utilisateur.DoesNotExist:
            return Response({'success': False, 'message': 'المستخدم غير موجود'}, status=404)


# ========== Forgot / Reset Password (حقيقي) ==========

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'success': False, 'message': 'Email requis'}, status=400)
        
        try:
            user = Utilisateur.objects.get(email=email)
            send_reset_password_email(user)
            return Response({'success': True, 'message': 'تم إرسال رمز إعادة التعيين إلى بريدك الإلكتروني'})
        except Utilisateur.DoesNotExist:
            # لأسباب أمنية، لا نخبر المستخدم إذا كان الإيميل موجوداً
            return Response({'success': False, 'message': 'المستخدم غير موجود'}, status=404)


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('new_password')
        
        if not email or not code or not new_password:
            return Response({'success': False, 'message': 'Email, code et nouveau mot de passe requis'}, status=400)
        
        try:
            user = Utilisateur.objects.get(email=email)
            
            if user.reset_password_code != code:
                return Response({'success': False, 'message': 'رمز غير صحيح'}, status=400)
            
            if not is_code_valid(user.reset_password_code_created_at):
                return Response({'success': False, 'message': 'انتهت صلاحية الرمز'}, status=400)
            
            user.set_password(new_password)
            user.reset_password_code = None
            user.reset_password_code_created_at = None
            user.save()
            
            return Response({'success': True, 'message': 'تم تغيير كلمة المرور بنجاح'})
        except Utilisateur.DoesNotExist:
            return Response({'success': False, 'message': 'المستخدم غير موجود'}, status=404)
