from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cuidadores, name='lista_cuidadores'),
    path('novo/', views.novo_cuidador, name='novo_cuidador'),
]
