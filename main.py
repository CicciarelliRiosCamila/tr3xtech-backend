# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
import security

app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "TR3XTECH backend andando"}


@app.post("/registro", response_model=schemas.UsuarioOut)
def registro(datos: schemas.UsuarioRegistro, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(
        (models.Usuario.usuario == datos.usuario) | (models.Usuario.email == datos.email)
    ).first()

    if existe:
        raise HTTPException(status_code=400, detail="El usuario o el email ya están registrados")

    nuevo_usuario = models.Usuario(
        usuario=datos.usuario,
        contrasena_hash=security.hashear_contrasena(datos.contrasena),
        email=datos.email,
        nombre_completo=datos.nombre_completo,
        direccion_envio=datos.direccion_envio,
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


@app.post("/login", response_model=schemas.Token)
def login(datos: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    # 1. Buscamos al usuario por su nombre de usuario
    usuario = db.query(models.Usuario).filter(models.Usuario.usuario == datos.usuario).first()

    # 2. Si no existe, O si la contraseña no coincide con el hash guardado, rechazamos.
    # Ojo: usamos el MISMO mensaje de error en ambos casos (no decimos cuál de los dos
    # está mal) para no darle pistas a alguien intentando adivinar usuarios válidos.
    if not usuario or not security.verificar_contrasena(datos.contrasena, usuario.contrasena_hash):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

    # 3. Si todo está bien, generamos el token
    token = security.crear_token(usuario.id_usuario)

    return {"access_token": token, "token_type": "bearer"}
@app.get("/perfil", response_model=schemas.UsuarioOut)
def perfil(usuario_actual: models.Usuario = Depends(security.obtener_usuario_actual)):
    # Gracias a la dependencia, acá ya tenemos el Usuario identificado por el token.
    # Ni siquiera necesitamos escribir lógica de validación acá: si el token
    # no era válido, esta función ni se llega a ejecutar.
    return usuario_actual
from typing import Optional


@app.get("/productos", response_model=list[schemas.ProductoOut])
def listar_productos(
    busqueda: Optional[str] = None,
    categoria: Optional[str] = None,
    marca: Optional[str] = None,
    db: Session = Depends(get_db),
):
    # Arrancamos con "todos los productos" y le vamos agregando filtros
    # solo si el que llama al endpoint los mandó.
    query = db.query(models.Producto)

    if busqueda:
        # ilike = "case insensitive LIKE": busca sin importar mayúsculas/minúsculas
        # el % antes y después significa "que contenga este texto en cualquier parte"
        query = query.filter(models.Producto.nombre.ilike(f"%{busqueda}%"))

    if categoria:
        query = query.filter(models.Producto.categoria == categoria)

    if marca:
        query = query.filter(models.Producto.marca == marca)

    return query.all()


@app.get("/productos/destacados", response_model=list[schemas.ProductoOut])
def productos_destacados(db: Session = Depends(get_db)):
    return db.query(models.Producto).filter(models.Producto.destacado == True).all()