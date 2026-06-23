import requests 

class ApiShoppingClient:
    
    def __init__(self):
    
        self.URL_BASE = "https://shopping-kohl-tau.vercel.app"

    def get_product_by_id(self, products_id):
        """
        Este método hace una petición GET para traer un post específico usando su ID.
        Ejemplo: Si pasás post_id = 1, buscará en /posts/1
        """
        # ruta exacta combinando la base con el endpoint /posts/ y el ID
        url_completa = f"{self.URL_BASE}/api/products/{products_id}"
        
        # Hacemos el llamado GET y guardamos lo que nos responde el servidor
        respuesta = requests.get(url_completa)
        
        
        return respuesta

    def get_all_products(self):
        """
        Este método trae la lista completa de publicaciones de la tienda.
        Mapea directamente al endpoint GET /products
        """
        url_completa = f"{self.URL_BASE}/api/products/"
        return requests.get(url_completa)