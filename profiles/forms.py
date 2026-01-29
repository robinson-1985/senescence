from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import ProfessionalProfile


class ProfessionalProfileForm(forms.ModelForm):
    class Meta:
        model = ProfessionalProfile
        fields = [
            "display_name",
            "city",
            "region",
            "is_caregiver",
            "bio",
            "phone_whatsapp",
            "services",
            "available",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 5}),
            "phone_whatsapp": forms.TextInput(attrs={"placeholder": "Ex: 16999998888 (sem +55)"}),
        }
        
        widgets = {
            "display_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Maria Silva",
                "maxlength": "120"
            }),
            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Araraquara",
                "maxlength": "80"
            }),
            "region": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Araraquara e região",
                "maxlength": "120"
            }),
            "is_caregiver": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Conte um pouco sobre sua experiência, formação e qualificações..."
            }),
            "phone_whatsapp": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "16999998888",
                "maxlength": "20",
                "pattern": "[0-9]+",
                "title": "Apenas números com DDD"
            }),
            "services": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: banho, companhia, medicação, curativos",
                "maxlength": "255"
            }),
            "available": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
        
        labels = {
            "display_name": _("Nome de exibição"),
            "city": _("Cidade"),
            "region": _("Região de atendimento"),
            "is_caregiver": _("Sou cuidador(a)"),
            "bio": _("Sobre mim"),
            "phone_whatsapp": _("WhatsApp (com DDD)"),
            "services": _("Serviços oferecidos"),
            "available": _("Estou disponível para novos clientes"),
        }
        
        help_texts = {
            "phone_whatsapp": _("Apenas números com DDD. Ex: 16999998888"),
            "services": _("Liste os principais serviços que você oferece"),
            "bio": _("Descreva sua experiência profissional e qualificações"),
            "available": _("Desmarque se não estiver aceitando novos clientes no momento"),
        }
    
    def clean_phone_whatsapp(self):
        phone = self.cleaned_data.get("phone_whatsapp", "")
        
        digits = "".join(filter(str.isdigit, phone))
        
        if len(digits) not in [10, 11]:
            raise ValidationError(
                _("Telefone deve conter 10 ou 11 dígitos (DDD + número). Ex: 16999998888")
            )
        
        ddd = int(digits[:2])
        if ddd < 11 or ddd > 99:
            raise ValidationError(
                _("DDD inválido. Use um DDD válido do Brasil.")
            )
        
        return digits
    
    def clean_display_name(self):
        """
        Valida o nome de exibição.
        """
        name = self.cleaned_data.get("display_name", "").strip()
        
        if len(name) < 3:
            raise ValidationError(
                _("O nome deve ter pelo menos 3 caracteres.")
            )
        
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        
        is_caregiver = cleaned_data.get("is_caregiver")
        services = cleaned_data.get("services", "").strip()
        
        if is_caregiver and not services:
            self.add_error(
                "services",
                _("Por favor, descreva os serviços que você oferece como cuidador(a).")
            )
        
        return cleaned_data
