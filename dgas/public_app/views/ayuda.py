# -*- coding: utf-8 -*-
import datetime
from braces.views import LoginRequiredMixin
from django.views.generic import RedirectView, TemplateView


class PreguntasFrecuentes(TemplateView):
    template_name = "public_app/ayuda/preguntas_frecuentes.html"


class Implementacion(TemplateView):
    template_name = "public_app/ayuda/fases_de_implementacion.html"
