# -*- coding: utf-8 -*-
import datetime
from braces.views import LoginRequiredMixin
from django.conf import settings
from django.db.models import Sum
from django.middleware.csrf import rotate_token
from django.views.generic import RedirectView, TemplateView

from dgas.gas_app.models import Estacion
# from django.core.urlresolvers import reverse
from dgas.users.models import User


class Estaciones(TemplateView):
    template_name = "public_app/estaciones.html"

    def get_context_data(self, **kwargs):
        context = super(Estaciones, self).get_context_data(**kwargs)
        context['key'] = settings.MAP_KEY # env.db("MAP_KEY")
        return context


class Colas(TemplateView):
    template_name = "public_app/colas.html"

    def get_context_data(self, **kwargs):
        context = super(Colas, self).get_context_data(**kwargs)

        return context
