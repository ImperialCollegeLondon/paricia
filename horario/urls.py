from django.urls import path
from horario import views

app_name = 'horario'
urlpatterns = [
    path('horario/porcentaje', views.ConsultarPorcentaje.as_view(), name='porcentaje'),

]