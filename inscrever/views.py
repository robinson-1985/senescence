from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cuidador
from .forms import CuidadorForm


class ListaCuidadorView(ListView):
    model = Cuidador
    template_name = 'inscrever/lista.html'
    context_object_name = 'cuidadores'
    paginate_by = 10  # Mostra 10 cuidadores por página


class NovoCuidadorView(LoginRequiredMixin, CreateView):
    model = Cuidador
    form_class = CuidadorForm
    template_name = 'inscrever/novo.html'
    success_url = reverse_lazy('lista_cuidadores')
    login_url = reverse_lazy('login')  # Redireciona para login se não estiver autenticado

    def form_valid(self, form):
        messages.success(self.request, 'Cadastro realizado com sucesso!')
        return super().form_valid(form)


class CuidadorDetailView(DetailView):
    model = Cuidador
    template_name = 'inscrever/detalhe.html'
    context_object_name = 'cuidador'
