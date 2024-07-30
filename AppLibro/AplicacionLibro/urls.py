from django.urls import path
from . import views

urlpatterns = [
    path('', views.libro_diario, name='libro_diario'),
    path('entrada/<int:libro_diario_id>/', views.entrada_diario, name='entrada_diario'),
    path('entrada/<int:entrada_id>/modificar/', views.modificar_entrada, name='modificar_entrada'),
    path('entrada/<int:entrada_id>/eliminar/', views.eliminar_entrada, name='eliminar_entrada'),
    path('libro_diario/eliminar/<int:id>/', views.eliminar_libro_diario, name='eliminar_libro_diario'),

]
