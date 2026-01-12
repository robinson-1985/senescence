from django.views.generic import ListView, DetailView, CreateView
from .models import Cuidador
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class CuidadorListView(ListView):
    model = Cuidador
    template_name = 'inscrever/cuidador_list.html'
    ordering = ['nome']

class CuidadorDetailView(DetailView):
    model = Cuidador
    template_name = 'inscrever/detalhe.html'

class NovoCuidadorView(LoginRequiredMixin, CreateView):
    model = Cuidador
    fields = '__all__'
    template_name = 'inscrever/novo_cuidador.html'
    success_url = reverse_lazy('cuidador_list')
