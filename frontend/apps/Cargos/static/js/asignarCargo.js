document.addEventListener("DOMContentLoaded", () => {
// 🚀 Cargar estados de vinculación en el select
const estadoSelect = document.getElementById("estadoVinculacion");

async function cargarEstados() {
  try {
    const response = await fetch("http://127.0.0.1:8001/api/cargos/estado-vinculacion/");
    if (response.ok) {
      const estados = await response.json();

      // limpiar el select
      estadoSelect.innerHTML = '<option value="">-- Selecciona --</option>';

      estados.forEach(estado => {
        const option = document.createElement("option");
        option.value = estado.id;          // id de la BD
        option.textContent = estado.estado; // nombre del estado
        estadoSelect.appendChild(option);
      });
    } else {
      console.error("❌ Error al cargar estados:", response.status);
    }
  } catch (error) {
    console.error("⚠️ Error de red:", error);
  }
}
// Llamar apenas cargue la página
cargarEstados();

//PARA MODAL ASIGNAR FUNCIONARIO
  const nuevoModal = document.getElementById('nuevoModal');
  const closeNuevoModal = document.getElementById('closeNuevoModal');
  const cargoIdInput = document.getElementById('cargoIdSeleccionado');

  // Abrir modal dinámicamente
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.open-nuevo-modal');
    if (btn) {
      e.preventDefault();
      const cargoId = btn.dataset.cargoId;

      // Guardar cargo en el input hidden
      cargoIdInput.value = cargoId;

      // Mostrar modal
      nuevoModal.classList.remove('hidden');
      nuevoModal.classList.add('flex');
    }
  });

  // Cerrar modal con la X
  closeNuevoModal.addEventListener('click', () => {
    nuevoModal.classList.add('hidden');
    nuevoModal.classList.remove('flex');
  });

  // Cerrar si se hace clic fuera del contenido
  window.addEventListener('click', (e) => {
    if (e.target === nuevoModal) {
      nuevoModal.classList.add('hidden');
      nuevoModal.classList.remove('flex');
    }
  });
//FIN DE MODAL ASIGNAR FUNCIONARIO



// 🚀 Enviar formulario de asignación de funcionario
const formAsignarFuncionario = document.getElementById("formAsignarFuncionario");

formAsignarFuncionario.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData(formAsignarFuncionario);

  try {
    const response = await fetch("http://127.0.0.1:8001/api/cargos/cargo-usuarios/", {
      method: "POST",
      body: formData
    });

    if (response.ok) {
      const data = await response.json();
      console.log("✅ Funcionario asignado:", data);

      // Cerrar modal
      nuevoModal.classList.add("hidden");
      nuevoModal.classList.remove("flex");

      // Opcional: refrescar tabla o recargar página
      location.reload();
    } else {
      const errorData = await response.json();
      console.error("❌ Error al asignar funcionario:", errorData);
      alert("Error al asignar funcionario. Revisa la consola.");
    }
  } catch (error) {
    console.error("⚠️ Error de red:", error);
  }
});


});

