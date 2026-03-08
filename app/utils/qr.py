import qrcode
import re
from io import BytesIO
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    CircleModuleDrawer,
    GappedSquareModuleDrawer,
    HorizontalBarsDrawer,
    RoundedModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
)

MAX_TEXT_LENGTH = 2325
ALLOWED_QR_TYPES = {1, 2, 3, 4, 5, 6}
QR_DRAWERS = {
    1: CircleModuleDrawer(),
    2: GappedSquareModuleDrawer(),
    3: VerticalBarsDrawer(),
    4: HorizontalBarsDrawer(),
    5: RoundedModuleDrawer(),
    6: SquareModuleDrawer(),
}

def sanitize_filename(filename):
    """Sanitiza el nombre del archivo para seguridad"""
    if not filename:
        return "qr_default"
    filename = re.sub(r'[^\w\-_.]', '', filename)
    filename = filename[:50]
    return filename or "qr_default"

def validate_qr_input(texto, tipo, nombre):
    """Valida los inputs del usuario"""
    errors = []
    if not texto or not texto.strip():
        errors.append("No se proporcionó texto para el QR")
    if len(texto) > MAX_TEXT_LENGTH:
        errors.append(f"El texto es demasiado largo. Máximo {MAX_TEXT_LENGTH} caracteres")
    if tipo not in ALLOWED_QR_TYPES:
        errors.append(f"Tipo de QR no válido. Debe ser entre 1 y 6")
    return len(errors) == 0, errors

def generate_qr_image(texto, tipo):
    """Función unificada para generar QR"""
    try:
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(texto)
        qr.make(fit=True)
        drawer = QR_DRAWERS.get(tipo, SquareModuleDrawer())        
        img = qr.make_image(
            image_factory=StyledPilImage, 
            module_drawer=drawer,
            fill_color="black",
            back_color="white"
        )
        return img, qr.version
    except Exception as e:
        raise Exception(f"Error generando imagen QR: {str(e)}")
