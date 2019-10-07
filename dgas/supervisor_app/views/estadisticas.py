# -*- coding: utf-8 -*-
import datetime
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.conf import settings
from django.db.models import Sum
from django.middleware.csrf import rotate_token
from django.views.generic import RedirectView, TemplateView

from dgas.gas_app import models as md
from dgas.users.models import User

import pytz
from datetime import datetime


class SupervisorEstadisticas(GroupRequiredMixin, TemplateView):
    # required
    group_required = u"Supervisor"
    raise_exception = True

    template_name = "supervisor_app/supervisor_estadisticas/list.html"

    def get_context_data(self, **kwargs):
        context = super(SupervisorEstadisticas, self).get_context_data(**kwargs)
        
        datenow = datetime.now()
        dateinit = datetime(datenow.year, datenow.month, datenow.day, tzinfo=pytz.UTC)
        
        context["num_user"] = User.objects.count()
        context["num_vehiculos"] = md.Vehiculo.objects.count()
        context["num_atendidos"] = md.Cola.objects.filter(created_at__gt=dateinit).count()
        context["num_rebotados"] = md.Rebotado.objects.filter(created_at__gt=dateinit).count()

        return context
