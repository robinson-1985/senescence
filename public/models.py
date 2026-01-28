from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from profiles.models import ProfessionalProfile


class Lead(models.Model):
    """Modelo para armazenar leads/contatos de pessoas interessadas nos serviços."""
    
    profile = models.ForeignKey(
        ProfessionalProfile,
        on_delete=models.CASCADE,
        related_name="leads",
        verbose_name=_("Perfil profissional")
    )
    
    name = models.CharField(
        _("Nome"),
        max_length=120,
        help_text=_("Nome completo do interessado")
    )
    
    phone_validator = RegexValidator(
        regex=r'^\d{10,11}$',
        message=_("Telefone deve conter 10 ou 11 dígitos")
    )
    
    phone = models.CharField(
        _("Telefone"),
        max_length=30,
        blank=True,
        validators=[phone_validator],
        help_text=_("Telefone com DDD (opcional)")
    )
    
    message = models.TextField(
        _("Mensagem"),
        help_text=_("Descrição da necessidade ou interesse")
    )
    
    created_at = models.DateTimeField(
        _("Criado em"),
        auto_now_add=True
    )
    
    contacted = models.BooleanField(
        _("Contatado?"),
        default=False,
        help_text=_("Marque quando entrar em contato com este lead")
    )
    
    notes = models.TextField(
        _("Observações internas"),
        blank=True,
        help_text=_("Anotações sobre contato e acompanhamento")
    )
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Lead")
        verbose_name_plural = _("Leads")
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["profile", "-created_at"]),
            models.Index(fields=["contacted"]),
        ]
    
    def __str__(self):
        return f"Lead para {self.profile.display_name} - {self.name}"
    
    def get_phone_formatted(self):
        """Retorna o telefone formatado para exibição."""
        if not self.phone:
            return ""
        
        digits = "".join(filter(str.isdigit, self.phone))
        
        if len(digits) == 11:
            return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
        elif len(digits) == 10:
            return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        
        return self.phone
