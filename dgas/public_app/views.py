# -*- coding: utf-8 -*-
import datetime
from braces.views import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView
#from django.core.urlresolvers import reverse
from dgas.users.models import User
from django.db.models import Sum
from dgas.gas_app.models import Estacion


class Estaciones(TemplateView):
    template_name = "public_app/estaciones.html"

    def get_context_data(self, **kwargs):
        context = super(Estaciones, self).get_context_data(**kwargs)
        return context
