# -*- coding: utf-8 -*-
import json
from braces.views import GroupRequiredMixin, LoginRequiredMixin
from datetime import datetime
from datetime import timedelta
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    DetailView, ListView,
    UpdateView, CreateView, DeleteView
)
from django.views.generic import View
from pure_pagination.mixins import PaginationMixin

from dgas.gas_app.models import Combustible, Estacion, Vehiculo, Cola
from pure_pagination.mixins import PaginationMixin


class ColasListView(LoginRequiredMixin, PaginationMixin, ListView):
    paginate_by = 5

    model = Cola
    context_object_name = 'colas'
    template_name = 'users_app/colas/colas_list.html'

    page = {
        'title': 'Mis cargas',
        'subtitle': 'Listado general'
    }

    def get_queryset(self):

        vehiculos = Vehiculo.objects.filter(usuario_id=self.request.user.id)

        return Cola.objects.filter(vehiculo__in=vehiculos)

    def get_context_data(self, **kwargs):
        context = super(ColasListView, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context
