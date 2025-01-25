from flask import Flask, render_template, request, jsonify
import os
import qrcode
from io import BytesIO
import base64
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    CircleModuleDrawer,
    GappedSquareModuleDrawer,
    HorizontalBarsDrawer,
    RoundedModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/crear_qr", methods=["POST"])
def crear_qr():
    try:
        data = request.json
        texto = data.get("texto")
        tipo = data.get("tipo", 6)  # Tipo predeterminado 6
        nombre = data.get("nombre", "qr_default")
        
        if not texto:
            return jsonify({"error": "No se proporcionó texto para el QR"}), 400
        
        # Crear el objeto QRCode
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(texto)

        # Seleccionar el estilo del QR según la opción del usuario
        tipoQRC = {
            1: CircleModuleDrawer(),
            2: GappedSquareModuleDrawer(),
            3: VerticalBarsDrawer(),
            4: HorizontalBarsDrawer(),
            5: RoundedModuleDrawer(),
            6: SquareModuleDrawer(),
        }.get(tipo, SquareModuleDrawer())

        # Generar la imagen del QR
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=tipoQRC)

        # Convertir la imagen a base64
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        # Devolver la imagen en base64 para que el navegador la descargue
        return jsonify({
            "success": True,
            "image_base64": f"data:image/png;base64,{img_base64}",
            "filename": f"{nombre}.png"
        })
    
    except Exception as e:
        # Capturar cualquier error y devolver un mensaje adecuado
        return jsonify({"error": f"Error al generar el QR: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
