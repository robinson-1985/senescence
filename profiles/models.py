from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from urllib.parse import quote


class ProfessionalProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="professional_profile",
        verbose_name=_("Usuário")
    )
    display_name = models.CharField(
        _("Nome de exibição"),
        max_length=120
    )
    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        db_index=True
    )
    city = models.CharField(
        _("Cidade"),
        max_length=80,
        default="Araraquara"
    )
    region = models.CharField(
        _("Região de atendimento"),
        max_length=120,
        default="Araraquara e região",
        blank=True
    )
    is_caregiver = models.BooleanField(
        _("É cuidador(a)?"),
        default=True
    )
    bio = models.TextField(
        _("Biografia"),
        blank=True,
        help_text=_("Descreva sua experiência e qualificações")
    )
    services = models.CharField(
        _("Serviços oferecidos"),
        max_length=255,
        blank=True,
        help_text=_("Ex: banho, companhia, medicação, curativos")
    )
    phone_validator = RegexValidator(
        regex=r'^\d{10,11}$',
        message=_("Telefone deve conter 10 ou 11 dígitos (DDD + número)")
    )
    phone_whatsapp = models.CharField(
        _("WhatsApp"),
        max_length=20,
        validators=[phone_validator],
        help_text=_("Somente números com DDD (ex: 16999998888)")
    )
    available = models.BooleanField(
        _("Disponível"),
        default=True,
        help_text=_("Está aceitando novos clientes?")
    )
    published = models.BooleanField(
        _("Publicado"),
        default=False,
        help_text=_("Marque para aparecer publicamente")
    )
    created_at = models.DateTimeField(
        _("Criado em"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Atualizado em"),
        auto_now=True
    )
    
    class Meta:
        ordering = ["-updated_at"]
        verbose_name = _("Perfil Profissional")
        verbose_name_plural = _("Perfis Profissionais")
        indexes = [
            models.Index(fields=["-updated_at"]),
            models.Index(fields=["published", "available"]),
        ]
    
    def __str__(self):
        return f"{self.display_name} ({self.city})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)
    
    def _generate_unique_slug(self):
        base_slug = slugify(self.display_name)[:120] or "profissional"
        slug = base_slug
        counter = 2
        
        while ProfessionalProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        return slug
    
    @property
    def whatsapp_link(self):
       
        digits = "".join(filter(str.isdigit, self.phone_whatsapp))
        
        # Adiciona código do Brasil se necessário
        if not digits.startswith("55"):
            digits = f"55{digits}"
        
        message = "Olá, vi seu perfil no Senescence. Podemos conversar?"
        encoded_message = quote(message)
        
        return f"https://wa.me/{digits}?text={encoded_message}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("professional_profile_detail", kwargs={"slug": self.slug})
