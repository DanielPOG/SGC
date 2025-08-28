
    // Abrir modal
    document.getElementById('openModal').onclick = function(e) {
      e.preventDefault();
      document.getElementById('modalRecuperar').style.display = 'flex';
    };

    // Cerrar modal con botón
    document.getElementById('closeModal').onclick = function() {
      document.getElementById('modalRecuperar').style.display = 'none';
    };

    // Cerrar modal haciendo clic fuera del contenido
    window.onclick = function(event) {
      var modal = document.getElementById('modalRecuperar');
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }