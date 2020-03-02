from django.shortcuts import render

from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from horario.forms import PorcentajeHorarioForm
from horario.functions import get_porcentaje_registro


# Create your views here.
class ConsultarPorcentaje(LoginRequiredMixin, FormView):
    template_name = 'horario/porcentaje_horario.html'
    form_class = PorcentajeHorarioForm
    success_url = '/horario/porcentaje'

    def post(self, request, *args, **kwargs):
        form = PorcentajeHorarioForm(self.request.POST or None)
        if form.is_valid() and self.request.is_ajax():
            datos = get_porcentaje_registro(form)
            template = 'horario/horario_table.html'
            return render(request, template, {'datos': datos})
        return self.render_to_response(self.get_context_data(form=form, save=True))

    def get_context_data(self, **kwargs):
        context = super(ConsultarPorcentaje, self).get_context_data(**kwargs)
        return context

