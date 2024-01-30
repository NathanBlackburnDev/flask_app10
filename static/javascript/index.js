// Highlight the current page the user is on in the Navbar
// Wait for entire document object model to be loaded
addEventListener("DOMContentLoaded", () => {
    // Iterate through each 'nav-link' class
    document.querySelectorAll('.nav-link').forEach(
        link => {
            if (link.href === window.location.href) {
                link.setAttribute('aria-current', 'page');
                link.classList.add('active');
            }
        }
    )
})