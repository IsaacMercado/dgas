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

from dgas.gas_app.models import Combustible, Estacion, Vehiculo
from pure_pagination.mixins import PaginationMixin


class VehiculoListView(LoginRequiredMixin, PaginationMixin, ListView):
    paginate_by = 5

    model = Vehiculo
    context_object_name = 'vehiculos'
    template_name = 'public_app/vehiculos/vehiculos_list.html'

    page = {
        'title': 'Vehiculos',
        'subtitle': 'Listado general'
    }

    def get_queryset(self):

        return Vehiculo.objects.filter(usuario_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(VehiculoListView, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context


class VehiculoCreateView(LoginRequiredMixin, CreateView):

    model = Vehiculo
    template_name = 'public_app/vehiculos/vehiculo_form.html'

    fields = ['placa', 'cedula', 'tipo_vehiculo', 'cilindros']

    page = {
        'title': 'Vehículos',
        'subtitle': 'agregar'
    }

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Vehículo creado satisfactoriamente')
        return reverse('public_app:vehiculos_list')

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.usuario_id = self.request.user.id

        self.object.save()
        return super(VehiculoCreateView, self).form_valid(form)


class VehiculoUpdateView(LoginRequiredMixin, UpdateView):

    model = Vehiculo
    fields = ['placa', 'cedula', 'tipo_vehiculo', 'cilindros']
    template_name = 'public_app/vehiculos/vehiculo_form_edit.html'
    pk_url_kwarg = 'placa'

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Vehículo actualizado satisfactoriamente')
        return reverse('public_app:vehiculos_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario_id = self.request.user.id
        self.object.save()
        return super(VehiculoUpdateView, self).form_valid(form)
