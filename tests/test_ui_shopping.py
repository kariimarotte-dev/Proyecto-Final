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