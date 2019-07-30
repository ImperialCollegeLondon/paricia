#from estacion.models import Estacion,Inamhi
from django.views import generic
from indices.forms import SearchForm

# Create your views here.

class Doblemasa(generic.FormView):
    template_name = "indices/doblemasa.html"
    form_class = SearchForm

    success_url = "/"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super(Doblemasa,self).form_valid(form)