# carrito.py
# El carrito vive en memoria (RN05), no en la base de datos.
# Estructura: un diccionario donde la clave es el id_usuario,
# y el valor es OTRO diccionario: { id_producto: cantidad }

carritos_por_usuario = {}


def obtener_carrito_crudo(id_usuario: int) -> dict:
    # setdefault: si el usuario todavía no tiene carrito, le crea uno vacío
    # y lo devuelve. Si ya tenía, devuelve el que ya existía.
    return carritos_por_usuario.setdefault(id_usuario, {})


def agregar_producto(id_usuario: int, id_producto: int, cantidad: int):
    carrito = obtener_carrito_crudo(id_usuario)
    # si el producto ya estaba en el carrito, sumamos a la cantidad existente
    carrito[id_producto] = carrito.get(id_producto, 0) + cantidad


def quitar_producto(id_usuario: int, id_producto: int):
    carrito = obtener_carrito_crudo(id_usuario)
    carrito.pop(id_producto, None)  # el None evita error si no estaba


def vaciar_carrito(id_usuario: int):
    carritos_por_usuario.pop(id_usuario, None)