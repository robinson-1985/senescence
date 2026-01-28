from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import ProfessionalProfile


@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "city",
        "is_caregiver",
        "status_badges",
        "whatsapp_display",
        "updated_at"
    )
    
    list_filter = (
        "published",
        "available",
        "is_caregiver",
        "city",
        "created_at",
        "updated_at"
    )
    
    search_fields = (
        "display_name",
        "user__username",
        "user__email",
        "city",
        "services",
        "bio"
    )
    
    prepopulated_fields = {"slug": ("display_name",)}
    
    readonly_fields = (
        "created_at",
        "updated_at",
        "slug",
        "whatsapp_preview"
    )
    
    fieldsets = (
        (_("Informações Básicas"), {
            "fields": ("user", "display_name", "slug", "bio")
        }),
        (_("Localização"), {
            "fields": ("city", "region")
        }),
        (_("Serviços"), {
            "fields": ("is_caregiver", "services")
        }),
        (_("Contato"), {
            "fields": ("phone_whatsapp", "whatsapp_preview")
        }),
        (_("Status"), {
            "fields": ("available", "published")
        }),
        (_("Datas"), {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    actions = ["publish_profiles", "unpublish_profiles", "mark_available", "mark_unavailable"]
    
    list_per_page = 25
    date_hierarchy = "created_at"
    
    @admin.display(description=_("Status"), ordering="published")
    def status_badges(self, obj):
        badges = []
        
        if obj.published:
            badges.append('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">✓ Publicado</span>')
        else:
            badges.append('<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">✗ Não publicado</span>')
        
        if obj.available:
            badges.append('<span style="background-color: #007bff; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; margin-left: 5px;">Disponível</span>')
        else:
            badges.append('<span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; margin-left: 5px;">Indisponível</span>')
        
        return format_html(" ".join(badges))
    
    @admin.display(description=_("WhatsApp"))
    def whatsapp_display(self, obj):
        return format_html(
            '<a href="{}" target="_blank" style="color: #25D366; text-decoration: none;">📱 {}</a>',
            obj.whatsapp_link,
            obj.phone_whatsapp
        )
    
    @admin.display(description=_("Preview WhatsApp"))
    def whatsapp_preview(self, obj):
        if obj.phone_whatsapp:
            return format_html(
                '<a href="{}" target="_blank" class="button" style="background-color: #25D366; color: white;">Testar WhatsApp</a>',
                obj.whatsapp_link
            )
        return "-"
    
    @admin.action(description=_("Publicar perfis selecionados"))
    def publish_profiles(self, request, queryset):
        updated = queryset.update(published=True)
        self.message_user(request, f"{updated} perfil(is) publicado(s) com sucesso.")
    
    @admin.action(description=_("Despublicar perfis selecionados"))
    def unpublish_profiles(self, request, queryset):
        updated = queryset.update(published=False)
        self.message_user(request, f"{updated} perfil(is) despublicado(s) com sucesso.")
    
    @admin.action(description=_("Marcar como disponível"))
    def mark_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f"{updated} perfil(is) marcado(s) como disponível(is).")
    
    @admin.action(description=_("Marcar como indisponível"))
    def mark_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f"{updated} perfil(is) marcado(s) como indisponível(is).")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("user")
