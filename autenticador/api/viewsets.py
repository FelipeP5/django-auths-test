from rest_framework import viewsets, status
from autenticador.api import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from autenticador.api.serializers import BoxSerializer, CustomUserSerializer, LoginSerializer, Box, CustomUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class BoxViewset(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer

class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request):
        serializer = serializers.CustomUserSerializer(data=request.data)
        serializer.is_valid()
        senha_hash = make_password(serializer.validated_data["password"])
        serializer.validated_data["password"] = senha_hash
        return Response(CustomUser.objects.create(**serializer.validated_data), status.HTTP_201_CREATED)

class LoginViewset(viewsets.ViewSet):
    # O DefaultRouter espere nomes específico para essas funções
    # list, create, retrieve e etc. create define um POST para a URL
    def create(self, request):
    # Todo código abaixo é cópia do meu projeto anterior que é cópia do apifinanceiro, modificado
        serializer = LoginSerializer(data=request.data)
        # is_valid() observa se o valor conforma com o serializer,
        # preenchendo .validated_data se sim; .errors se não
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            email = serializer.validated_data["email"]
            # função definida em .backends
            user = authenticate(username = username, password = password, email = email)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                return Response({
                    'access': str(access_token),
                    'refresh': str(refresh),
                    'user': {
                        'userId': user.id,
                        'username': user.username,
                        'email': user.email,
                    }
                }, status= status.HTTP_200_OK)
            return Response(f"Falha na autenticação...\n Otário", status=status.HTTP_418_IM_A_TEAPOT) 
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)