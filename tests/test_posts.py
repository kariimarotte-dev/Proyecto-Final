import pytest

from pages.ApiShoppingCliente import ApiShoppingClient
from utils.logger import get_logger

api= ApiShoppingClient()
logger = get_logger()
posts_id = 2

def test_get_one_posts():
    logger.info("SE INICIO EL LLAMADO A UN POST a la url : ")
    logger.info(f"")
    posts_id = 2

    res = api.get_posts(posts_id)

    # Validar que la respuesta sea exitosa
    assert res.status_code == 200, f"Error: Se esperaba 200 pero dio {res.status_code}"
    
    # Validar que tenga contenido
    datos = res.json()
    assert len(datos) > 0, "Error: El post regresó vacío"

# TEST API 1: Escenario Positivo - Verificar lista completa de posts
def test_api_obtener_todos_los_posts_exitoso():
    api = ApiShoppingClient()
    respuesta = api.get_todos_los_posts()
    
    # Validamos que el servidor de la tienda responda 200 OK
    assert respuesta.status_code == 200, f"Error: Se esperaba 200 pero dio {respuesta.status_code}"
    
    # Validamos que devuelva una lista de publicaciones
    datos = respuesta.json()
    assert isinstance(datos, list), "Error: La API no devolvió una lista de posts."

    
# TEST API 2: Escenario Positivo - Verificar un post específico por su ID

def test_api_obtener_un_post_por_id():
    api = ApiShoppingClient()
    respuesta = api.get_posts(1)  # Buscamos el post con ID 1
    
    # Validamos que si el post existe, el servidor responda exitosamente
    assert respuesta.status_code == 200, f"Error: No se pudo traer el post 1. Código: {respuesta.status_code}"
    
    datos = respuesta.json()
    assert len(datos) > 0, "Error: El contenido del post regresó vacío."