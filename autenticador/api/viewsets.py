from rest_framework import viewsets, status
from autenticador.api import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from autenticador.api.serializers import BoxSerializer, CustomUserSerializer, LoginSerializer, Box, CustomUser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

class BoxViewset(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [AllowAny]

class CustomUserViewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = serializers.CustomUserSerializer(data=request.data)
        # O código aqui estava errado, o .create é para criar o obj na db,
        # Retorná-lo no Response() dá erro de serialização, pois é dem tipo complexo
        # https://www.django-rest-framework.org/api-guide/responses/#response
        if serializer.is_valid():
            senha_hash = make_password(serializer.validated_data["password"])
            serializer.validated_data["password"] = senha_hash
            CustomUser.objects.create(**serializer.validated_data)
            return Response(serializer.validated_data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

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
                refresh_token = RefreshToken.for_user(user)
                access_token = refresh_token.access_token
                body = {
                    'access': str(access_token),
                    'refresh': str(refresh_token),
                    'user': {
                        'userId': user.id,
                        'username': user.username,
                        'email': user.email,
                    }
                }
                # Criando o obj Response e guardando tokens em cookies
                response = Response(body, status.HTTP_200_OK)
                response.set_cookie("access_token", access_token)
                response.set_cookie("refresh_token", refresh_token)
                return response
            return Response(f"Falha na autenticação...\n Otário", status=status.HTTP_418_IM_A_TEAPOT) 
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)