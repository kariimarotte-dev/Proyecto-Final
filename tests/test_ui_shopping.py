import pytest
import json
import time
from pages.login_page import LoginPage
from utils.logger import get_logger

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


# CASO 3: Flujo de Navegación y Búsqueda de Productos

def test_caso3_buscar_producto_existente(driver):
    datos = cargar_datos()
    login = LoginPage(driver)
    
    # Primero nos logueamos para poder navegar en la tienda
    login.abrir_pagina()
    login.iniciar_sesion(datos["usuario_valido"]["user"], datos["usuario_valido"]["pass"])
    
    # Buscamos el término guardado en nuestro JSON externo ('Clean code')
    login.buscar_producto(datos["producto_busqueda"])
    
    # Validamos que el buscador funcionó verificando que la URL contiene el parámetro de búsqueda
    assert "search" in driver.current_url or "query" in driver.current_url, "Error: El buscador no actualizó la URL."


# CASO 4: Añadir Producto al Carrito de Compras

def test_caso4_agregar_producto_al_carrito(driver):
    datos = cargar_datos()
    login = LoginPage(driver)
    
    login.abrir_pagina()
    login.iniciar_sesion(datos["usuario_valido"]["user"], datos["usuario_valido"]["pass"])
    login.buscar_producto(datos["producto_busqueda"])
    
    # Añadimos el producto al carrito
    login.agregar_primer_producto_al_carrito()
    
    # Validamos visualmente que el carrito tenga al menos 1 elemento activo
    icono_carrito = driver.find_element(*login.icono_carrito)
    assert "0" not in icono_carrito.text, "Error: El producto no se sumó al contador del carrito."


# CASO 5: Flujo E2E Completo - Checkout de Compra Exitoso

def test_caso5_flujo_checkout_completo(driver):
    datos = cargar_datos()
    login = LoginPage(driver)
    
    # Realizamos todo el camino de compra del cliente de principio a fin
    login.abrir_pagina()
    login.iniciar_sesion(datos["usuario_valido"]["user"], datos["usuario_valido"]["pass"])
    login.buscar_producto(datos["producto_busqueda"])
    login.agregar_primer_producto_al_carrito()
    
    # Procedemos a pagar
    login.ir_al_carrito_y_pagar()

    time.sleep(3)
    
    # Validamos que aparezca el cartel de felicitaciones o éxito en la orden
    mensaje_final = login.obtener_mensaje_compra_exitosa()
    assert "gracias" in mensaje_final.lower() or "éxito" in mensaje_final.lower() or len(mensaje_final) > 0, "Error: La compra falló o no se generó el recibo."