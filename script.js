    document.addEventListener("DOMContentLoaded", function () {
    const slider = document.getElementById("slider");

    slider.addEventListener("click", function () {
        this.classList.add("active");
        setTimeout(() => {
            window.location.href = "main.html"; 
        }, 300); 
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".container_Main img").forEach(boton => {
        boton.addEventListener("click", function () {
            const destino = this.getAttribute("data-url"); 
            if (destino) {
                window.location.href = destino;
            }
        });
    });
});