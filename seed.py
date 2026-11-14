from inventario.models import Categoria, Producto

herr = Categoria.objects.get(nombre__iexact='Herramientas')
cano = Categoria.objects.get(nombre__iexact='cañería')
pint = Categoria.objects.get(nombre__iexact='pinturas')

datos = [
    ('Martillo de uña 16 oz', '7501000000001', herr, 120.00, 15),
    ('Desarmador plano', '7501000000002', herr, 45.50, 30),
    ('Pinzas de presión', '7501000000003', herr, 185.00, 2),
    ('Llave ajustable 10 pulgadas', '7501000000004', herr, 210.00, 8),
    ('Tubo PVC 1/2 pulgada', '7501000000005', cano, 65.00, 25),
    ('Codo PVC 90 grados', '7501000000006', cano, 12.00, 40),
    ('Cinta teflón', '7501000000007', cano, 18.50, 3),
    ('Pintura vinílica blanca 4 L', '7501000000008', pint, 389.00, 12),
    ('Brocha 4 pulgadas', '7501000000009', pint, 55.00, 20),
]

for nombre, codigo, cat, precio, stock in datos:
    Producto.objects.get_or_create(
        codigo_barras=codigo,
        defaults={'nombre': nombre, 'categoria': cat, 'precio': precio, 'stock': stock},
    )

print('Productos en la base:', Producto.objects.count())