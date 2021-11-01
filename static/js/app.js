const navSlide = () => {
    const burger = document.querySelector(".burger");
    const nav = document.querySelector(".navbar-mobile");
    const navLinks = document.querySelectorAll("ul.navbar-mobile li");

    
    burger.addEventListener("click", () => {
        //Toggle Navbar
        nav.classList.toggle("nav-active");
        
        //Animate Links
        navLinks.forEach((link, index) => {
        if (link.style.animation) {
            link.style.animation ="";
        } else {
            link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
        }
    });
    });
}
navSlide();
