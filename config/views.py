# -*- coding: utf-8 -*-
import datetime
from braces.views import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView
#from django.core.urlresolvers import reverse
from dgas.users.models import User
from django.db.models import Sum


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        '''
        total_dias = Vacacion.objects.filter(empleado_id=self.request.user.id).aggregate(Sum('nro_dias'))
        if total_dias['nro_dias__sum']:
            td = int(total_dias['nro_dias__sum'])
        else:
            td = 0

        total_dias_disfrutados = VacacionSolicitud.objects.filter(empleado_id=self.request.user.id).aggregate(
            Sum('nro_dias'))
        if total_dias_disfrutados['nro_dias__sum']:
            tdd = int(total_dias_disfrutados['nro_dias__sum'])
        else:
            tdd = 0

        context['total_por_disfrutar'] = td - tdd

        hoy = datetime.date.today()

        jornadas = Jornada.objects.filter(fecha_entrega__gte=hoy)
        context['jornadas'] = jornadas
        '''

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
