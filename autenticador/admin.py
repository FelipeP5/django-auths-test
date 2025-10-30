from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from autenticador.models import CustomUser

admin.site.register(CustomUser, UserAdmin)