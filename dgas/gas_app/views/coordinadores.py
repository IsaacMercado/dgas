# -*- coding: utf-8 -*-
import datetime
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.conf import settings
from django.db.models import Sum
from django.middleware.csrf import rotate_token
from django.views.generic import RedirectView, TemplateView

from dgas.gas_app.models import Estacion
from dgas.users.models import User


class Colas(GroupRequiredMixin, TemplateView):
    # required
    group_required = u"Coordinador"
    raise_exception = True

    template_name = "gas_app/coordinadores/colas.html"

    def get_context_data(self, **kwargs):
        context = super(Colas, self).get_context_data(**kwargs)

        return context


class ColasIslas(GroupRequiredMixin, TemplateView):
    # required
    group_required = u"Coordinador"
    raise_exception = True

    template_name = "gas_app/coordinadores/colas_v2.html"

    def get_context_data(self, **kwargs):
        context = super(ColasIslas, self).get_context_data(**kwargs)

        return context
