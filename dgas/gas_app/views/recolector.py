from braces.views import GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (
    DetailView, ListView, TemplateView,
    UpdateView, CreateView, DeleteView
)

from dgas.gas_app.models import Estacion


class CargaDashBoardListView(GroupRequiredMixin, ListView):

    # required
    group_required = u"Recolector"
    raise_exception = True
    model = Estacion
    context_object_name = 'estaciones'

    template_name = 'gas_app/recolector/carga_dash_board.html'
    context_object_name = 'estaciones'

    page = {
        'title': 'Clientes',
        'subtitle': 'Listado general'
    }

    def get_context_data(self, **kwargs):
        context = super(CargaDashBoardListView, self).get_context_data(**kwargs)
        context['page'] = self.page
        return context


class CargaTemplateView(GroupRequiredMixin, TemplateView):

    # required
    group_required = u"Recolector"
    raise_exception = True

    template_name = 'gas_app/recolector/carga.html'
    context_object_name = 'demo_list'

    page = {
        'title': 'Clientes',
        'subtitle': 'Listado general'
    }

    def get_context_data(self, **kwargs):
        context = super(CargaTemplateView, self).get_context_data(**kwargs)
        context['page'] = self.page
        context['estacion'] = Estacion.objects.get(pk=self.kwargs['estacion_id'])
        return context
