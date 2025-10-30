# https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#authentication-backends

# O authenticate do ModelBackend é restrito ao
# username (ou USERNAME_FIELD) e o password
# aqui desejamos fazer: username || email && password

from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from autenticador.models import CustomUser
from django.contrib.auth.hashers import check_password

class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, email=None, password=None):
        try:
            user = CustomUser._default_manager.get(Q(username=username) | Q(email=email))
        except CustomUser.DoesNotExist:
            # isso faz o hashing da senha mesmo na falha, impedindo que
            # um atacante observe as senhas existentes olhando o tempo
            # de resposta, segurança.
            CustomUser().set_password(password)
        else:
            if user.check_password(password):
                return user
        
