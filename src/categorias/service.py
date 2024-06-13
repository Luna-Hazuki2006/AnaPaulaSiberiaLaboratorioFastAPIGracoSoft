from sqlalchemy.orm import Session
import categorias.models as models
import categorias.schemas as schemas

def crear_categoria(db: Session, categoria: schemas.CategoriaCrear):
    db_categoria = models.Categoria(nombre=categoria.nombre, descripcion=categoria.descripcion)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria