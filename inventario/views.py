from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import ProductoForm, ClienteForm
from .models import Producto, Cliente

STOCK_BAJO = 5


# ---------- PRODUCTOS ----------
class ProductoListView(ListView):
    model = Producto
    template_name = 'inventario/producto_lista.html'
    context_object_name = 'productos'
    paginate_by = 6

    def get_queryset(self):
        queryset = Producto.objects.select_related('categoria')
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(nombre__icontains=q)
                | Q(codigo_barras__icontains=q)
                | Q(categoria__nombre__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '').strip()
        context['stock_bajo_limite'] = STOCK_BAJO
        context['productos_bajos'] = Producto.objects.filter(stock__lte=STOCK_BAJO).count()
        return context


class ProductoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_lista')
    success_message = '¡Producto %(nombre)s registrado correctamente!'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.stock <= STOCK_BAJO:
            messages.warning(
                self.request,
                f'Atención: quedan solo {self.object.stock} piezas de {self.object.nombre}.',
            )
        return response


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventario/producto_form.html'
    success_url = reverse_lazy('producto_lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, f'¡Precios/Stock de {self.object.nombre} actualizados!')
        if self.object.stock <= STOCK_BAJO:
            messages.warning(
                self.request,
                f'Atención: quedan solo {self.object.stock} piezas de {self.object.nombre}.',
            )
        return response


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inventario/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_lista')

    def form_valid(self, form):
        nombre = self.object.nombre
        response = super().form_valid(form)
        messages.warning(self.request, f'El producto {nombre} fue retirado del inventario.')
        return response


# ---------- CLIENTES ----------
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'inventario/cliente_lista.html'
    context_object_name = 'clientes'


class ClienteCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'inventario/cliente_form.html'
    success_url = reverse_lazy('cliente_lista')
    success_message = '¡Cliente %(nombre)s registrado correctamente!'


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'inventario/cliente_form.html'
    success_url = reverse_lazy('cliente_lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, f'¡Datos de {self.object.nombre} actualizados!')
        return response


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'inventario/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_lista')

    def form_valid(self, form):
        nombre = self.object.nombre
        response = super().form_valid(form)
        messages.warning(self.request, f'El cliente {nombre} fue eliminado.')
        return response