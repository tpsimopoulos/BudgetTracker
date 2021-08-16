const showNavbar = () => {
    const navbarMobileMenuButton = document.querySelector('.mobile-menu-button')
    const navbar = document.querySelector('.navbar')
    const navbarLinks = document.querySelectorAll('.navbar__links *')

    navbarMobileMenuButton.addEventListener('click', () => {
        navbar.classList.toggle('navbar-active')
        navbarMobileMenuButton.classList.toggle("toggle")
        
        navbarLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + .5}s`;
            }
        });

    });
}

showNavbar();