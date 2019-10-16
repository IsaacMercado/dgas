# -*- coding: utf-8 -*-
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.conf import settings
from django.db.models import Sum
from django.middleware.csrf import rotate_token
from django.views.generic import RedirectView, TemplateView
from django.http import HttpResponse, JsonResponse
from django.views import View

from dgas.gas_app import models as md
from dgas.users import models as us
from dgas.supervisor_app import plots

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
        
        context["num_user"] = us.User.objects.count()
        context["num_vehiculos"] = md.Vehiculo.objects.count()
        context["num_atendidos"] = md.Cola.objects.filter(created_at__date__gt=dateinit).count()
        context["num_rebotados"] = md.Rebotado.objects.filter(created_at__date__gt=dateinit).count()
        
        context['estaciones'] = md.Estacion.objects.all()
        context['municipios'] = us.Municipio.objects.all()
        context['parroquias'] = us.Parroquia.objects.all()

        return context


class SupervisorPlots(GroupRequiredMixin, View):
    # required
    group_required = u"Supervisor"
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(SupervisorPlots, self).get_context_data(**kwargs)

        return context
    
    def get(self, request, *args, **kwargs):
        rangedate = request.GET.get('daterange','')
        municipio = request.GET.get('municipioPlot','')
        parroquia = request.GET.get('parroquiaPlot','')
        estacion = request.GET.get('estacionPlot','')
        
        content = 'No ha realizado ninguna consulta'
        params = {}
        
        if rangedate or municipio or parroquia or estacion:
            date_ini, date_end = str(rangedate).split(' - ')
            
            params["init"] = datetime.strptime(date_ini, '%d/%m/%Y')\
                            .replace(tzinfo=pytz.UTC).date()
            params["end"] = datetime.strptime(date_end, '%d/%m/%Y')\
                            .replace(tzinfo=pytz.UTC).date()
            
            if municipio:
                params["municipio"] = us.Municipio.objects.get(id=int(municipio))
            
            if parroquia:
                params["parroquia"] = us.Parroquia.objects.get(id=int(parroquia))
            
            if estacion:
                params["estacion"] = md.Estacion.objects.get(id=int(estacion))

            content = plots.plotly_consult(**params)

        response = HttpResponse(content)
        response["X-Frame-Options"] = "sameorigin"
        return response


