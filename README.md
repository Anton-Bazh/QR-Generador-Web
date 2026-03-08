# Generador de Códigos QR

Bienvenido al Generador de Códigos QR, un sistema web profesional, listo para desplegar de forma local o remota en la red empleando arquitectura moderna y modo oscuro avanzado. 

## 1. Requisitos Iniciales
Este despliegue está optimizado para funcionar en entornos Windows / Windows Server de manera nativa sin necesitar configuraciones de IP complejas, contenedores ni tecnologías externas.
Solo necesitas:
* **Python 3.x** instalado en la máquina anfitriona. 
* *Nota: Asegúrate de marcar "Add Python to PATH" durante la instalación si es nuevo.*

## 2. Instalación y Despliegue con 1 clic (Windows Server Local)
Para correr el proyecto en la red local (haciéndolo accesible para todos los dispositivos conectados al módem / LAN corporativa):

1. Abre la carpeta principa del proyecto (`QR-Generador-Web`).
2. Localiza el archivo **`iniciar_servidor.bat`**
3. Da doble clic en él.

**¿Qué hace este script?**
* Escaneará automáticamente tus dependencias locales.
* Instalará **Waitress**, el cual es un servidor WSGI de nivel de producción recomendado para correr sistemas Python en entornos Windows (Flask no se recomienda usar en red sin Waitress/Gunicorn).
* Mostrará la IP local (IPv4) asignada a tu Windows Server. Ej: `192.168.1.5`
* Desplegará la aplicación expuesta en el **Puerto 5000**.

Cualquier dispositivo en la red podrá acceder escribiendo la dirección IP mostrada en su navegador web. Ej: `http://192.168.1.5:5000/`.

## 3. Notas en caso de accesibilidad (Firewall)
Si ejecutas `iniciar_servidor.bat` y otras computadoras en la red no pueden acceder a la herramienta, suele deberse al firewall del servidor.

**Abrir el puerto 5000 en Windows Server:**
1. Abre el menú Inicio y escribe: "Firewall de Windows Defender con seguridad avanzada".
2. Ve a **Reglas de entrada** (Inbound Rules) -> **Nueva regla**.
3. Selecciona **Puerto** -> Siguiente.
4. Selecciona **TCP** e introduce el número **5000** en puertos locales específicos -> Siguiente.
5. Permitir la conexión. Acepta y finaliza poniéndole el nombre "Generador QR". 
6. Listo. 

## 4. Gestión de Servidor
Para administrar usuarios o ver estadísticas, visita la ruta el Panel de Administración de tu IP:
* `http://[TU_IP]:5000/dashboard`

El usuario administrador por defecto es:
* **Usuario:** `admin`
* **Contraseña:** `admin123`
