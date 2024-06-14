from fastapi import FastAPI
from categorias import router as categorias
from estados_compras import router as estados_compras
from estados_cotizacion import router as estados_cotizacion
from metodos_envios import router as metodos_envios
from tipos_compra import router as tipos_compra
from metodos_pagos import router as metodos_pagos
from estados_caracteristicas import router as estados_caracteristicas
from tipos_usuario import router as tipos_usuario
from tipos_producto import router as tipos_productos

app = FastAPI()

app.include_router(categorias.router, prefix='/categorias')
app.include_router(estados_compras.router, prefix='/estados_compras')
app.include_router(estados_cotizacion.router, prefix='/estados_cotizacion')
app.include_router(metodos_envios.router, prefix='/metodos_envios')
app.include_router(tipos_compra.router, prefix='/tipos_compras')
app.include_router(metodos_pagos.router, prefix='/metodos_pagos')
app.include_router(estados_caracteristicas.router, prefix='/estados_caracteristicas')
app.include_router(tipos_usuario.router, prefix='/tipos_usuarios')
app.include_router(tipos_productos.router, prefix='/tipos_productos')


@app.get('/')
def home():
    return {"message": "Hello world"}

#https://fastapi.tiangolo.com/tutorial/bigger-applications/
#https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable

# prueba