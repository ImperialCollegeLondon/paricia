from django.urls import path
from .views import *

app_name = 'indices'
urlpatterns = [
    path('indices/doblemasa/', Doblemasa.as_view(),name='doblemasa'),
]
