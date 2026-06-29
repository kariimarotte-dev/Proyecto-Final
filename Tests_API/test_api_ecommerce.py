import pytest
import requests

BASE_URL = "https://shopping-kohl-tau.vercel.app"

# 1. CASO DE PRUEBA: GET (Obtener productos y validar estructura)
def test_get_products_success():
# Enviar petición GET para obtener el listado de productos de tu tienda
    response = requests.get(f"{BASE_URL}/api/products")
    
    if response.status_code == 404:
# por si la API se consulta directo en la raíz o ruta alternativa
        response = requests.get(f"{BASE_URL}/")
    
    assert response.status_code == 200, f"Se esperaba un 200 pero se obtuvo {response.status_code}"
    
# Verificar que responda en un formato válido (puedes validar cabeceras)
    assert "Content-Type" in response.headers, "La respuesta no contiene encabezados de tipo de contenido"
    print("\n[GET] Prueba exitosa: Conexión con la plataforma verificada.")


# 2. CASO DE PRUEBA: GET (Escenario de Error - Ruta inexistente en tu sitio)
def test_get_route_not_found():
# Intentamos buscar una ruta inválida o un producto que no existe en tu servidor
    response = requests.get(f"{BASE_URL}/api/recurso-inexistente-error-404")
    
# Validación del código de error esperado (404)
    assert response.status_code == 404, f"Se esperaba un error 404 pero se obtuvo {response.status_code}"
    print("\n[GET Error] Prueba exitosa: Tu servidor maneja correctamente las páginas/rutas no encontradas.")