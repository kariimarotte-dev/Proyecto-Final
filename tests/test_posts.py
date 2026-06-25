import pytest

from pages.ApiShoppingCliente import ApiShoppingClient
from utils.logger import get_logger

api= ApiShoppingClient()
logger = get_logger()
product_id = "prod-018"

def test_get_one_product():
    logger.info(f"SE INICIO EL LLAMADO A UN Producto de la url con ID: {product_id}")

    res = api.get_product_by_id(product_id)

    # Validar que la respuesta sea exitosa
    assert res.status_code == 200, f"Error: Se esperaba 200 pero dio {res.status_code}"

    # Validar que tenga contenido
    datos = res.json()
    assert len(datos) > 0, "Error: El post regresó vacío"
    
    # Extraer el producto de la respuesta
    producto = datos['product']
    
    # Validar que ese objeto tenga una propiedad que sea id 
    assert "id" in producto, "Error: El producto no tiene propiedad id"


# TEST API 1: Escenario Positivo - Verificar lista completa de posts
def test_api_get_all_products_exitoso():
    api = ApiShoppingClient()
    respuesta = api.get_all_products()
    
    # Validamos que el servidor de la tienda responda 200 OK
    assert respuesta.status_code == 200, f"Error: Se esperaba 200 pero dio {respuesta.status_code}"
    
    # Validamos que devuelva una lista de publicaciones
    datos = respuesta.json()
    assert isinstance(datos['items'], list), "Error: La API no devolvió una lista de productos."
    assert len(datos['items']) > 0, "Error: La API no trajo productos"

# TEST API2: Escenario positivo - Verificar un producto especifico por su id 
def test_api_get_a_product_by_id():
    api = ApiShoppingClient()
    # Usar un ID de producto válido con formato esperado por la API
    respuesta = api.get_product("prod-001")

    assert respuesta.status_code == 200, f"Error: No se pudo traer el producto prod-001. Codigo: {respuesta.status_code}"

    datos = respuesta.json()
    assert len(datos) > 0, "Error: el contenido del producto regresó vacio."


#TEST API3: Escenario Negativo - Buscar un id no existe en el sistema
def test_api_get_products_inexistente_da_error():
    api = ApiShoppingClient()

    id_falso = 99999
    respuesta = api.get_product(id_falso)

    assert respuesta.status_code == 404, f"Error: se esperba codigo 404 para un id falso, pero la api devolvió {respuesta.status_code}"