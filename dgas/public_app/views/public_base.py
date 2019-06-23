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


class Publico(TemplateView):
    template_name = "dash_publico.html"

    def get_context_data(self, **kwargs):
        context = super(Publico, self).get_context_data(**kwargs)
        #scontext['key'] = settings.MAP_KEY # env.db("MAP_KEY")
        return context


class Estaciones(TemplateView):
    template_name = "public_app/estaciones.html"

    def get_context_data(self, **kwargs):
        context = super(Estaciones, self).get_context_data(**kwargs)
        #scontext['key'] = settings.MAP_KEY # env.db("MAP_KEY")
        return context


class ColasTemplateView(TemplateView):
    template_name = "public_app/colas_publico.html"

    def get_context_data(self, **kwargs):
        context = super(ColasTemplateView, self).get_context_data(**kwargs)

        return context


class ColasHistorioTemplateView(TemplateView):
    template_name = "public_app/colas_publico_historico.html"

    def get_context_data(self, **kwargs):
        context = super(ColasHistorioTemplateView, self).get_context_data(**kwargs)

        return context
