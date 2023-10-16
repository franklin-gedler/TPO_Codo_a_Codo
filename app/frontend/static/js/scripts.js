// Inicio de la función para controlar el comportamiento del footer
const footer = document.querySelector('footer');

// Variable para rastrear la posición anterior del scroll
let previousScrollPosition = window.pageYOffset || document.documentElement.scrollTop;

// Función para controlar el comportamiento del footer
function handleFooterVisibility() {
    const currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;

    // Verifica si el usuario ha hecho scroll hacia abajo
    if (currentScrollPosition > previousScrollPosition) {
        // Si es así, oculta el footer
        footer.classList.add('hidden-footer');
    } else {
        // Si el usuario está haciendo scroll hacia arriba, muestra el footer
        footer.classList.remove('hidden-footer');
    }

    // Actualiza la posición anterior del scroll
    previousScrollPosition = currentScrollPosition;
}

// Asocia la función al evento scroll
window.addEventListener('scroll', handleFooterVisibility);
// Fin de la función para controlar el comportamiento del footer




// Inicio para enviar email en Contactanos
document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.getElementById("contact-form");
    contactForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const nombre = document.getElementById("nombre").value;
        const email = document.getElementById("email").value;
        const mensaje = document.getElementById("mensaje").value;

        if (!validateEmail(email)) {
            alert("Por favor, ingrese una dirección de correo electrónico válida.");
            return;
        }

        const body = {
            nombre: nombre,
            email: email,
            mensaje: mensaje
        };

        // Enviar la solicitud POST al backend de Flask
        fetch('/sendmail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .then(data => {
            if (data.requestId) {
                // Si la respuesta contiene un requestId, el envío fue exitoso
                alert("Mensaje enviado exitosamente.");
                contactForm.reset();
            } else if (data.message && data.type) {
                // Si la respuesta contiene un mensaje de error y un tipo de error
                alert("Error: " + data.message + " (" + data.type + ")");
            } else {
                // Si la respuesta no se ajusta a ninguno de los casos anteriores
                alert("Respuesta inesperada del servidor: " + JSON.stringify(data));
            }
        })
    });

    function validateEmail(email) {
        const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
        return regex.test(email);
    }
});
// Fin para enviar email en Contactanos

// Inicio para imagenes-videos
document.addEventListener("DOMContentLoaded", function () {
    const playButtons = document.querySelectorAll(".play-button");
    const videoPopup = document.getElementById("video-popup");
    const videoIframe = document.getElementById("video-iframe");
    const closeButton = document.getElementById("close-button");

    playButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const videoId = button.getAttribute("data-video");
            const videoSrc = `https://www.youtube.com/embed/${videoId}`;
            videoIframe.src = videoSrc;
            videoPopup.style.display = "flex";
        });
    });

    closeButton.addEventListener("click", function () {
        videoIframe.src = "";
        videoPopup.style.display = "none";
    });
});
// Fin para imagenes-videos
