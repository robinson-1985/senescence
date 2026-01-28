from django.urls import path
from . import views

app_name = "public"

urlpatterns = [
    path("", views.professionals_list, name="professionals_list"),
    path("profissionais/<slug:slug>/", views.professional_detail, name="professional_detail"),
    path("profissionais/<slug:slug>/contato/", views.contact_professional, name="contact_professional"),
    path("profissionais/<slug:slug>/obrigado/", views.thanks, name="thanks"),
]
