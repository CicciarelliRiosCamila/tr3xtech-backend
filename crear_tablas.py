from database import Base, engine
import models  # esto hace que Python 'lea' la clase Producto antes de crear las tablas

Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente")