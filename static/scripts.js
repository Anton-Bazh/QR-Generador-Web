document.getElementById("crear-qr-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch("/crear_qr", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            texto: formData.get("texto"),
            tipo: parseInt(formData.get("tipo")),
            nombre: formData.get("nombre") || "qr_default",
        }),
    });

    // Ahora esperamos una respuesta JSON
    if (response.ok) {
        const result = await response.json();  
        if (result.success) {
            // Mostrar el QR generado
            const imgElement = document.createElement("img");
            imgElement.src = result.image_base64;  // Usamos la propiedad base64
            imgElement.alt = "QR Code generado";
            
            const link = document.createElement('a');
            link.href = result.image_base64;  // Enlace con la imagen en base64
            link.download = result.filename;  // Nombre del archivo para la descarga
            link.textContent = 'Descargar el QR generado';
            link.classList.add('download-btn');  // Añadimos la clase para el estilo del botón

            // Insertamos la imagen y el enlace de descarga en el contenedor
            document.getElementById("qr-result").innerHTML = '';
            document.getElementById("qr-result").appendChild(imgElement);
            document.getElementById("qr-result").appendChild(link);
        } else {
            console.error("Error en la generación del QR:", result.error);
        }
    } else {
        console.error('Error al generar el QR:', response.statusText);
    }
});

document.getElementById("leer-qr-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const response = await fetch("/leer_qr", {
        method: "POST",
        body: formData,
    });
    const result = await response.json();
    if (result.content) {
        document.getElementById("qr-content").innerText = `Contenido del QR: ${result.content}`;
    }
});
