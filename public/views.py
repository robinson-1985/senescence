from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from profiles.models import ProfessionalProfile
from .forms import LeadForm


def professionals_list(request):
    """Lista pública de profissionais com filtros e busca."""
    
    city = request.GET.get("city", "").strip()
    caregiver = request.GET.get("caregiver", "")
    search = request.GET.get("search", "").strip()
    
    qs = ProfessionalProfile.objects.filter(
        published=True,
        available=True
    ).select_related("user")
    
    if city:
        qs = qs.filter(city__icontains=city)
    
    if caregiver == "1":
        qs = qs.filter(is_caregiver=True)
    elif caregiver == "0":
        qs = qs.filter(is_caregiver=False)
    
    if search:
        qs = qs.filter(
            Q(display_name__icontains=search) |
            Q(services__icontains=search) |
            Q(bio__icontains=search)
        )
    
    qs = qs.order_by("-updated_at")
    
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    available_cities = ProfessionalProfile.objects.filter(
        published=True,
        available=True
    ).values_list("city", flat=True).distinct().order_by("city")
    
    context = {
        "page_obj": page_obj,
        "profiles": page_obj.object_list,
        "city": city,
        "caregiver": caregiver,
        "search": search,
        "available_cities": available_cities,
        "total_count": qs.count()
    }
    
    return render(request, "public/professionals_list.html", context)


def professional_detail(request, slug):
    """Página de detalhes de um profissional específico."""
    
    profile = get_object_or_404(
        ProfessionalProfile.objects.select_related("user"),
        slug=slug,
        published=True
    )
    
    form = LeadForm()
    
    context = {
        "profile": profile,
        "form": form
    }
    
    return render(request, "public/professional_detail.html", context)


def contact_professional(request, slug):
    """Processa o formulário de contato com o profissional."""
    
    profile = get_object_or_404(
        ProfessionalProfile,
        slug=slug,
        published=True
    )
    
    if request.method != "POST":
        messages.warning(request, _("Método não permitido."))
        return redirect("public_professional_detail", slug=slug)
    
    form = LeadForm(request.POST)
    
    if form.is_valid():
        lead = form.save(commit=False)
        lead.profile = profile
        lead.save()
        
        messages.success(
            request,
            _("Mensagem enviada com sucesso! O profissional entrará em contato em breve.")
        )
        
        return redirect("public_thanks", slug=slug)
    
    messages.error(
        request,
        _("Por favor, corrija os erros no formulário.")
    )
    
    context = {
        "profile": profile,
        "form": form
    }
    
    return render(request, "public/professional_detail.html", context)


def thanks(request, slug):
    """Página de agradecimento após envio do formulário."""
    
    profile = get_object_or_404(
        ProfessionalProfile,
        slug=slug,
        published=True
    )
    
    context = {"profile": profile}
    
    return render(request, "public/thanks.html", context)
