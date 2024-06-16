from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import compras.models as models 
import compras.schemas as schemas
import compras.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Compra])
def listar_compra(db: Session = Depends(get_db)):
    return service.listar_compras(db=db)

@router.post('', response_model=schemas.Compra)
def crear_compra(compra: schemas.CompraCrear, db: Session = Depends(get_db)):
    return service.crear_compra(db=db, compra=compra)

@router.get('/{id}', response_model=schemas.Compra)
def buscar_compra(id : int, db: Session = Depends(get_db)): 
    return service.buscar_compra(db=db, id=id)

@router.put('/{id}', response_model=schemas.Compra)
def modificar_compra(id : int, compra: schemas.CompraCrear, db: Session = Depends(get_db)): 
    return service.modificar_compra(db=db, id=id, compra=compra)

@router.delete('/{id}', response_model=schemas.Compra)
def eliminar_compra(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_compra(db=db, id=id)