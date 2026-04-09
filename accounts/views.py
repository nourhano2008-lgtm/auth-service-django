from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Utilisateur
from .serializers import UtilisateurSerializer, InscriptionSerializer, ConnexionSerializer


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
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ConnexionView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = ConnexionSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'success': True,
                    'message': 'Connexion réussie',
                    'user': UtilisateurSerializer(user).data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                })
            else:
                return Response({
                    'success': False,
                    'message': 'Email ou mot de passe incorrect'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfilView(APIView):
    def get(self, request):
        serializer = UtilisateurSerializer(request.user)
        return Response({
            'success': True,
            'user': serializer.data
        })


class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'auth-service',
            'version': '1.0.0'
        })