import pytest
import json
from pages.login_page import LoginPage
from utils.logger import get_logger

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Función auxiliar para leer los datos del archivo externo JSON
def cargar_datos():
    with open("datos_prueba.json", "r") as archivo:
        return json.load(archivo)


# CASO 1: Escenario Negativo - Login fallido con credenciales inválidas

def test_caso1_login_invalido_muestra_error(driver):
    datos = cargar_datos()
    login = LoginPage(driver)
    
    login.abrir_pagina()
    login.iniciar_sesion(datos["usuario_invalido"]["user"], datos["usuario_invalido"]["pass"])
    
    error_visible = login.obtener_texto_error()
    assert len(error_visible) > 0, "Error: El sistema no mostró ningún mensaje de alerta."


# CASO 2: Escenario Positivo - Login exitoso con credenciales válidas

def test_caso2_login_valido_exitoso(driver):
    datos = cargar_datos()
    login = LoginPage(driver)
    
    login.abrir_pagina()
    login.iniciar_sesion(datos["usuario_valido"]["user"], datos["usuario_valido"]["pass"])
    
    # Validamos que ya no estemos atrapados en la URL de login
    assert "login" not in driver.current_url, "Error: No se pudo ingresar a la cuenta."

# CASO 3: Flujo de navegación de productos

def test_caso3_buscar_producto_existente(driver):
    datos = cargar_datos()
    login = LoginPage(driver)

    login.abrir_pagina()
    login.iniciar_sesion(datos["usuario_valido"]["user"], datos["usuario_valido"]["pass"])
    
    # Buscar producto
    login.buscar_producto(datos["producto_busqueda"])
    
    # Esperar dinámicamente a que la URL cambie a búsqueda
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    wait = WebDriverWait(driver, 100)
    wait.until(lambda d: "search" in d.current_url or "query" in d.current_url)
    
    assert "search" in driver.current_url or "query" in driver.current_url, "Error: El buscador no actualizó la URL."


 # CASO 4: Añadir Producto al Carrito de Compras

def test_caso4_agregar_productos_al_carrito(driver):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    datos = cargar_datos()
    login = LoginPage(driver)
    
    login.abrir_pagina()
    login.iniciar_sesion(datos["usuario_valido"]["user"], datos["usuario_valido"]["pass"])
    login.buscar_producto(datos["producto_busqueda"])
    
    # Añadimos el producto al carrito
    login.agregar_primer_producto_al_carrito()
    
    # Esperamos a que el ícono del carrito esté presente y actualizado
    wait = WebDriverWait(driver, 100)
    icono_carrito = wait.until(EC.presence_of_element_located(login.icono_carrito))
    
    # Validamos que el carrito tenga al menos 1 elemento activo
    assert "0" not in icono_carrito.text, "Error: El producto no se sumó al contador del carrito."

# CASO 5: Flujo completo - Checkout de compra exitoso

def test_caso5_flujo_de_checkout_completo(driver):
    datos = cargar_datos()
    login = LoginPage(driver)

    login.abrir_pagina()
    login.iniciar_sesion(datos["usuario_valido"]["user"], datos["usuario_valido"]["pass"])
    login.buscar_producto(datos["producto_busqueda"])
    login.agregar_primer_producto_al_carrito()
    
    login.ir_al_carrito_y_pagar()

    # Esperar dinámicamente a que aparezca el mensaje de compra
    wait = WebDriverWait(driver, 100)
    wait.until(EC.presence_of_element_located(login.mensaje_exito_compra))

    mensaje_final = login.obtener_mensaje_compra_exitosa()
    assert "gracias por tu compra" in mensaje_final.lower() or "pago exito" in mensaje_final.lower(), "Error: No se completó la compra exitosamente." 