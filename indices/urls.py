from django.urls import path
from .views import *

app_name = 'indices'
urlpatterns = [
    path('indices/doblemasa/', Doblemasa.as_view(),name='doblemasa'),
    path('indices/precipitacion/', IndPrecip.as_view(),name='precipitacion'),
    path('indices/caudal/', IndCaudal.as_view(),name='caudal'),
    path('indices/intensidad/', IntensidadRR.as_view(),name='intensidad'),
    path('indices/duracaudal/', DuracionCaudal.as_view(),name='duracaudal'),
    path('indices/rangos/', PeriodoDatos.as_view(),name='rangos'),

]
