# models.py
# Acá definimos las "tablas" de la base de datos como clases de Python.
# SQLAlchemy se encarga de traducir esto a SQL por detrás.

from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text
from database import Base  # Base es la clase que creamos en database.py


class Producto(Base):
    # __tablename__ le dice a SQLAlchemy cómo se va a llamar la tabla en la base
    __tablename__ = "productos"

    # Cada Column es una columna de la tabla.
    # primary_key=True significa que este campo identifica de forma única a cada fila
    # autoincrement=True hace que el número se genere solo (1, 2, 3...) sin que lo pongamos nosotros
    id_producto = Column(Integer, primary_key=True, autoincrement=True)

    nombre = Column(String(150), nullable=False)  # nullable=False = obligatorio
    descripcion = Column(Text, nullable=True)      # nullable=True = opcional

    precio_original = Column(Numeric(10, 2), nullable=False)  # Numeric(10,2) = hasta 10 dígitos, 2 decimales
    precio_venta = Column(Numeric(10, 2), nullable=False)
    descuento_pct = Column(Numeric(5, 2), nullable=False, default=0)  # default=0 si no se especifica

    stock = Column(Integer, nullable=False, default=0)
    marca = Column(String(80), nullable=True)
    categoria = Column(String(80), nullable=False)
    imagen = Column(String(255), nullable=True)  # acá guardamos la ruta o URL de la imagen
    destacado = Column(Boolean, nullable=False, default=False)

    def calcular_precio_venta(self):
        # RN04 de tu documento: precio_venta = precio_original * (1 - descuento_pct/100)
        return round(float(self.precio_original) * (1 - float(self.descuento_pct) / 100), 2)
    # --- Modelo de Usuario ---
# Representa a cada persona que se registra en el sistema (sección 7.2 del documento)

import enum
from sqlalchemy import Enum


class RolUsuario(str, enum.Enum):
    # enum.Enum limita los valores posibles a solo estas tres opciones,
    # así evitamos que alguien escriba mal un rol (ej: "administrador" en vez de "Administrador")
    VISITANTE = "Visitante"
    REGISTRADO = "Registrado"
    ADMINISTRADOR = "Administrador"


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)

    usuario = Column(String(50), unique=True, nullable=False)  # unique=True: no puede repetirse
    contrasena_hash = Column(String(255), nullable=False)      # acá va el hash, nunca la contraseña real
    email = Column(String(120), unique=True, nullable=False)
    nombre_completo = Column(String(150), nullable=False)
    rol = Column(Enum(RolUsuario), nullable=False, default=RolUsuario.REGISTRADO)
    direccion_envio = Column(String(255), nullable=True)
    # --- Modelo de Pedido ---
# Representa una compra completa (sección 7.3 del documento)

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class MetodoPago(str, enum.Enum):
    CREDITO = "Crédito"
    DEBITO = "Débito"
    TRANSFERENCIA = "Transferencia"
    EFECTIVO = "Efectivo"


class EstadoPedido(str, enum.Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO = "Confirmado"
    EN_CAMINO = "En camino"
    ENTREGADO = "Entregado"


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)

    # ForeignKey: este pedido "pertenece" a un usuario que ya existe en la tabla usuarios
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)

    subtotal = Column(Numeric(10, 2), nullable=False)
    envio = Column(Numeric(10, 2), nullable=False, default=0)
    descuento = Column(Numeric(10, 2), nullable=False, default=0)
    total = Column(Numeric(10, 2), nullable=False)

    metodo_pago = Column(Enum(MetodoPago), nullable=False)
    estado = Column(Enum(EstadoPedido), nullable=False, default=EstadoPedido.PENDIENTE)

    # server_default=func.now() hace que la base de datos ponga la fecha/hora actual sola
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    # Esto NO crea una columna. Es un atajo de Python: permite escribir
    # pedido.usuario para acceder al Usuario dueño de este pedido.
    usuario = relationship("Usuario", backref="pedidos")


class PedidoItem(Base):
    # Un pedido puede tener VARIOS productos. Como una tabla no puede tener
    # "una lista" adentro de una columna, usamos una tabla aparte: cada fila
    # acá es "un producto dentro de un pedido específico".
    __tablename__ = "pedido_items"

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(Integer, ForeignKey("pedidos.id_pedido"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)

    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)  # precio al momento de la compra

    pedido = relationship("Pedido", backref="items")
    producto = relationship("Producto")