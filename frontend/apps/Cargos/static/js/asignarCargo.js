document.addEventListener("DOMContentLoaded", () => {
  const estadoSelect = document.getElementById("estadoVinculacion");

  // ------------------------
  // Cargar estados
  // ------------------------
  async function cargarEstados() {
    try {
      const response = await fetch("http://127.0.0.1:8001/api/cargos/estado-vinculacion/");
      if (response.ok) {
        const estados = await response.json();
        estadoSelect.innerHTML = '<option value="">-- Selecciona --</option>';
        estados.forEach(estado => {
          const option = document.createElement("option");
          option.value = estado.id;
          option.textContent = estado.estado;
          estadoSelect.appendChild(option);
        });
      }
    } catch (error) {
      console.error("⚠️ Error de red:", error);
    }
  }
  cargarEstados();

  // ------------------------
  // Modal
  // ------------------------
  const nuevoModal = document.getElementById("nuevoModal");
  const closeNuevoModal = document.getElementById("closeNuevoModal");
  const cargoIdInput = document.getElementById("cargoIdSeleccionado");

  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".open-nuevo-modal");
    if (btn) {
      e.preventDefault();
      cargoIdInput.value = btn.dataset.cargoId;
      nuevoModal.classList.remove("hidden");
      nuevoModal.classList.add("flex");
    }
  });

  closeNuevoModal.addEventListener("click", () => {
    nuevoModal.classList.add("hidden");
    nuevoModal.classList.remove("flex");
  });

  window.addEventListener("click", (e) => {
    if (e.target === nuevoModal) {
      nuevoModal.classList.add("hidden");
      nuevoModal.classList.remove("flex");
    }
  });

  // ------------------------
  // Enviar formulario
  // ------------------------
formAsignarFuncionario.addEventListener("submit", async function (e) {
  e.preventDefault();

  const formData = new FormData(this);
  formData.append("cargo_id", cargoIdInput.value); // asegurar que se incluya el cargo

  try {
    const res = await fetch("http://127.0.0.1:8001/api/cargos/cargo-usuarios/?modo=escalonado", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (!res.ok) {
      console.error("❌ Errores de validación:", data);
      alert("❌ Verifica los campos obligatorios");
      return;
    }

    // 👉 Si hay sugerencias (escalonado)
    if (data.sugerencias && data.sugerencias.length > 0) {
      manejarSugerenciasEscalonadas(data.sugerencias, data.cargo_usuario.usuario_id);
    } else {
      alert("✅ Funcionario asignado correctamente");
      nuevoModal.classList.add("hidden");
      nuevoModal.classList.remove("flex");
      if (typeof buscarPorIdp === "function") buscarPorIdp();
    }

  } catch (err) {
    console.error("⚠️ Error de red:", err);
    alert("❌ Error de red al asignar funcionario");
  }
});



});
