document.addEventListener("DOMContentLoaded", () => {
  console.log("JS cargado ✅");

  // --- LOGIN ---
  const form = document.querySelector(".login-form");

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      console.log("Evento submit detectado ✅");

      const usuario = document.getElementById("usuario").value.trim();
      const password = document.getElementById("password").value.trim();

      if (!usuario || !password) {
        alert("⚠️ Debes ingresar usuario y contraseña");
        return;
      }

      try {
        const response = await fetch("http://http://127.0.0.1:8000/api/usuarios/login/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username: usuario, password }),
        });

        if (response.ok) {
          const data = await response.json();
          alert("✅ Login exitoso");
          console.log("Tokens:", data);
          localStorage.setItem("access", data.access);
          localStorage.setItem("refresh", data.refresh);
          window.location.href = "/principal/";
        } else {
          const error = await response.json();
          alert("❌ Error: " + (error.detail || "Credenciales inválidas"));
        }
      } catch (err) {
        alert("⚠️ Error de conexión con el servidor");
        console.error(err);
      }
    });
  } else {
    console.error("⚠️ No se encontró el formulario .login-form");
  }

  // --- MODAL ---
  const modal = document.getElementById("modalRecuperar");
  const openModalBtn = document.getElementById("openModal");
  const closeModalBtn = document.getElementById("closeModal");

  if (openModalBtn && modal) {
    openModalBtn.addEventListener("click", (e) => {
      e.preventDefault();
      modal.style.display = "flex";
    });
  }

  if (closeModalBtn && modal) {
    closeModalBtn.addEventListener("click", () => {
      modal.style.display = "none";
    });
  }

  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
});
