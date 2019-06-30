from django.urls import path

from dgas.users.views import (
    user_list_view,
    user_redirect_view,
    user_update_view,
    user_detail_view,
    ParroquiasView,
    UserPerfilDetailView,
    UserPerfilUpdateView,
    UserPhotolUpdateView
)

app_name = "users"

urlpatterns = [
    path("", view=user_list_view, name="list"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    path('perfil', UserPerfilDetailView.as_view(), name='user_perfil_detail'),
    path('perfil/actualizar', UserPerfilUpdateView.as_view(), name='user_perfil_update'),
    path('perfil/actualizar/foto', UserPhotolUpdateView.as_view(), name='user_photo_update'),

    path('parroquias/<int:pk>', ParroquiasView.as_view(), name='user_parroquia'),
]
