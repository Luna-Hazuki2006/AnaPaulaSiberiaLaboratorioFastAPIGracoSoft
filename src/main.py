import uvicorn

from fastapi import FastAPI, Request, Depends

from categorias import router as categorias
from estados_compras import router as estados_compras
from estados_cotizacion import router as estados_cotizacion
from metodos_envios import router as metodos_envios
from tipos_compra import router as tipos_compra
from metodos_pagos import router as metodos_pagos
from estados_caracteristicas import router as estados_caracteristicas
from tipos_usuario import router as tipos_usuario
from tipos_producto import router as tipos_productos
from usuarios import router as usuarios
from productos import router as productos
from calificaciones import router as calificaciones
from reseñas import router as reseñas
from anecdotas import router as anecdotas
from compras import router as compras
from caracteristicas import router as caracteristicas
from cotizaciones import router as cotizaciones
from facturas import router as facturas
from productos.service import get_productos_por_artesano

from usuarios.service import RequiresLoginException, AuthHandler, listar_artesanos
from usuarios.service import LoginExpired

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, Response, HTMLResponse
from database import SessionLocal, engine 
from sqlalchemy.orm import Session

auth_handler = AuthHandler()

app = FastAPI()

app.mount("/static", StaticFiles(directory="./../static"), name="static")

templates = Jinja2Templates(directory="./../templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(categorias.router, prefix='/categorias')
app.include_router(estados_compras.router, prefix='/estados_compras')
app.include_router(estados_cotizacion.router, prefix='/estados_cotizacion')
app.include_router(metodos_envios.router, prefix='/metodos_envios')
app.include_router(tipos_compra.router, prefix='/tipos_compras')
app.include_router(metodos_pagos.router, prefix='/metodos_pagos')
app.include_router(estados_caracteristicas.router, prefix='/estados_caracteristicas')
app.include_router(tipos_usuario.router, prefix='/tipos_usuarios')
app.include_router(tipos_productos.router, prefix='/tipos_productos')
app.include_router(usuarios.router)
app.include_router(productos.router, prefix='/productos')
app.include_router(calificaciones.router, prefix='/calificaciones')
app.include_router(reseñas.router, prefix='/reseñas')
app.include_router(anecdotas.router, prefix='/anecdotas')
app.include_router(compras.router, prefix='/compras')
app.include_router(caracteristicas.router, prefix='/caracteristicas')
app.include_router(cotizaciones.router, prefix='/cotizaciones')
app.include_router(facturas.router, prefix='/facturas')


@app.get('/home')
async def home(request: Request, db: Session = Depends(get_db), info=Depends(auth_handler.auth_wrapper)):
        print(info)
        if info["tipo_usuario_id"] == 1: 
            lista = get_productos_por_artesano(db=db, cedula_artesano=info['cedula'])
            return templates.TemplateResponse('/homes/artesanos.html', 
                                              {'request': request, 
                                               "info": info, 
                                               'lista': lista})
        elif info["tipo_usuario_id"] == 2: 
            lista = listar_artesanos(db=db)
            return templates.TemplateResponse('/homes/clientes.html', 
                                              {'request': request, 
                                               "info": info, 
                                               'lista': lista})
        else: 
            return {'hola': info}

@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return templates.TemplateResponse("message-redirection.html", {"request": request, "message": exc.message, "path_route": exc.path_route, "path_message": exc.path_message})

@app.exception_handler(LoginExpired)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return templates.TemplateResponse("message-redirection.html", {"request": request, "message": exc.message, "path_route": exc.path_route, "path_message": exc.path_message})

@app.middleware("http")
async def create_auth_header(request: Request, call_next,):
    '''
    Check if there are cookies set for authorization. If so, construct the
    Authorization header and modify the request (unless the header already
    exists!)
    '''
    if ("Authorization" not in request.headers 
        and "Authorization" in request.cookies
        ):
        access_token = request.cookies["Authorization"]
        
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                 f"Bearer {access_token}".encode(),
            )
        )
    elif ("Authorization" not in request.headers 
        and "Authorization" not in request.cookies
        ): 
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                 f"Bearer 12345".encode(),
            )
        )
        
    response = await call_next(request)
    return response    



#https://fastapi.tiangolo.com/tutorial/bigger-applications/
#https://github.com/zhanymkanov/fastapi-best-practices#1-project-structure-consistent--predictable
#https://rummanahmar.medium.com/master-fastapi-build-a-full-stack-todo-application-8efe01fb761f

# prueba


#Para debbugear :(
# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)