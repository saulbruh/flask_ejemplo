document.addEventListener("DOMContentLoaded", function() {
    const logoutLink = document.getElementById("logout-link");

    if (logoutLink) {
        logoutLink.addEventListener("click", function(event) {
            const confirmLogout = confirm("¿Estás seguro de que deseas cerrar sesión?");
            if (!confirmLogout) {
                event.preventDefault(); // Evita que el usuario cierre sesión si cancela
            }
        });
    }
});