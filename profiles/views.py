from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from .forms import ProfessionalProfileForm
from .models import ProfessionalProfile


@login_required
def my_profile(request):
    profile, created = ProfessionalProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "display_name": request.user.get_full_name() or request.user.username,
            "phone_whatsapp": "",
        }
    )
    
    if request.method == "POST":
        form = ProfessionalProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.published = False
            obj.save()
            
            messages.success(
                request,
                _("Perfil atualizado com sucesso! Aguarde aprovação da equipe.")
            )
            
            return redirect("profiles:my_profile")
        else:
            messages.error(
                request,
                _("Por favor, corrija os erros abaixo.")
            )
    else:
        form = ProfessionalProfileForm(instance=profile)
    
    context = {
        "form": form,
        "profile": profile,
        "is_new_profile": created
    }
    
    return render(request, "profiles/my_profile.html", context)
