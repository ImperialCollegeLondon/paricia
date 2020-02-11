from django.shortcuts import render

from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from mensual.forms import FrecuenciaMensualForm
from mensual.functions import get_frecuencia_registro


# Create your views here.
class ConsultarFrecuencia(LoginRequiredMixin, FormView):
    template_name = 'mensual/frecuencia_mensual.html'
    form_class = FrecuenciaMensualForm
    success_url = '/mensual/frecuencia'

    def post(self, request, *args, **kwargs):
        form = FrecuenciaMensualForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            datos = get_frecuencia_registro(form)
            template = 'mensual/mensual_table.html'
            return render(request, template, {'datos': datos})
        return self.render_to_response(self.get_context_data(form=form, save=True))

    def get_context_data(self, **kwargs):
        context = super(ConsultarFrecuencia, self).get_context_data(**kwargs)
        return context

