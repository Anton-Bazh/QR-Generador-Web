import os
import sys

# Agregar la ruta del proyecto actual al path
project_dir = os.path.dirname(os.path.abspath(__file__))
if project_dir not in sys.path:
    sys.path.append(project_dir)

from app import create_app

# Gunicorn y uWSGI por convención buscan 'app' o 'application'
application = create_app()

if __name__ == "__main__":
    application.run()
