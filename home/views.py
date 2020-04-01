from django.views import  View
from django.views.generic.base import TemplateView
from django.views.generic import FormView
from home.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class AjaxableResponseMixin:

    def form_invalid(self, form):
        response = super().form_invalid(form)
        form_field_errors = []
        form_non_field_errors = []
        if self.request.is_ajax():
            for field in form:
                if field.errors:
                    for error in field.errors:
                        fila = {
                            'label_tag': field.label,
                            'error': error
                        }
                        form_field_errors.append(fila)

            for error in form.non_field_errors():
                fila = {
                    'error': error
                }
                form_non_field_errors.append(fila)
            data_error = {
                'form_field_errors': form_field_errors,
                'form_non_field_errors': form_non_field_errors
            }
            # return JsonResponse(form.errors, status=400)
            return JsonResponse(data_error, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                #'pk': self.object.pk,
                'mensaje': 'Registro Guardado'
            }
            return JsonResponse(data)
        else:
            return response


class MessageSucces(View):
    @staticmethod
    def get(request):
        mensaje = "Registro Guardado"
        data ={
            'mensaje':mensaje
        }
        return JsonResponse(data, safe=False)


class MessageDelete(View):
    @staticmethod
    def get(request):
        mensaje = "Registro Eliminado"
        data ={
            'mensaje': mensaje
        }
        return JsonResponse(data, safe=False)


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