document.addEventListener("DOMContentLoaded", () => {
  const estadoSelect = document.getElementById("estadoVinculacion");

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

  // Modal
  const nuevoModal = document.getElementById('nuevoModal');
  const closeNuevoModal = document.getElementById('closeNuevoModal');
  const cargoIdInput = document.getElementById('cargoIdSeleccionado');

  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.open-nuevo-modal');
    if (btn) {
      e.preventDefault();
      cargoIdInput.value = btn.dataset.cargoId;
      nuevoModal.classList.remove('hidden');
      nuevoModal.classList.add('flex');
    }
  });

  closeNuevoModal.addEventListener('click', () => {
    nuevoModal.classList.add('hidden');
    nuevoModal.classList.remove('flex');
  });

  window.addEventListener('click', (e) => {
    if (e.target === nuevoModal) {
      nuevoModal.classList.add('hidden');
      nuevoModal.classList.remove('flex');
    }
  });

  // 🚀 Enviar formulario
const formAsignarFuncionario = document.getElementById("formAsignarFuncionario");

formAsignarFuncionario.addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();

  formData.append("num_doc", document.getElementById("usuarioNumDoc").value);
  formData.append("cargo", document.getElementById("cargoIdSeleccionado").value);
  formData.append("estadoVinculacion", document.getElementById("estadoVinculacion").value);
  formData.append("salario", document.getElementById("salario").value);
  formData.append("grado", document.getElementById("grado").value);
  formData.append("resolucion", document.getElementById("resolucion").value);
  formData.append("observacion", document.getElementById("observacionCU").value);
  formData.append("fechaInicio", document.getElementById("fechaInicio").value);

  // 👇 archivo solo si el usuario seleccionó uno
  const fileInput = document.getElementById("resolucionArchivo");
  if (fileInput.files.length > 0) {
    formData.append("resolucion_archivo", fileInput.files[0]);
  }

  try {
    const response = await fetch("http://127.0.0.1:8001/api/cargos/cargo-usuarios/", {
      method: "POST",
      body: formData, 
    });

    if (response.ok) {
      const data = await response.json();
      alert("Funcionario asignado con éxito");
    } else {
      const text = await response.text();
      console.error("❌ Error al asignar funcionario:", text);
      alert("Error al asignar funcionario. Mira consola.");
    }
  } catch (error) {
    console.error("⚠️ Error de red:", error);
  }
});

});
