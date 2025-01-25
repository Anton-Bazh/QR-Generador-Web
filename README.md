# QR-Generador-Web

El proyecto **QR-Generador-Web** es una aplicación web que permite a los usuarios generar códigos QR personalizados de manera rápida y eficiente. Los usuarios pueden elegir entre varios estilos de módulos para el código QR, y la imagen generada no se guarda en el servidor, sino que se maneja en el caché y se envía como una imagen base64 para su descarga.

## Tecnologías Utilizadas

- **Flask**: Framework ligero para la creación de aplicaciones web en Python.
- **qrcode**: Librería de Python para generar códigos QR.
- **HTML/CSS/JS**: Para la estructura, el estilo y la interactividad en el frontend.
- **Heroku** *(opcional)*: Para el despliegue de la aplicación en la nube.

## Instalación

Sigue estos pasos para ejecutar el proyecto localmente:

1. **Clonar el repositorio**
   
   Si aún no has clonado el repositorio, utiliza el siguiente comando:
   ```bash
   git clone https://github.com/Anton-Bazh/QR-Generador-Web.git
   ```

2. **Instalar dependencias**
   
   Asegúrate de tener Python y pip instalados. Luego, instala las dependencias necesarias desde el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación**
   
   Después de instalar las dependencias, puedes iniciar el servidor Flask ejecutando:
   ```bash
   python app.py
   ```
   Esto iniciará la aplicación en `http://127.0.0.1:5000`, donde podrás acceder a la interfaz web y generar códigos QR.

## Detalles Técnicos y Flujo del Proyecto

### Flask como Framework Web

El proyecto utiliza Flask para manejar las rutas y las solicitudes HTTP. Las principales rutas son:

- `/`: Muestra la interfaz de usuario para interactuar con la aplicación.
- `/crear_qr`: Recibe los datos del usuario (como el texto y el estilo del QR), genera el código QR y devuelve la imagen como una cadena base64.

### Generación del Código QR

El proyecto utiliza la librería **qrcode** para crear los códigos QR. Los estilos de los módulos del QR (como círculos, cuadrados, barras) se configuran mediante la librería `qrcode.image.styles.moduledrawers`.

En lugar de guardar la imagen en el servidor, el QR se convierte a base64 y se devuelve al navegador. Esto permite al usuario descargar el código QR sin necesidad de almacenamiento en el servidor.

### Uso de Procfile y runtime.txt

Si decides desplegar el proyecto en Heroku, los siguientes archivos son necesarios:

- **Procfile**: Indica a Heroku cómo ejecutar la aplicación. Contiene la línea:
  ```text
  web: python app.py
  ```

- **runtime.txt**: Define la versión de Python a usar en Heroku. Ejemplo:
  ```text
  python-3.9.6
  ```

## Funcionalidad de la Aplicación

- **Generación de QR**: Los usuarios pueden ingresar texto y elegir entre varios estilos de códigos QR (por ejemplo, círculos, cuadrados, barras horizontales, etc.).
- **Descarga directa**: La imagen generada se devuelve como una cadena base64, lista para ser descargada.
- **Sin almacenamiento en el servidor**: La aplicación maneja las imágenes QR generadas en el caché, enviándolas directamente al cliente.

## Imágenes del Proyecto

Pantallas del proyecto:
- ![Pantalla principal](static/image/pantalla.png)
- ![Pantalla generador](static/image/pantalla2.png)

## Repositorio del Proyecto

Puedes encontrar el código fuente del proyecto en el siguiente enlace:
[https://github.com/Anton-Bazh/QR-Generador-Web](https://github.com/Anton-Bazh/QR-Generador-Web)
