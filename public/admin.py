from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "created_at_formatted",
        "name",
        "phone_formatted",
        "profile",
        "contacted_badge",
        "message_preview"
    )
    
    search_fields = (
        "name",
        "phone",
        "message",
        "profile__display_name",
        "profile__city"
    )
    
    list_filter = (
        "contacted",
        "created_at",
        "profile__city",
        "profile__is_caregiver"
    )
    
    readonly_fields = ("created_at", "profile_link")
    
    fieldsets = (
        (_("Informações do Lead"), {
            "fields": ("name", "phone", "message")
        }),
        (_("Profissional"), {
            "fields": ("profile", "profile_link")
        }),
        (_("Gestão"), {
            "fields": ("contacted", "notes")
        }),
        (_("Data"), {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )
    
    actions = ["mark_as_contacted", "mark_as_not_contacted"]
    list_per_page = 25
    date_hierarchy = "created_at"
    
    @admin.display(description=_("Data/Hora"), ordering="created_at")
    def created_at_formatted(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M")
    
    @admin.display(description=_("Telefone"))
    def phone_formatted(self, obj):
        formatted = obj.get_phone_formatted()
        if formatted:
            return format_html(
                '<a href="tel:{}" style="color: #007bff;">📞 {}</a>',
                obj.phone,
                formatted
            )
        return "-"
    
    @admin.display(description=_("Status"), ordering="contacted")
    def contacted_badge(self, obj):
        if obj.contacted:
            return format_html(
                '<span style="background-color: #28a745; color: white; '
                'padding: 3px 8px; border-radius: 3px; font-size: 11px;">'
                '✓ Contatado</span>'
            )
        else:
            return format_html(
                '<span style="background-color: #dc3545; color: white; '
                'padding: 3px 8px; border-radius: 3px; font-size: 11px;">'
                '✗ Pendente</span>'
            )
    
    @admin.display(description=_("Mensagem"))
    def message_preview(self, obj):
        if len(obj.message) > 50:
            return f"{obj.message[:50]}..."
        return obj.message
    
    @admin.display(description=_("Ver Perfil"))
    def profile_link(self, obj):
        if obj.profile:
            url = f"/admin/profiles/professionalprofile/{obj.profile.pk}/change/"
            return format_html(
                '<a href="{}" target="_blank">🔗 {}</a>',
                url,
                obj.profile.display_name
            )
        return "-"
    
    @admin.action(description=_("Marcar como contatado"))
    def mark_as_contacted(self, request, queryset):
        updated = queryset.update(contacted=True)
        self.message_user(request, f"{updated} lead(s) marcado(s) como contatado(s).")
    
    @admin.action(description=_("Marcar como NÃO contatado"))
    def mark_as_not_contacted(self, request, queryset):
        updated = queryset.update(contacted=False)
        self.message_user(request, f"{updated} lead(s) marcado(s) como NÃO contatado(s).")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("profile", "profile__user")
