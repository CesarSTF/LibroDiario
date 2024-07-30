from django.urls import path
from . import views

urlpatterns = [
    path('', views.libro_diario, name='libro_diario'),
    path('entrada/<int:libro_diario_id>/', views.entrada_diario, name='entrada_diario'),

]
