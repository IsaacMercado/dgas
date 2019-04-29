from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
from model_utils import Choices


class User(AbstractUser):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    photo_user = VersatileImageField(_('Photo user'), upload_to='images/photo_user', blank=True, null=True)

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
