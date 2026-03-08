import os
from app import create_app

flask_app = create_app()

if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    print(f"Iniciando servidor mejorado en http://{host}:{port}")
    print(f"Modo debug: {debug_mode}")
    flask_app.run(debug=debug_mode, host=host, port=port)