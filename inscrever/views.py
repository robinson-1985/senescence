from django.shortcuts import render, redirect
from .models import Cuidador
from .forms import CuidadorForm


def lista_cuidadores(request):
    cuidadores = Cuidador.objects.all()
    return render(request, 'inscrever/lista_cuidadores.html', {'cuidadores': cuidadores})


def novo_cuidador(request):
    if request.method == 'POST':
        form = CuidadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cuidadores')
    else:
        form = CuidadorForm()
    return render(request, 'inscrever/novo_cuidador.html', {'form': form})
