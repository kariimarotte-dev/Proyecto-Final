from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://shopping-kohl-tau.vercel.app/login"
        
        # Localizadores de Login 
        self.campo_usuario = (By.ID, "username")
        self.campo_password = (By.ID, "password")
        self.boton_ingresar = (By.CSS_SELECTOR, "button[type='submit']")
        self.mensaje_error = (By.CSS_SELECTOR, "[data-testid='login-error']")
        
        # del Buscador y Navegación
        self.campo_buscar = (By.CSS_SELECTOR, "input[placeholder*='Buscar']") # Busca por el texto del placeholder (con mayúscula)
        self.boton_buscar = (By.CSS_SELECTOR, "button[type='submit']")
        
        # de Carrito y Checkout 
        self.boton_agregar_carrito = (By.XPATH, "//button[contains(text(), 'Agregar')]")
        self.icono_carrito = (By.CSS_SELECTOR, "[data-testid='cart-icon']")
        self.badge_carrito = (By.CSS_SELECTOR, "[data-testid='cart-badge']")
        self.boton_checkout = (By.CSS_SELECTOR, "[data-testid='checkout-button']")
        self.mensaje_exito_compra = (By.ID, "success-message")

    def abrir_pagina(self):
        self.driver.get(self.url)

    def iniciar_sesion(self, usuario, contrasenia):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self.campo_usuario)).send_keys(usuario)
        wait.until(EC.presence_of_element_located(self.campo_password)).send_keys(contrasenia)
        wait.until(EC.element_to_be_clickable(self.boton_ingresar)).click()

    def obtener_texto_error(self):
        wait = WebDriverWait(self.driver, 5)
        elemento_error = wait.until(EC.presence_of_element_located(self.mensaje_error))
        return elemento_error.text
        

    def buscar_producto(self, nombre_producto):
        """Busca un producto usando el campo de búsqueda"""
        try:
            wait = WebDriverWait(self.driver, 10)
            campo_buscar = wait.until(EC.presence_of_element_located(self.campo_buscar))
            campo_buscar.clear()
            campo_buscar.send_keys(nombre_producto)
            
            # Intentar hacer clic en el botón de búsqueda si existe
            try:
                boton = wait.until(EC.element_to_be_clickable(self.boton_buscar))
                boton.click()
            except TimeoutException:
                # Si no hay botón, presionar Enter
                from selenium.webdriver.common.keys import Keys
                campo_buscar.send_keys(Keys.RETURN)
            
            # Esperar a que la URL cambie indicando resultados de búsqueda
            wait.until(lambda d: "search" in d.current_url or "query" in d.current_url or len(d.find_elements(*self.boton_agregar_carrito)) > 0)
        except TimeoutException:
            print("No se pudo encontrar el campo de búsqueda")
    
    def agregar_primer_producto_al_carrito(self):
        """Añade el primer producto encontrado al carrito"""
        wait = WebDriverWait(self.driver, 10)
        boton_agregar = wait.until(EC.element_to_be_clickable(self.boton_agregar_carrito))
        boton_agregar.click()
        # Esperar a que el badge del carrito aparezca (solo se renderiza si hay >0 items)
        wait.until(EC.presence_of_element_located(self.badge_carrito))
    
    def ir_al_carrito_y_pagar(self):
        """Navega al carrito y procede al checkout"""
        wait = WebDriverWait(self.driver, 10)

        # Hacer clic en el ícono del carrito
        icono = wait.until(EC.element_to_be_clickable(self.icono_carrito))
        icono.click()

        # Hacer clic en el botón de checkout/pagar
        boton_pagar = wait.until(EC.element_to_be_clickable(self.boton_checkout))
        boton_pagar.click()

        # Esperar a que aparezca el mensaje de compra exitosa
        wait.until(EC.presence_of_element_located(self.mensaje_exito_compra))
    
    def obtener_mensaje_compra_exitosa(self):
        """Obtiene el mensaje de confirmación de compra exitosa"""
        wait = WebDriverWait(self.driver, 10)
        mensaje = wait.until(EC.presence_of_element_located(self.mensaje_exito_compra))
        return mensaje.text
