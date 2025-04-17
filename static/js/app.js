
function toggleSlider() {
    let sliderBtn = document.getElementById("sliderBtn");
    sliderBtn.classList.toggle("active");

    if (sliderBtn.classList.contains("active")) {
        setTimeout(() => {
            document.querySelector(".singUp-form").submit();
        }, 300);
    }
}

