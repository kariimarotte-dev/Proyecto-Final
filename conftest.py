import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# FIXTURE 1: Driver de Selenium
@pytest.fixture
def driver():
    """
    Crea y configura el navegador Chrome para los tests de UI.
    Se ejecuta antes de cada test y se cierra después.
    """
    # Instalar y configurar ChromeDriver automáticamente
    servicio = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servicio)
    
    # Configuraciones del navegador
    driver.maximize_window()
    driver.implicitly_wait(10)
    
    # Entrega el driver al test
    yield driver
    
    # Cierra el navegador después del test
    driver.quit()


# FIXTURE 2: Datos de ejemplo para tests de Posts/Productos
@pytest.fixture
def posts_data():
    """Estructura de datos de un producto/post de la tienda"""
    return {
        "id": 1,
        "name": "Clean Code",
        "description": "Libro de programación",
        "price": 29.99,
        "stock": 10,
        "category": "Libros",
        "imageUrl": "https://example.com/imagen.jpg",
        "active": True,
        "createdAt": "2024-01-01"
    }


# FIXTURE 3: Datos de ejemplo para tests de Usuarios
@pytest.fixture
def users_data():
    """Estructura de datos de un usuario"""
    return {
        "id": 1,
        "username": "admin",
        "email": "admin@shopping.com",
        "role": "admin",
        "name": "Administrador",
        "createdAt": "2024-01-01"
    }