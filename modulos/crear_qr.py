import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    CircleModuleDrawer,
    GappedSquareModuleDrawer,
    HorizontalBarsDrawer,
    RoundedModuleDrawer,
    SquareModuleDrawer,
    VerticalBarsDrawer,
)
from io import BytesIO

def crear_qr(valorQR, opc_usuario, imagenQR=None):
    try:
        # Crear el objeto QRCode con tamaño dinámico
        qr = qrcode.QRCode(
            version=None,  # Ajusta el tamaño automáticamente según los datos
            error_correction=qrcode.constants.ERROR_CORRECT_Q,  # Mejor corrección de errores
            box_size=10,
            border=4,
        )
        qr.add_data(valorQR)
        qr.make(fit=True)  # Ajusta el QR al contenido

        # Seleccionar el estilo del QR según la opción del usuario
        tipoQRC = {
            1: CircleModuleDrawer(),
            2: GappedSquareModuleDrawer(),
            3: VerticalBarsDrawer(),
            4: HorizontalBarsDrawer(),
            5: RoundedModuleDrawer(),
            6: SquareModuleDrawer(),
        }.get(opc_usuario, SquareModuleDrawer())

        # Generar la imagen del QR
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=tipoQRC)

        # Guardar el QR si se proporciona un nombre de archivo
        if imagenQR:
            img.save(imagenQR)
            print(f"QR guardado en: {imagenQR}")
        
        # Devolver la imagen en memoria
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return img_io  # Devuelve la imagen en memoria como BytesIO
    except Exception as e:
        print(f"Error al generar el QR: {e}")
        raise  # Relanzar el error para manejo externo

def codigo_personalizado(valorQR, opc_usuario, nombreQR=None):
    return crear_qr(valorQR, opc_usuario, nombreQR)
