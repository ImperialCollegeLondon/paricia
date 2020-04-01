from django.urls import re_path, path
from validacion import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'validacion'
urlpatterns = [
    re_path(r'^validacion/periodos_validacion/$', views.PeriodosValidacion.as_view(), name='periodos_validacion'),
    re_path(r'^validacion/borrar/$', views.ValidacionBorrar.as_view(), name='borrar'),
    path('validacion/lista/<int:estacion>/<int:variable>/<str:fecha>', views.ListaValidacion.as_view(), name='horario'),
    path('validacion/diaria/', views.ValidacionDiaria.as_view(), name='diaria'),

    ### url para los datos desde la api
    path('inst/', views.VarList.as_view()),

]
