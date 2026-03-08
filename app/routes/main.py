from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
import os
import base64
from io import BytesIO
from app.utils.qr import generate_qr_image, validate_qr_input, sanitize_filename, MAX_TEXT_LENGTH, ALLOWED_QR_TYPES
from app.utils.db import get_db

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/privacidad")
def privacidad():
    return render_template("privacidad.html")

@main_bp.route("/terminos")
def terminos():
    return render_template("terminos.html")

@main_bp.route("/crear_qr", methods=["POST"])
def crear_qr():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type debe ser application/json"}), 400
        data = request.get_json()
        if not data:
            return jsonify({"error": "Cuerpo de la solicitud vacío o inválido"}), 400
        
        texto = data.get("texto", "").strip()
        tipo = data.get("tipo", 6)
        nombre = sanitize_filename(data.get("nombre", "qr_default"))
        color_dark = data.get("color_dark", "#000000")
        color_light = data.get("color_light", "#FFFFFF")
        
        is_valid, errors = validate_qr_input(texto, tipo, nombre)
        if not is_valid:
            return jsonify({"error": "; ".join(errors)}), 400
            
        img, qr_version = generate_qr_image(texto, tipo, color_dark, color_light)        
        
        # Save to database
        try:
            db = get_db(current_app)
            db.execute('INSERT INTO qr_history (texto, tipo, nombre) VALUES (?, ?, ?)',
                       (texto, tipo, nombre))
            db.commit()
            db.close()
        except Exception as db_err:
            print(f"Error al guardar en DB: {db_err}")

        img_io = BytesIO()
        img.save(img_io, 'PNG', optimize=True)
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')        
        
        return jsonify({
            "success": True,
            "image_base64": f"data:image/png;base64,{img_base64}",
            "filename": f"{nombre}.png",
            "qr_size": f"Versión {qr_version}",
            "message": "QR generado exitosamente"
        })
    
    except ValueError as ve:
        return jsonify({"error": f"Error en los datos: {str(ve)}"}), 400
    except Exception as e:
        print(f"Error en crear_qr: {str(e)}")
        return jsonify({"error": "Error interno del servidor al generar el QR"}), 500

@main_bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main_bp.route("/health")
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "qr-generator",
        "version": "2.0.0"
    })

@main_bp.route("/api/info")
def api_info():
    return jsonify({
        "name": "QR Generator Web",
        "version": "2.0.0",
        "max_text_length": MAX_TEXT_LENGTH,
        "allowed_qr_types": list(ALLOWED_QR_TYPES),
        "endpoints": {
            "create_qr": "/crear_qr (POST)",
            "health": "/health (GET)",
            "info": "/api/info (GET)"
        }
    })
