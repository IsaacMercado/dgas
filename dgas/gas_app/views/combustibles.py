# -*- coding: utf-8 -*-
import json
from braces.views import GroupRequiredMixin
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

from dgas.gas_app.models import Combustible, Estacion


class CombustiblesListView(GroupRequiredMixin, ListView):
    # required
    group_required = u"Estacion"
    raise_exception = True
    paginate_by = 50

    model = Combustible
    context_object_name = 'estaciones'
    template_name = 'gas_app/combustibles/combustibles_list.html'

    page = {
        'title': 'Combustibles',
        'subtitle': 'Listado general'
    }

    def get_queryset(self):
        est = Estacion.objects.filter(usuario_id=self.request.user.id)
        return Combustible.objects.filter(estacion__in=est)

    def get_context_data(self, **kwargs):
        context = super(CombustiblesListView, self).get_context_data(**kwargs)
        context['page'] = self.page
        #context['estacion'] = Estacion.objects.get(pk=self.request.user.id)

        return context


class CombustibleDetailView(GroupRequiredMixin, DetailView):
    # required
    group_required = u"Estacion"
    raise_exception = True

    model = Combustible
    template_name = 'gas_app/combustibles/combustible_detail.html'

    page = {
        'title': 'Combustibles',
        'subtitle': 'Detalle de datos de la estación'
    }

    def get_context_data(self, **kwargs):
        context = super(EstacionDetailView, self).get_context_data(**kwargs)
        context['page'] = self.page
        return context


class CombustibleCreateView(GroupRequiredMixin, CreateView):
    # required
    group_required = u"Estacion"
    raise_exception = True

    model = Combustible
    template_name = 'gas_app/combustibles/combustible_form.html'

    fields = ['estacion', 'tipo_combustible', 'nro_factura', 'cantidad', 'fecha_carga']

    page = {
        'title': 'Combustibles',
        'subtitle': 'Agregar'
    }

    def get_context_data(self, **kwargs):
        context = super(CombustibleCreateView, self).get_context_data(**kwargs)
        context['page'] = self.page
        context['form'].fields['estacion'].queryset = Estacion.objects.filter(
            usuario_id=self.request.user.id)  # Versión intranet
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Registro de combustible ha sido creado satisfactoriamente')
        return reverse('gas_app:combustibles_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.usuario_id = self.request.user.id
        self.object.save()
        return super(CombustibleCreateView, self).form_valid(form)


class CombustibleUpdateView(GroupRequiredMixin, UpdateView):
    # required
    group_required = u"Estacion"
    raise_exception = True

    model = Combustible
    fields = ['tipo_combustible', 'nro_factura','cantidad', 'fecha_carga']
    success_url = 'gas_app:combustibles_list'
    template_name = 'gas_app/combustibles/combustible_form.html'

    def get_context_data(self, **kwargs):
        context = super(CombustibleUpdateView, self).get_context_data(**kwargs)
        context['page'] = {
            'name': 'user_update',
            'title': 'Actualización de estacion de servicio ',
            'form_action': '',
        }

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.username = form.cleaned_data['username']
        # self.object.email = form.cleaned_data['username']
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'Registro de combustible actualizado')

        super(CombustibleUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class CombustibleDelete(GroupRequiredMixin, DeleteView):
    # required
    group_required = u"Estacion"
    raise_exception = True

    model = Combustible

    template_name = 'gas_app/combustibles/combustible_confirm_delete.html'
    success_message = "La sección ha sido eliminado satisfactoriamente"

    page = {
        'title': 'Combustible',
        'subtitle': 'Eliminación de carga de combustible'
    }

    # send the user back to their own page after a successful update
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Registro de combustible ha sido eliminad satisfactoriamente')
        return reverse('gas_app:combustibles_list')

    def get_context_data(self, **kwargs):
        context = super(CombustibleDelete, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context
