from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'email', 'nom', 'prenom', 'role', 'telephone', 'entreprise', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class InscriptionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Utilisateur
        fields = ['email', 'nom', 'prenom', 'role', 'password', 'password_confirm', 'telephone', 'entreprise']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = Utilisateur(**validated_data)
        user.set_password(password)
        user.save()
        from .utils import send_verification_email
        send_verification_email(user)
        return user
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = Utilisateur(**validated_data)
        user.set_password(password)
        user.email_verified = False  # ⬅️ أضف هذا
        user.save()
        
        # ⬅️ أضف هذا - إرسال رمز التحقق تلقائياً
        from .utils import send_verification_email
        send_verification_email(user)
        
        return user


class ConnexionSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # أضف في نهاية الملف

class EmailVerificationSerializer(serializers.Serializer):
    """Serialiser للتحقق من البريد الإلكتروني"""
    email = serializers.EmailField(required=True)
    code = serializers.CharField(max_length=6, required=True)


class ResendVerificationCodeSerializer(serializers.Serializer):
    """Serialiser لإعادة إرسال رمز التحقق"""
    email = serializers.EmailField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    """Serialiser لطلب إعادة تعيين كلمة المرور"""
    email = serializers.EmailField(required=True)


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(max_length=6, required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "كلمتا المرور غير متطابقتين"})
        return attrs








    