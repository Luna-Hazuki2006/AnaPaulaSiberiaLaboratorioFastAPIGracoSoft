from sqlalchemy import Column, Integer, String
from database import Base #!aaaaaaa

class Estado_Compra(Base): 
    __tablename__  = "estados_compras"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, index=True)
    descripcion = Column(String, index=True)
