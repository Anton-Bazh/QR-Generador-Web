    // Manejo del formulario para crear el QR
    document.getElementById('crear-qr-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(this);
        const texto = formData.get('texto');
        const tipo = formData.get('tipo');
        const nombre = formData.get('nombre') || 'qr_default';

        fetch('/crear_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                texto: texto,
                tipo: parseInt(tipo),
                nombre: nombre
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Crear una imagen en base64 a partir de la respuesta
                const imgElement = document.createElement('img');
                imgElement.src = data.image_base64;  // Usamos la propiedad image_base64
                imgElement.alt = 'Código QR generado';

                const link = document.createElement('a');
                link.href = data.image_base64;  // Enlace con la imagen en base64
                link.download = nombre + '.png';  // Nombre del archivo para la descarga
                link.textContent = 'Descargar el QR generado';
                link.classList.add('download-btn');  // Añadimos la clase para el estilo del botón

                // Insertamos la imagen y el enlace de descarga en el contenedor
                document.getElementById('qr-result').innerHTML = '';
                document.getElementById('qr-result').appendChild(imgElement);
                document.getElementById('qr-result').appendChild(link);

                // Mostrar el modal de donación después de la descarga
                link.addEventListener('click', function() {
                    // Mostrar el modal
                    document.getElementById('donation-modal').style.display = 'flex';
                });
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => alert('Error al generar el QR: ' + error));
    });

    // Cerrar el modal cuando el usuario haga clic en el botón de cierre
    document.querySelector('.close-btn').addEventListener('click', function() {
        document.getElementById('donation-modal').style.display = 'none';
    });

    // Cerrar el modal si el usuario hace clic fuera del contenido del modal
    window.addEventListener('click', function(event) {
        if (event.target === document.getElementById('donation-modal')) {
            document.getElementById('donation-modal').style.display = 'none';
        }
    });

    // Mostrar imagen de ejemplo del QR seleccionado
    document.getElementById('tipo').addEventListener('change', function() {
        const tipo = this.value;
        const exampleImg = document.getElementById('example-img');
        switch(tipo) {
            case '1':
                exampleImg.src = '/static/image/Circulo.png';
                break;
            case '2':
                exampleImg.src = '/static/image/Cuadrado.png';
                break;
            case '3':
                exampleImg.src = '/static/image/Barra Vertical.png';
                break;
            case '4':
                exampleImg.src = '/static/image/Barra Horizontal.png';
                break;
            case '5':
                exampleImg.src = '/static/image/Redondeado.png';
                break;
            case '6':
                exampleImg.src = '/static/image/Cuadrado clasico.png';
                break;
            default:
                exampleImg.src = '';
        }
    });