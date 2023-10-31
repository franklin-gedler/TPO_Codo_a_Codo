// Inicio de la función para controlar el comportamiento del footer
document.addEventListener("DOMContentLoaded", function () {
    
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
});
// Fin de la función para controlar el comportamiento del footer

// Inicio para enviar email en Contactanos
document.addEventListener("DOMContentLoaded", function () {
    const currentPage = window.location.pathname.split("/").pop();

    if (['contactanos'].includes(currentPage)) {
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
    }
});
// Fin para enviar email en Contactanos

// Inicio generacion content all pages
document.addEventListener("DOMContentLoaded", function () {
    // Obtener el nombre de la página actual sin la extensión
    //console.log(window.location.pathname.split("/").pop());
    const currentPage = window.location.pathname.split("/").pop();

    if (['inicio', 'peliculas', 'series'].includes(currentPage)) {
        
        // Función para crear elementos de video
        function createVideoElement(data, isMovie) {
            const container = document.createElement("div");
            container.className = isMovie ? "pelicula" : "serie";

            const playIconContainer = document.createElement("div");
            playIconContainer.className = "play-icon-container";
            playIconContainer.setAttribute("data-video", data.video);

            const playIcon = document.createElement("i");
            playIcon.className = "fas fa-play play-icon";

            playIconContainer.appendChild(playIcon);

            const img = document.createElement("img");
            //img.src = `{{ url_for('static', filename='image/${data.img}') }}`;
            img.src = data.img;
            img.alt = data.alt;
            img.className = isMovie ? "pelicula-img" : "serie-img";

            const tooltip = document.createElement("div");
            tooltip.className = "image-tooltip";
            const tooltipText = document.createElement("p");
            //tooltipText.textContent = "Texto de la burbuja o miniventana flotante.";
            tooltipText.textContent = data.details;

            tooltip.appendChild(tooltipText);

            container.appendChild(playIconContainer);
            container.appendChild(img);
            container.appendChild(tooltip);

            return container;
        }

        fetch('/movies_series_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ currentPage: currentPage })
        })
        .then(response => response.json())
        .then(data => {
            if (currentPage === 'inicio') {

                const moviesContainer = document.getElementById('movies-container');
                const seriesContainer = document.getElementById('series-container');

                data.moviesData.forEach((movieData) => {
                    const movieElement = createVideoElement(movieData, true);
                    moviesContainer.appendChild(movieElement);
                });

                data.seriesData.forEach((seriesData) => {
                    const seriesElement = createVideoElement(seriesData, false);
                    seriesContainer.appendChild(seriesElement);
                });

                document.body.appendChild(createVideoPopup());

            } else if (currentPage === 'peliculas') {

                const moviesContainer = document.getElementById('movies-container');

                data.moviesData.forEach((movieData) => {
                    const movieElement = createVideoElement(movieData, true);
                    moviesContainer.appendChild(movieElement);
                });

                document.body.appendChild(createVideoPopup());

            } else if (currentPage === 'series') {

                const seriesContainer = document.getElementById('series-container');

                data.seriesData.forEach((seriesData) => {
                    const seriesElement = createVideoElement(seriesData, false);
                    seriesContainer.appendChild(seriesElement);
                });

                document.body.appendChild(createVideoPopup());
            }
            gen_tooltip();
            Video_Popup();
        })
        .catch(error => console.error('Error:', error));
    }
});
// FIN generacion content all pages

function Video_Popup() {
    const playButtons = document.querySelectorAll(".play-icon-container");
    const videoPopup = document.getElementById("video-popup");
    const videoIframe = document.getElementById("video-iframe");
    const closeButton = document.getElementById("close-button");
    
    playButtons.forEach((button) => {
        button.addEventListener("click", function () {
            const videoId = button.getAttribute("data-video");
            //console.log("Video ID:", videoId); // Agregar esto
            const videoSrc = `https://www.youtube.com/embed/${videoId}`;
            //console.log("Video Source:", videoSrc); // Agregar esto
            videoIframe.src = videoSrc;
            videoPopup.style.display = "flex";
        });
    });

    closeButton.addEventListener("click", function () {
        videoIframe.src = "";
        videoPopup.style.display = "none";
    });
}

// Función para crear el bloque de video-popup
function createVideoPopup() {
    const videoPopup = document.createElement("div");
    videoPopup.id = "video-popup";
    videoPopup.className = "video-popup";

    const videoContainer = document.createElement("div");
    videoContainer.className = "video-container";

    const iframe = document.createElement("iframe");
    iframe.id = "video-iframe";
    iframe.width = "560";
    iframe.height = "315";
    iframe.src = ""; // Establece la fuente del iframe según tus necesidades
    iframe.title = "YouTube video player";
    iframe.frameBorder = "0";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
    iframe.allowFullscreen = true;

    videoContainer.appendChild(iframe);

    const closeButton = document.createElement("div");
    closeButton.id = "close-button";
    closeButton.className = "close-button";

    const closeIcon = document.createElement("i");
    closeIcon.className = "fas fa-times";

    closeButton.appendChild(closeIcon);

    videoPopup.appendChild(videoContainer);
    videoPopup.appendChild(closeButton);

    return videoPopup;
}

function gen_tooltip() {
    const images = document.querySelectorAll(".pelicula-img, .serie-img");

    images.forEach((img) => {
        img.addEventListener("mouseover", function (event) {
            const x = event.clientX;
            const y = event.clientY;

            const tooltip = img.nextElementSibling;

            tooltip.style.left = x + "px";
            tooltip.style.top = y + "px";

            tooltip.style.display = "block";
        });

        img.addEventListener("mouseout", function () {
            const tooltip = img.nextElementSibling;
            tooltip.style.display = "none";
        });
    });
}

