# schemas.py
# Acá definimos qué forma tienen los datos que ENTRAN y SALEN de la API,
# separado de cómo se guardan en la base de datos (eso está en models.py)

from pydantic import BaseModel, EmailStr
from typing import Optional


class UsuarioRegistro(BaseModel):
    # Esto es lo que esperamos que nos mande el frontend para registrarse
    usuario: str
    contrasena: str  # acá SÍ va en texto plano, todavía no la hasheamos
    email: EmailStr  # EmailStr valida automáticamente que tenga formato de email válido
    nombre_completo: str
    direccion_envio: Optional[str] = None  # Optional = no es obligatorio


class UsuarioOut(BaseModel):
    # Esto es lo que la API devuelve como respuesta. Notá que NO incluye la contraseña.
    id_usuario: int
    usuario: str
    email: str
    nombre_completo: str
    rol: str

    class Config:
        from_attributes = True  # le permite a Pydantic leer esto directo desde un objeto Usuario de SQLAlchemy
        # --- Schemas para login ---

class UsuarioLogin(BaseModel):
    usuario: str
    contrasena: str


class Token(BaseModel):
    access_token: str
    token_type: str
    # --- Schema para Productos ---

class ProductoOut(BaseModel):
    id_producto: int
    nombre: str
    descripcion: Optional[str] = None
    precio_original: float
    precio_venta: float
    descuento_pct: float
    stock: int
    marca: Optional[str] = None
    categoria: str
    imagen: Optional[str] = None
    destacado: bool

    class Config:
        from_attributes = True
        # --- Schemas para el Carrito ---

class AgregarAlCarrito(BaseModel):
    id_producto: int
    cantidad: int = 1  # si no se especifica, agrega 1 unidad por defecto


class ItemCarritoOut(BaseModel):
    id_producto: int
    nombre: str
    precio_unitario: float
    cantidad: int
    subtotal_item: float


class CarritoOut(BaseModel):
    # Esto refleja exactamente el panel RESUMEN de tu pantalla de Carrito
    items: list[ItemCarritoOut]
    subtotal: float
    envio: float
    descuento: float
    total: float
    # --- Schemas para el Checkout / Pedidos ---

class ItemPedido(BaseModel):
    id_producto: int
    cantidad: int


class CrearPedido(BaseModel):
    metodo_pago: str  # "Crédito", "Débito", "Transferencia" o "Efectivo"


class PedidoItemOut(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float


class PedidoOut(BaseModel):
    id_pedido: int
    id_usuario: int
    subtotal: float
    envio: float
    descuento: float
    total: float
    metodo_pago: str
    estado: str
    items: list[PedidoItemOut]

    class Config:
        from_attributes = True