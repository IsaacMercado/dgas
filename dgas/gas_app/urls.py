from django.urls import path

from dgas.gas_app.views import recolector, coordinadores
from dgas.gas_app.views import usuarios, estaciones, combustibles

app_name = "gas_app"

urlpatterns = [

    # Coordinadores
    path('coordinadores/', coordinadores.Colas.as_view(), name='coodinadores_list'),
    path('coordinadores_isla/', coordinadores.ColasIslas.as_view(), name='coodinadores_list'),

    path('recolector/', recolector.CargaDashBoardListView.as_view(), name='recolector_dash'),
    path('recolector/cargar/<int:estacion_id>', recolector.CargaTemplateView.as_view(), name='carga'),

    # Usuarios
    path('usuarios/', usuarios.GasUsersListView.as_view(), name='usuarios_list'),
    path('usuarios/create', usuarios.GasUserCreateView.as_view(), name='usuario_create'),
    path('usuarios/edit/<int:pk>', usuarios.GasUserUpdateView.as_view(), name='usuario_edit'),
    path('usuarios/detail/<int:pk>', usuarios.GasUserDetailView.as_view(), name='usuario_detail'),
    path('usuarios/delete/<int:pk>', usuarios.GasUserDelete.as_view(), name='usuario_delete'),
    path('usuarios/change_passwd/<int:pk>', usuarios.GasUserUpdatePasswdView.as_view(), name='usuario_change_passwd'),

    # Usuarios
    path('estaciones/', estaciones.EstacionesListView.as_view(), name='estaciones_list'),
    path('estaciones/create', estaciones.EstacionCreateView.as_view(), name='estacion_create'),
    path('estaciones/edit/<int:pk>', estaciones.EstacionUpdateView.as_view(), name='estacion_edit'),
    path('estaciones/detail/<int:pk>', estaciones.EstacionDetailView.as_view(), name='estacion_detail'),
    path('estaciones/delete/<int:pk>', estaciones.EstacionDelete.as_view(), name='estacion_delete'),

    path('estaciones/edit_est/<int:pk>', estaciones.EstacionEstUpdateView.as_view(), name='estacion_est_edit'),
    path('estaciones/list_est', estaciones.EstacionesEstListView.as_view(), name='estaciones_est_list'),

    # Usuarios
    path('estacion/combustibles/', combustibles.CombustiblesListView.as_view(), name='combustibles_list'),
    path('estacion/combustibles/create', combustibles.CombustibleCreateView.as_view(), name='combustible_create'),
    path('estacion/combustibles/edit/<int:pk>', combustibles.CombustibleUpdateView.as_view(), name='combustible_edit'),
    path('estacion/combustibles/detail/<int:pk>', combustibles.CombustibleDetailView.as_view(), name='combustible_detail'),
    path('estacion/combustibles/delete/<int:pk>', combustibles.CombustibleDelete.as_view(), name='combustible_delete'),

]
