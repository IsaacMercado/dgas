import json
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.views.generic import View
from django.shortcuts import redirect

from .models import Parroquia

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserListView(LoginRequiredMixin, ListView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["last_name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class ParroquiasView(View):

    def get(self, context, **response_kwargs):
        municipio_id = self.kwargs['pk']
        parroquias_list = Parroquia.objects.filter(municipio=municipio_id).values('id', 'parroquia',).order_by('-parroquia')
        response = [r for r in parroquias_list]

        return HttpResponse(json.dumps(response))


class UserPerfilDetailView(LoginRequiredMixin, DetailView):

    model = User
    template_name = 'users/perfiles/perfil_detail.html'

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


class UserPerfilUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ['first_name', 'last_name', 'cedula', 'telefono_celular', 'direccion_base', 'municipio', 'parroquia']
    template_name = 'users/perfiles/perfil_form.html'
    success_url = reverse_lazy('users:user_perfil_detail')

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'Se ha actualizado el perfil')

        super(UserPerfilUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class UserPhotolUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ['photo_user']
    template_name = 'users/perfiles/perfil_form.html'
    success_url = reverse_lazy('users:user_perfil_detail')

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'Se ha actualizado la foto')

        super(UserPhotolUpdateView, self).form_valid(form)

        return redirect(self.success_url)
