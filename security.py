# security.py
# Funciones para hashear y verificar contraseñas, y para manejar tokens JWT

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
import models

# --- Hashing de contraseñas ---

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashear_contrasena(contrasena_plana: str) -> str:
    return pwd_context.hash(contrasena_plana)


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    return pwd_context.verify(contrasena_plana, contrasena_hash)


# --- Manejo de tokens JWT ---

CLAVE_SECRETA = "tr3xtech-clave-secreta-2026"
ALGORITMO = "HS256"
MINUTOS_EXPIRACION = 480


def crear_token(id_usuario: int) -> str:
    datos = {"sub": str(id_usuario)}
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    datos["exp"] = expira
    return jwt.encode(datos, CLAVE_SECRETA, algorithm=ALGORITMO)


def leer_token(token: str):
    try:
        payload = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        return payload.get("sub")
    except Exception:
        return None


# --- Protección de endpoints ---

security_scheme = HTTPBearer()


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> models.Usuario:
    token = credenciales.credentials

    error_credenciales = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
    )

    id_usuario = leer_token(token)
    if id_usuario is None:
        raise error_credenciales

    usuario = db.query(models.Usuario).filter(
        models.Usuario.id_usuario == int(id_usuario)
    ).first()

    if usuario is None:
        raise error_credenciales

    return usuario