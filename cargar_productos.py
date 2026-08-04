# cargar_productos.py
# Script para cargar algunos productos de ejemplo en la base de datos,
# así podemos probar el catálogo con datos reales.

from database import SessionLocal
from models import Producto

db = SessionLocal()

productos_ejemplo = [
    {
        "nombre": "Mouse Logitech G502",
        "descripcion": "Mouse gamer con sensor de alta precisión",
        "precio_original": 45000,
        "descuento_pct": 20,
        "stock": 30,
        "marca": "Logitech",
        "categoria": "Periféricos",
        "destacado": True,
    },
    {
        "nombre": "Teclado HyperX Alloy",
        "descripcion": "Teclado mecánico gamer con RGB",
        "precio_original": 80000,
        "descuento_pct": 15,
        "stock": 20,
        "marca": "HyperX",
        "categoria": "Periféricos",
        "destacado": True,
    },
    {
        "nombre": "Monitor Samsung Odyssey",
        "descripcion": "Monitor curvo 27 pulgadas 144Hz",
        "precio_original": 350000,
        "descuento_pct": 8,
        "stock": 8,
        "marca": "Samsung",
        "categoria": "Monitores",
        "destacado": False,
    },
]

for datos in productos_ejemplo:
    producto = Producto(**datos)  # ** "desempaqueta" el diccionario como argumentos
    producto.precio_venta = producto.calcular_precio_venta()  # usamos el método que ya escribimos
    db.add(producto)

db.commit()
print(f"Se cargaron {len(productos_ejemplo)} productos")