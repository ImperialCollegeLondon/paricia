from django.urls import re_path, path
from django.urls import reverse_lazy
from home.views import HomePageView
from reportes import views
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = 'home'
urlpatterns = [
    re_path(r'^$', HomePageView.as_view(), name='home'),
    #re_path(r'^$', views.ConsultasPeriodo.as_view(), name='home'),
    # re_path(r'^$', LoginView.as_view(), name='login'),
    re_path(r'^login/$', LoginView.as_view(template_name='home/login.html'), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    #re_path(r'^$', TemplateView.as_view(template_name="home/consultas_usuario.html")),
]
