import logging
import os 
import pytest_check as check 

os.makedirs("logs",exist_ok=True) #fileExistsError

logging.basicConfig(
    filename="logs/execution.logs",
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s - %(message)s',
    force=True

)
logger = logging.getLogger(__name__)


def get_logger():
    """Retorna el logger configurado para usar en los tests"""
    return logger