from django.db import models
from django.contrib.auth.models import User, UserManager

class PerfilDeUsuario(models.Model):
    user = models.OneToOneField(User)
    dni = models.IntegerField()

