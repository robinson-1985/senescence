from django.urls import path
from .views import CuidadorDetailView, ListaCuidadorView, NovoCuidadorView

urlpatterns = [
    path('', ListaCuidadorView.as_view(), name='cuidadores_lista'),
    path('novo/', NovoCuidadorView.as_view(), name='cuidadores_novo'),
    path('<int:pk>/', CuidadorDetailView.as_view(), name='cuidadores_detalhe'),
]
