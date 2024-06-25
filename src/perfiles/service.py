from compras.models import Compra
from tipos_compra.models import Tipo_Compra
from productos.models import Producto
from estados_compras.models import Estado_Compra
from facturas.models import Factura
from cotizaciones.models import Cotizacion
from usuarios.models import Usuario
from sqlalchemy.orm import Session

def listar_compras_cliente(db: Session, cedula: str): 
    lista = db.query(Compra).filter(Compra.cliente_cedula == cedula).all()
    facturas = db.query(Factura).all()
    lista_final = []
    for esto in lista: 
        try: 
            final = {}
            final['producto'] = db.query(Producto).filter(Producto.id == esto.producto_id).first()
            final['cantidad'] = esto.cantidad
            final['vendedor'] = db.query(Usuario).filter(Usuario.cedula == final['producto'].usuario_cedula).first()
            for esta in facturas: 
                real = db.query(Cotizacion).filter(Cotizacion.id == esta.cotizacion_id).first()
                if real != None: 
                    final['monto_total'] = final['cantidad'] * real.precio
                    lista_final.append(final)
        except Exception: 
            continue
    return lista_final