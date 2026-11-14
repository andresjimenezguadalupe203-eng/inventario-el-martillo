from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='producto_lista'),
    path('nuevo/', views.ProductoCreateView.as_view(), name='producto_nuevo'),
    path('<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_editar'),
    path('<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_eliminar'),

    path('clientes/', views.ClienteListView.as_view(), name='cliente_lista'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente_nuevo'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_eliminar'),
]