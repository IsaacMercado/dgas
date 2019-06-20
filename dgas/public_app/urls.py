from django.urls import path

from dgas.public_app import views

app_name = "public_app"

urlpatterns = [

    path('estaciones/', views.Estaciones.as_view(), name='estaciones'),
    path('colas/', views.Colas.as_view(), name='colas'),

]
