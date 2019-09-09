from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from model_utils import Choices


NAC_CHOICES = Choices('V', 'E')


class Municipio (models.Model):
    municipio = models.CharField(max_length=100)

    def __str__(self):
        return self.municipio


class Parroquia (models.Model):
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, null=True, blank=True)
    parroquia = models.CharField(max_length=100)

    def __str__(self):
        return self.parroquia


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    nacionalidad = models.CharField(max_length=2, choices=NAC_CHOICES, default='V')
    cedula = models.CharField('Cedula de identidad', max_length=16, default='')
    telefono_celular = models.CharField('Teléfono celular', max_length=16, null=True, blank=True, default='')
    direccion_base = models.TextField('Dirección de habitación', blank=True, max_length=128, default='')
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True)
    parroquia = models.ForeignKey(Parroquia, on_delete=models.SET_NULL, null=True, blank=True)

    photo_user = VersatileImageField(_('Foto del perfil'), upload_to='images/photo_user', blank=True, null=True)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class GasUser(User):
    USUARIO_TIPO_CHOICES = Choices('Gerente', 'Recolector')
    direccion = models.TextField('Dirección de habitación', blank=True, max_length=128, default='')
    telefono = models.CharField('Teléfono', max_length=16, null=True, blank=True, default='')

    created = models.DateTimeField(auto_now=True, blank=True)
    modificated = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        verbose_name = 'Usuario de Dgas'
        verbose_name_plural = 'Usuarios de Gas'

    def __str__(self):
        return u"%s" % self.first_name
