
let mobileMenu = document.querySelector(".mobile-menu") // actual menu displayed
let ham = document.querySelector(".ham") // the button to be clicked
let menuIcon = document.querySelector(".menuIcon")
let closeIcon = document.querySelector(".closeIcon")

function toggleMenu() {
    
    if (mobileMenu.classList.contains("show-menu")) {
        mobileMenu.classList.remove("show-menu")
        closeIcon.style.display = "none"
        menuIcon.style.display = "block"
    } else {
        mobileMenu.classList.add("show-menu")
        closeIcon.style.display = "block"
        menuIcon.style.display = "none"

    }
}

ham.addEventListener("click", toggleMenu)

