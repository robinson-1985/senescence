from django.urls import path
from .views import CuidadorListView, CuidadorDetailView, NovoCuidadorView

urlpatterns = [
    path('', CuidadorListView.as_view(), name='cuidador_list'),
    path('novo/', NovoCuidadorView.as_view(), name='novo_cuidador'),
    path('<int:pk>/', CuidadorDetailView.as_view(), name='detalhe'),
]
