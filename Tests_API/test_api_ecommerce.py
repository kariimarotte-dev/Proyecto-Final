import pytest
import requests

#BASE URL de la API publica que usaremos para la pruebas 
BASE_URL = "https://shopping-kohl-tau.vercel.app"

# 1. caso de prueba: get (obtener productos y validar estructura)
def test_get_products_success():
    response = requests.get(f"{BASE_URL}/api/products")

    if response.status_code == 400:
        response = requests.get(f"{BASE_URL}/")
