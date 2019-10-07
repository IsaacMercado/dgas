# -*- coding: utf-8 -*-
import datetime
from braces.views import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView
#from django.core.urlresolvers import reverse
from dgas.users.models import User
from django.db.models import Sum
from dgas.gas_app.models import Estacion


class Dashboard(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        if self.request.user.groups.filter(name='Estacion').exists():
            #context['estaciones'] = Estacion.objects.filter(usuario_id=self.request.user.id)
            context['estaciones'] = Estacion.objects.all()

        if self.request.user.groups.filter(name='Recolector').exists():
            context['estaciones'] = Estacion.objects.all()


        return context


class Profile(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self):

        user = User.objects.get(id=self.request.user.id)
        #if user.groups.filter(name='VentasCliente').exists():
        #    return reverse('clientesalmacen_dash_view')
        #else:
        #    return reverse('dashboard')
