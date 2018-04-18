from django.views.generic.base import TemplateView
from django.views.generic import FormView
from home.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context


'''class LoginView(FormView):
    form_class=LoginForm
    template_name='home/login.html'
    def post(self, request, *args, **kwargs):
        form=LoginForm(self.request.POST or None)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                print "entro"
                login(self.request,user)
                return redirect('home:home')
            else:
                print "no llego"
            return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        return context
def logout_view(request):
    logout(request)'''
