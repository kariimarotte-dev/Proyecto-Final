import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime 

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
            "id": "prod-015",
            "name": "Clean Code",
            "description": "Manual de artesanía de software por Robert C. Martin.",
            "price": 35,
            "stock": 10,
            "category": "Books",
            "imageUrl": "https://picsum.photos/seed/prod-015/400/300",
            "active": True,
            "createdAt": "2026-01-15T00:00:00.000Z"
    }


# FIXTURE 3: Datos de ejemplo para tests de Usuarios
@pytest.fixture
def users_data():
    """Estructura de datos de un usuario"""
    return {
            "id": "81dcd757-d0b8-48c5-853b-e4127d18bc14",
            "username": "admin",
            "email": "admin@shop.test",
            "role": "admin",
            "name": "Admin User",
            "createdAt": "2026-01-01T00:00:00.000Z"
    }

# para capturar screenshot
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 1. Ejecutar el test normalmente
    outcome = yield
    report = outcome.get_result()
    
    # 2. Verificar si el test FALLÓ
    if report.when == "call" and report.failed:
        # 3. Intentar obtener el driver del test
        driver = item.funcargs.get('driver')
        
    # 4. Si hay driver (test de UI), capturar screenshot
    if driver:
    # 5. Crear nombre descriptivo con fecha/hora
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        test_name = item.name
        screenshot_name = f"screenshots/{test_name}_FAILED_{timestamp}.png"
            
    # 6. Guardar el screenshot
        driver.save_screenshot(screenshot_name)
        print(f"\n📸 Screenshot guardado: {screenshot_name}")
