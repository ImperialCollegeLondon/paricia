from django.views.generic.base import TemplateView
from django.views.generic import FormView
from home.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(TemplateView):
    template_name = "home/consultas_usuario.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['base_template'] = "index.html"
        else:
            context['base_template'] = "index_invitado.html"
        return context


class ConsultasView(TemplateView):
    template_name = "consultas_usuario.html"