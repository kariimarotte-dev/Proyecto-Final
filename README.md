# Proyecto Final - Automatización de Testing

## Descripción
Proyecto de testing automatizado para la aplicación de e-commerce Shopping.
Incluye pruebas de interfaz (UI) con Selenium y pruebas de API con Requests.

## Sitio Web Testeado
https://shopping-kohl-tau.vercel.app/

## Estructura del Proyecto
- `pages/` - Page Object Model para UI y clientes API
- `tests/` - Casos de prueba automatizados
- `utils/` - Utilidades (logger)
- `conftest.py` - Configuración de fixtures de pytest
- `datos_prueba.json` - Datos de prueba

## Instalación
```bash
pip install -r requirements.txt
# Todos los tests
pytest

# Solo tests de UI
pytest tests/test_ui_shopping.py

# Solo tests de API
pytest tests/test_posts.py

# Con reporte HTML
pytest --html=reporte.html