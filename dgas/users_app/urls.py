from django.urls import path

from dgas.users_app.views import colas

app_name = "users_app"

urlpatterns = [

    # Cargas
    path('cargas/', colas.ColasListView.as_view(), name='colas_list'),

]
