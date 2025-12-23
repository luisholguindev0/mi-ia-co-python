import sys
import os

# Asegurar que el directorio raíz está en el path para poder importar 'src'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la aplicación FastAPI
from src.main import app

# Vercel serverless function entrypoint
# app es el objeto FastAPI
