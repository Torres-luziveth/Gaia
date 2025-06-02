
function toggleSlider() {
    let sliderBtn = document.getElementById("sliderBtn");
    sliderBtn.classList.toggle("active");

    if (sliderBtn.classList.contains("active")) {
        setTimeout(() => {
            document.querySelector(".singUp-form").submit();
        }, 300);
    }
}

function mostrar() {
    
    const input = document.getElementById("password");
    input.type = input.type === "password" ? "text" : "password";
}

document.addEventListener('DOMContentLoaded', () => {

  
  const planeta = document.querySelector('.section-banner');
let isDragging = false;
let startX, startY;
let backgroundPosX = 0;
let backgroundPosY = 0;
let velocityX = 0;
let velocityY = 0;
let autoRotateSpeedX = 0.5; 
let autoRotateSpeedY = 0;   
let animationFrame;


// Detiene la rotación automática
function stopAutoRotate() {
  cancelAnimationFrame(animationFrame);
}

// Rotación automática 
function rotateAutomatically() {
  backgroundPosX += autoRotateSpeedX;
  backgroundPosY += autoRotateSpeedY;
  planeta.style.backgroundPosition = `${backgroundPosX}px ${backgroundPosY}px`;
  animationFrame = requestAnimationFrame(rotateAutomatically);
}

// Cambia el cursor al entrar y salir 
planeta.addEventListener('mouseenter', () => {
  if (!isDragging) {
    planeta.style.cursor = 'grab';
  }
});

planeta.addEventListener('mouseleave', () => {
  if (!isDragging) {
    planeta.style.cursor = 'default';
  }
});

// Al presionar el mause
planeta.addEventListener('mousedown', (e) => {
  isDragging = true;
  startX = e.clientX;
  startY = e.clientY;
  planeta.style.cursor = 'grabbing';
  stopAutoRotate(); 
});

// Al mover el mouse
document.addEventListener('mousemove', (e) => {
  if (!isDragging) return;

  const deltaX = e.clientX - startX;
  const deltaY = e.clientY - startY;
  startX = e.clientX;
  startY = e.clientY;

  backgroundPosX += deltaX;
  backgroundPosY += deltaY;

  velocityX = deltaX; // Velocidad X
  velocityY = deltaY; // Velocidad Y

  planeta.style.backgroundPosition = `${backgroundPosX}px ${backgroundPosY}px`;
});

// Al soltar el mouse
document.addEventListener('mouseup', () => {
  if (isDragging) {
    isDragging = false;
    planeta.style.cursor = 'grab';
    animateInertia();
  }
});

// Inercia
function animateInertia() {
  velocityX *= 0.95;
  velocityY *= 0.95;

  backgroundPosX += velocityX;
  backgroundPosY += velocityY;

  planeta.style.backgroundPosition = `${backgroundPosX}px ${backgroundPosY}px`;

  if (Math.abs(velocityX) > 0.1 || Math.abs(velocityY) > 0.1) {
    requestAnimationFrame(animateInertia);
  } else {
    velocityX = 0;
    velocityY = 0;
    rotateAutomatically();
  }
}

rotateAutomatically();


});


