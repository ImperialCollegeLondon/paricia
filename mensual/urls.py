from django.urls import path
from mensual import views

app_name = 'mensual'
urlpatterns = [
    path('mensual/frecuencia', views.ConsultarFrecuencia.as_view(), name='frecuencia'),

]