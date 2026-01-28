from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Lead


class LeadForm(forms.ModelForm):
    """Formulário para visitantes entrarem em contato com profissionais."""
    
    class Meta:
        model = Lead
        fields = ["name", "phone", "message"]
        
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Seu nome completo",
                "maxlength": "120",
                "required": True
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "16999998888",
                "maxlength": "30",
                "pattern": "[0-9]+",
                "title": "Digite apenas números com DDD"
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Descreva o que você precisa (tipo de cuidado, horários, localização, etc.)",
                "required": True
            })
        }
        
        labels = {
            "name": _("Seu nome"),
            "phone": _("Telefone (WhatsApp)"),
            "message": _("Como podemos ajudar?")
        }
        
        help_texts = {
            "phone": _("Opcional. Informe seu WhatsApp para contato mais rápido."),
            "message": _("Descreva suas necessidades e disponibilidade.")
        }
        
        error_messages = {
            "name": {
                "required": _("Por favor, informe seu nome."),
            },
            "message": {
                "required": _("Por favor, descreva o que você precisa."),
            }
        }
    
    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        
        if len(name) < 3:
            raise ValidationError(
                _("Por favor, informe um nome válido (mínimo 3 caracteres).")
            )
        
        if " " not in name:
            raise ValidationError(
                _("Por favor, informe seu nome completo.")
            )
        
        return name
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        
        if not phone:
            return ""
        
        digits = "".join(filter(str.isdigit, phone))
        
        if len(digits) not in [10, 11]:
            raise ValidationError(
                _("Telefone deve ter 10 ou 11 dígitos (DDD + número). Ex: 16999998888")
            )
        
        ddd = int(digits[:2])
        if ddd < 11 or ddd > 99:
            raise ValidationError(
                _("DDD inválido. Digite um DDD válido do Brasil.")
            )
        
        return digits
    
    def clean_message(self):
        message = self.cleaned_data.get("message", "").strip()
        
        if len(message) < 10:
            raise ValidationError(
                _("Por favor, descreva melhor o que você precisa (mínimo 10 caracteres).")
            )
        
        return message
