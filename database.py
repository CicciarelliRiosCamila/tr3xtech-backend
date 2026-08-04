from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./tr3xtech.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
def get_db():
    # Esta función se la vamos a "inyectar" a cada endpoint que necesite la base de datos.
    # Abre una sesión, se la presta al endpoint, y pase lo que pase, la cierra al final.
    db = SessionLocal()
    try:
        yield db  # "yield" en vez de "return": le presta la sesión, no la entrega para siempre
    finally:
        db.close()  # esto se ejecuta siempre, haya error o no