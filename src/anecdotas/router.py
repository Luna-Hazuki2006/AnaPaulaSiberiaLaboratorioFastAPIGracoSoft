from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine #!aaaaaaa
import anecdotas.models as models 
import anecdotas.schemas as schemas
import anecdotas.service as service

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('', response_model=list[schemas.Anecdota])
def listar_anecdota(db: Session = Depends(get_db)):
    return service.listar_tipos_anecdota(db=db)

@router.post('', response_model=schemas.Anecdota)
def crear_anecdota(anecdota: schemas.AnecdotaCrear, db: Session = Depends(get_db)):
    return service.crear_anecdota(db=db, anecdota=anecdota)

@router.get('/{id}', response_model=schemas.Anecdota)
def buscar_anecdota(id : int, db: Session = Depends(get_db)): 
    return service.buscar_anecdota(db=db, id=id)

@router.put('/{id}', response_model=schemas.Anecdota)
def modificar_anecdota(id : int, anecdota: schemas.AnecdotaCrear, db: Session = Depends(get_db)): 
    return service.modificar_anecdota(db=db, id=id, anecdota=anecdota)

@router.delete('/{id}', response_model=schemas.Anecdota)
def eliminar_anecdota(id : int, db: Session = Depends(get_db)): 
    return service.eliminar_anecdota(db=db, id=id)