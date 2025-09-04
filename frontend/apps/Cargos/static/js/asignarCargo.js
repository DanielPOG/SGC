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
  const formAsignarFuncionario = document.getElementById("formAsignarFuncionario");

  formAsignarFuncionario.addEventListener("submit", async (e) => {
    e.preventDefault();

    // ------------------------
    // Validaciones básicas
    // ------------------------
    const numDoc = document.getElementById("usuarioNumDoc").value.trim();
    const cargoId = document.getElementById("cargoIdSeleccionado").value;
    const estadoVinculacion = document.getElementById("estadoVinculacion").value;

    if (!numDoc || !cargoId || !estadoVinculacion) {
      alert("⚠️ Debes completar documento, cargo y estado de vinculación");
      return;
    }

    // ------------------------
    // Preguntar el modo
    // ------------------------
    let modo = null;

    const elegirModo = confirm(
      "¿Quieres hacer la reasignación de forma ESCALONADA?\n\nAceptar = Escalonado\nCancelar = Automático"
    );

    if (elegirModo) {
      modo = "escalonado";
    } else {
      modo = "auto";
    }

    // ------------------------
    // Construir FormData
    // ------------------------
    const formData = new FormData();
    formData.append("num_doc", numDoc);
    formData.append("cargo", cargoId);
    formData.append("estadoVinculacion", estadoVinculacion);
    formData.append("salario", document.getElementById("salario").value);
    formData.append("grado", document.getElementById("grado").value);
    formData.append("resolucion", document.getElementById("resolucion").value);
    formData.append("observacion", document.getElementById("observacionCU").value);

    const fileInput = document.getElementById("resolucionArchivo");
    if (fileInput.files.length > 0) {
      formData.append("resolucion_archivo", fileInput.files[0]);
    }

    // ------------------------
    // Llamada al backend
    // ------------------------
    try {
      const response = await fetch(
        `http://127.0.0.1:8001/api/cargos/cargo-usuarios/?modo=${modo}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        const data = await response.json();

        if (modo === "escalonado" && data.sugerencias) {
          let mensaje = "⚠️ Funcionarios que deberían volver a su cargo de planta:\n\n";
          data.sugerencias.forEach((s) => {
            mensaje += `👤 ${s.usuario_nombre} → ${s.cargo_nombre}\n`;
          });
          alert(mensaje);
        } else {
          alert("✅ Funcionario asignado con éxito");
        }

        // Reset form y cerrar modal
        formAsignarFuncionario.reset();
        nuevoModal.classList.add("hidden");
        nuevoModal.classList.remove("flex");
      } else {
        const text = await response.text();
        console.error("❌ Error al asignar funcionario:", text);
        alert("❌ Error al asignar funcionario. Revisa la consola.");
      }
    } catch (error) {
      console.error("⚠️ Error de red:", error);
      alert("⚠️ No se pudo conectar con el servidor");
    }
  });


});
