# -*- coding: utf-8 -*-
from braces.views import GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    DetailView, ListView,
    UpdateView, CreateView, DeleteView
)
from pure_pagination.mixins import PaginationMixin

from dgas.gas_app.forms.usuario_form import GasUserForm, GasUserEditForm, GasUserPasswdForm
from dgas.users.models import GasUser


class GasUsersListView(GroupRequiredMixin, PaginationMixin, ListView):

    # required
    group_required = u"Admin"
    raise_exception = True

    model = GasUser
    template_name = 'gas_app/usuarios/usuarios_list.html'

    page = {
        'title': 'Usuarios',
        'subtitle': 'Listado general'
    }

    def get_context_data(self, **kwargs):
        context = super(GasUsersListView, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context


class GasUserCreateView(GroupRequiredMixin, CreateView):

    # required
    group_required = u"Admin"
    raise_exception = True

    model = GasUser
    form_class = GasUserForm
    success_url = 'gas_app:usuarios_list'
    template_name = 'gas_app/usuarios/usuario_form.html'

    page = {
        'title': 'Usuarios',
        'subtitle': 'formulario creación de cuenta'
    }

    def get_context_data(self, **kwargs):
        context = super(GasUserCreateView, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password1'])
        self.object.username = form.cleaned_data['username']
        self.object.email = form.cleaned_data['username']
        self.object.save()
        #self.object.groups.add(Group.objects.get(name='GasUsers'))
        self.object.save()

        messages.add_message(self.request,
                             messages.SUCCESS, 'Se ha creado la cuenta del usuario')

        super(GasUserCreateView, self).form_valid(form)

        return redirect(self.success_url)


class GasUserDetailView(GroupRequiredMixin, DetailView):

    # required
    group_required = u"Admin"
    raise_exception = True

    model = GasUser
    template_name = 'gas_app/usuarios/usuario_detail.html'

    page = {
        'title': 'Usuarios',
        'subtitle': 'Detalle de usuario'
    }

    def get_context_data(self, **kwargs):
        context = super(GasUserDetailView, self).get_context_data(**kwargs)
        context['page'] = self.page
        return context


class GasUserUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = u"Admin"
    raise_exception = True

    model = GasUser
    form_class = GasUserEditForm
    success_url = 'gas_app:usuarios_list'
    template_name = 'gas_app/usuarios/usuario_form.html'

    def get_context_data(self, **kwargs):
        context = super(GasUserUpdateView, self).get_context_data(**kwargs)
        context['page'] = {
            'name': 'user_update',
            'title': 'Actualización de operador',
            'form_action': '',
        }

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        #self.object.username = form.cleaned_data['username']
        #self.object.email = form.cleaned_data['username']
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'Se ha actualizado')

        super(GasUserUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class GasUserUpdatePasswdView(GroupRequiredMixin, UpdateView):

    # required
    group_required = u"Empresa"
    raise_exception = True

    model = GasUser
    form_class = GasUserPasswdForm
    success_url = 'gas_app:usuarios_list'
    template_name = 'gas_app/usuarios/usuario_form.html'

    def get_context_data(self, **kwargs):
        context = super(GasUserUpdatePasswdView, self).get_context_data(**kwargs)
        context['page'] = {
            'title': 'Usuarios',
            'subtitle': 'Cambio de password',
        }

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password1'])
        self.object.save()

        messages.add_message(self.request,
                             messages.SUCCESS, 'Se ha actualizado el password')

        super(GasUserUpdatePasswdView, self).form_valid(form)

        return redirect(self.success_url)


class GasUserDelete(GroupRequiredMixin, DeleteView):

    # required
    group_required = u"Admin"
    raise_exception = True

    model = GasUser

    template_name = 'gas_app/usuarios/usuario_confirm_delete.html'
    success_message = "El operador ha sido eliminado satisfactoriamente"

    page = {
        'title': 'GasUsers',
        'subtitle': 'Eliminación de usuario'
    }

    # send the user back to their own page after a successful update
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'El usuario ha sido eliminado satisfactoriamente')
        return reverse('gas_app:usuarios_list')

    def get_context_data(self, **kwargs):
        context = super(GasUserDelete, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context

