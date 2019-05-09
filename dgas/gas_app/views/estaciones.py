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

from dgas.gas_app.models import Estacion


class EstacionesListView(GroupRequiredMixin, ListView):
    # required
    group_required = u"Administrador"
    raise_exception = True
    paginate_by = 50

    model = Estacion
    context_object_name = 'estaciones'
    template_name = 'gas_app/estaciones/estaciones_list.html'

    page = {
        'title': 'Estaciones',
        'subtitle': 'Listado general'
    }

    #def get_queryset(self):
    #    return Estacion.objects.filter(usuario_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(EstacionesListView, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context


class EstacionesEstListView(GroupRequiredMixin, ListView):
    # required
    group_required = u"Estacion"
    raise_exception = True
    paginate_by = 50

    model = Estacion
    context_object_name = 'estaciones'
    template_name = 'gas_app/estaciones/estaciones_est_list.html'

    page = {
        'title': 'Estaciones',
        'subtitle': 'Listado general'
    }

    def get_queryset(self):
        return Estacion.objects.filter(usuario_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(EstacionesEstListView, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context


class EstacionDetailView(GroupRequiredMixin, DetailView):
    # required
    group_required = u"Administrador"
    raise_exception = True

    model = Estacion
    template_name = 'gas_app/estaciones/estacion_detail.html'

    page = {
        'title': 'Estaciones',
        'subtitle': 'Detalle de datos de la estación'
    }

    def get_context_data(self, **kwargs):
        context = super(EstacionDetailView, self).get_context_data(**kwargs)
        context['page'] = self.page
        return context


class EstacionCreateView(GroupRequiredMixin, CreateView):
    # required
    group_required = u"Administrador"
    raise_exception = True

    model = Estacion
    template_name = 'gas_app/estaciones/estacion_form.html'

    fields = ['usuario', 'nombre', 'capacidad_91', 'reserva_91','capacidad_95', 'reserva_95', 'capacidad_gasoil',
              'reserva_gasoil', 'operativa', 'latitude', 'longitude']

    page = {
        'title': 'Estaciones',
        'subtitle': 'Agregar'
    }

    def get_context_data(self, **kwargs):
        context = super(EstacionCreateView, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'La sección ha sido creada satisfactoriamente')
        return reverse('gas_app:estaciones_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.empresa_id = self.request.user.id
        self.object.save()
        return super(EstacionCreateView, self).form_valid(form)


class EstacionUpdateView(GroupRequiredMixin, UpdateView):
    # required
    group_required = u"Administrador"
    raise_exception = True

    model = Estacion
    fields = ['usuario', 'nombre', 'capacidad_91', 'reserva_91', 'capacidad_95', 'reserva_95', 'capacidad_gasoil',
              'reserva_gasoil', 'operativa', 'latitude', 'longitude']
    success_url = 'gas_app:estaciones_list'
    template_name = 'gas_app/estaciones/estacion_form.html'

    def get_context_data(self, **kwargs):
        context = super(EstacionUpdateView, self).get_context_data(**kwargs)
        context['page'] = {
            'name': 'user_update',
            'title': 'Actualización de estacion de servicio ',
            'form_action': '',
        }

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'Se ha actualizado la seccion')

        super(EstacionUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class EstacionEstUpdateView(GroupRequiredMixin, UpdateView):
    # required
    group_required = u"Estacion"
    raise_exception = True

    model = Estacion
    fields = ['operativa']
    success_url = 'gas_app:estaciones_list'
    template_name = 'gas_app/estaciones/estacion_est_form.html'

    def get_context_data(self, **kwargs):
        context = super(EstacionEstUpdateView, self).get_context_data(**kwargs)
        context['page'] = {
            'name': 'user_update',
            'title': 'Actualización de estacion de servicio ',
            'form_action': '',
        }

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'Se ha actualizado la seccion')

        super(EstacionUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class EstacionEstadoUpdateView(GroupRequiredMixin, UpdateView):
    # required
    group_required = u"Administrador"
    raise_exception = True

    model = Estacion
    fields = ['opetativa']
    success_url = 'gas_app:combustibles_list'
    template_name = 'gas_app/estaciones/estacion_est_form.html'

    def get_context_data(self, **kwargs):
        context = super(EstacionEstadoUpdateView, self).get_context_data(**kwargs)
        context['page'] = {
            'name': 'user_update',
            'title': 'Actualización del estado de la estacion de servicio ',
            'form_action': '',
        }

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'Se ha actualizado el estado')

        super(EstacionEstadoUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class EstacionDelete(GroupRequiredMixin, DeleteView):
    # required
    group_required = u"Administrador"
    raise_exception = True

    model = Estacion

    template_name = 'gas_app/estaciones/estacion_confirm_delete.html'
    success_message = "La sección ha sido eliminado satisfactoriamente"

    page = {
        'title': 'Estacions',
        'subtitle': 'Eliminación de sección'
    }

    # send the user back to their own page after a successful update
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'La seccion ha sido eliminada satisfactoriamente')
        return reverse('gas_app:estaciones_list')

    def get_context_data(self, **kwargs):
        context = super(EstacionDelete, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context
