from django.urls import re_path
from django.urls import reverse_lazy
from home.views import HomePageView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
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
    # re_path(r'^$', LoginView.as_view(), name='login'),
    re_path(r'^login/$', LoginView.as_view(template_name='home/login.html'), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout')
]
