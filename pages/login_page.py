from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

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
        self.campo_buscar = (By.CSS_SELECTOR, "input[placeholder*='Buscar']") # Busca por el texto del placeholder (con mayúscula)
        self.boton_buscar = (By.CSS_SELECTOR, "button[type='submit']")
        
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
        # Esperar a que la URL cambie después del login
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda d: "login" not in d.current_url) 

    def obtener_texto_error(self):
        try:
            wait = WebDriverWait(self.driver, 5)
            elemento_error = wait.until(EC.presence_of_element_located(self.mensaje_error))
            return elemento_error.text
        except TimeoutException:
            # Si no encuentra el elemento por ID, buscar cualquier mensaje de error visible
            try:
                error_generico = self.driver.find_element(By.XPATH, "//*[contains(@class, 'error') or contains(@class, 'alert')]")
                return error_generico.text
            except NoSuchElementException:
                return ""
    
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
        try:
            wait = WebDriverWait(self.driver, 10)
            boton_agregar = wait.until(EC.element_to_be_clickable(self.boton_agregar_carrito))
            boton_agregar.click()
            # Esperar a que el contador del carrito se actualice
            wait.until(lambda d: "0" not in d.find_element(*self.icono_carrito).text if d.find_elements(*self.icono_carrito) else False)
        except TimeoutException:
            print("No se pudo encontrar el botón para agregar al carrito")
    
    def ir_al_carrito_y_pagar(self):
        """Navega al carrito y procede al checkout"""
        try:
            wait = WebDriverWait(self.driver, 10)
            
            # Hacer clic en el ícono del carrito
            icono = wait.until(EC.element_to_be_clickable(self.icono_carrito))
            icono.click()
            
            # Hacer clic en el botón de checkout/pagar
            boton_pagar = wait.until(EC.element_to_be_clickable(self.boton_checkout))
            boton_pagar.click()
            # Esperar a que aparezca el mensaje de compra exitosa
            wait.until(EC.presence_of_element_located(self.mensaje_exito_compra))
        except TimeoutException:
            print("No se pudo completar el proceso de checkout")
    
    def obtener_mensaje_compra_exitosa(self):
        """Obtiene el mensaje de confirmación de compra exitosa"""
        try:
            wait = WebDriverWait(self.driver, 10)
            mensaje = wait.until(EC.presence_of_element_located(self.mensaje_exito_compra))
            return mensaje.text
        except TimeoutException:
            # Buscar cualquier mensaje de éxito alternativo
            try:
                mensaje_generico = self.driver.find_element(By.XPATH, "//*[contains(@class, 'success') or contains(text(), 'éxito') or contains(text(), 'gracias')]")
                return mensaje_generico.text
            except NoSuchElementException:
                return ""