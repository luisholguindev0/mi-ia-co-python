import sys
import os

try:
    # Asegurar que el directorio raíz está en el path para poder importar 'src'
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Intentar importar la aplicación principal
    from src.main import app

except Exception as e:
    # Si falla la importación, crear una app de respuesta de error
    # Esto nos permitirá ver POR QUÉ falla en Vercel
    from fastapi import FastAPI
    import traceback
    
    app = FastAPI()
    
    @app.get("/{path:path}")
    @app.post("/{path:path}")
    def catch_startup_error(path: str):
        return {
            "status": "startup_error", 
            "error": str(e), 
            "traceback": traceback.format_exc().splitlines()
        }
