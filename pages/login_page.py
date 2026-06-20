from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://shopping-kohl-tau.vercel.app/login"
        
        # Localizadores de Login 
        self.campo_usuario = (By.ID, "username")
        self.campo_password = (By.ID, "password")
        self.boton_ingresar = (By.CSS_SELECTOR, "button[type='submit']")
        self.mensaje_error = (By.ID, "error-message")
        
        # del Buscador y Navegación
        self.campo_buscar = (By.CSS_SELECTOR, "input[placeholder*='buscar']") # Busca por el texto del placeholder
        self.boton_buscar = (By.ID, "search-button")
        
        # de Carrito y Checkout 
        self.boton_agregar_carrito = (By.XPATH, "//button[contains(text(), 'Agregar')]")
        self.icono_carrito = (By.ID, "cart-icon")
        self.boton_checkout = (By.ID, "checkout-button")
        self.mensaje_exito_compra = (By.ID, "success-message")

    def abrir_pagina(self):
        self.driver.get(self.url)

    def iniciar_sesion(self, usuario, contrasenia):
        self.driver.find_element(*self.campo_usuario).send_keys(usuario)
        self.driver.find_element(*self.campo_password).send_keys(contrasenia)
        self.driver.find_element(*self.boton_ingresar).click()

    def obtener_texto_error(self):
        return self.driver.find_element(*self.mensaje_error).text