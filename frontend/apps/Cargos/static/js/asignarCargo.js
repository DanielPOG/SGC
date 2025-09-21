document.addEventListener("DOMContentLoaded", () => {
  const estadoSelect = document.getElementById("estadoVinculacion");
  const nuevoModal = document.getElementById("nuevoModal");
  const closeNuevoModal = document.getElementById("closeNuevoModal");
  const cargoIdInput = document.getElementById("cargoIdSeleccionado");
  const formAsignarFuncionario = document.getElementById("formAsignarFuncionario");

  const escalonModal = document.getElementById("escalonModal");
  const closeEscalonModal = document.getElementById("closeEscalonModal");
  const escalonTexto = document.getElementById("escalonTexto");
  const selectorCargos = document.getElementById("selectorCargos");
  const selectCargos = document.getElementById("selectCargos");
  const btnConfirmAsignar = document.getElementById("btnConfirmAsignar");

  const temporalModal = document.getElementById("temporalModal");
  const closeTemporalModal = document.getElementById("closeTemporalModal");
  const formTemporalAsignacion = document.getElementById("formTemporalAsignacion");
  const cancelTemporalModal = document.getElementById("cancelTemporalModal");


// Cerrar modal temporal
cancelTemporalModal.addEventListener("click", () => {
  temporalModal.classList.add("hidden");
  temporalModal.classList.remove("flex");
});


  let sugerenciasGlobal = [];
  let decisiones = [];
  let indiceActual = 0;
  let rootUsuarioId = null;
  let payloadRootBase = {};
  let archivoRoot = null;

  function agregarDecision(decision) {
    decisiones = decisiones.filter(d => d.usuario_id !== decision.usuario_id);
    decisiones.push(decision);
  }

 async function cargarEstados() {
  try {
    const res = await fetch("http://127.0.0.1:8001/api/cargos/estado-vinculacion/");
    if (!res.ok) throw new Error("Error cargando estados");

    const estados = await res.json();

    // Selecciona el <select> correcto
    const estadoSelect = document.getElementById("estadoVinculacion");
    const temporalEstado = document.getElementById("temporalEstado");

    // Limpia los options
    estadoSelect.innerHTML = '<option value="">-- Selecciona --</option>';
    if (temporalEstado) {
      temporalEstado.innerHTML = '<option value="">-- Selecciona --</option>';
    }


    // Agrega los estados
    estados.forEach(estado => {
      estadoSelect.innerHTML += `<option value="${estado.id}">${estado.estado}</option>`;
      if (temporalEstado) {
        temporalEstado.innerHTML += `<option value="${estado.id}">${estado.estado}</option>`;
      }
    });
  } catch (err) {
    console.error(err);
    alert("⚠️ Error cargando estados");
  }
}

// Ejecuta la carga
cargarEstados();




  
  // Abrir modal principal
  document.addEventListener("click", e => {
    const btn = e.target.closest(".open-nuevo-modal");
    if (!btn) return;
    e.preventDefault();
    cargoIdInput.value = btn.dataset.cargoId;
    nuevoModal.classList.remove("hidden");
    nuevoModal.classList.add("flex");
  });

  closeNuevoModal.addEventListener("click", () => {
    nuevoModal.classList.add("hidden");
    nuevoModal.classList.remove("flex");
  });

  window.addEventListener("click", e => {
    if (e.target === nuevoModal) {
      nuevoModal.classList.add("hidden");
      nuevoModal.classList.remove("flex");
    }
  });

  function validarFormulario(campos) {
    for (let campo of campos) {
      const el = document.getElementById(campo.id);
      if (!el.value || el.value.trim() === "") {
        alert(`❌ El campo "${campo.nombre}" es obligatorio`);
        el.focus();
        return false;
      }
    }
    return true;
  }

  // === POST Escalonado Inicial ===
  formAsignarFuncionario.addEventListener("submit", async e => {
    e.preventDefault();
    const camposRoot = [
      { id: "usuarioId", nombre: "Número de documento" },
      { id: "grado", nombre: "Grado" },
      { id: "salario", nombre: "Salario" },
      { id: "resolucion", nombre: "Resolución" },
      { id: "resolucionArchivo", nombre: "Archivo Resolución" },
      { id: "estadoVinculacion", nombre: "Estado de vinculación" },
      { id: "fechaInicio", nombre: "Fecha de inicio" }
    ];
    if (!validarFormulario(camposRoot)) return;

    const cargoDestinoId = parseInt(cargoIdInput.value);

    payloadRootBase = {
      cargo_id: cargoDestinoId,
      cargo_destino_id: cargoDestinoId,
      num_doc: document.getElementById("usuarioId").value,
      estadoVinculacion: parseInt(document.getElementById("estadoVinculacion").value),
      salario: document.getElementById("salario").value,
      grado: document.getElementById("grado").value,
      resolucion: document.getElementById("resolucion").value,
      observacion: document.getElementById("observacionCU").value || "",
      fechaInicio: document.getElementById("fechaInicio").value
    };

    archivoRoot = document.getElementById("resolucionArchivo").files[0];
    if (!archivoRoot) {
      alert("❌ Debes adjuntar el archivo de resolución");
      return;
    }

    try {
      const formData = new FormData();
      Object.entries(payloadRootBase).forEach(([key, value]) => {
        formData.append(key, value);
      });
      formData.append("resolucion_archivo", archivoRoot);

      const res = await fetch("http://127.0.0.1:8001/api/cargos/cargo-usuarios/?modo=escalonado", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      if (!res.ok) {
        console.error("Errores de validación:", data);
        alert("❌ Verifica los campos obligatorios");
        return;
      }

      if (data.sugerencias && data.sugerencias.length) {
        rootUsuarioId = data.cargo_usuario.usuario;
        sugerenciasGlobal = data.sugerencias;
        decisiones = [];
        indiceActual = 0;
        mostrarSiguienteSugerencia();
      } else {
        alert("✅ Funcionario asignado correctamente");
        nuevoModal.classList.add("hidden");
        nuevoModal.classList.remove("flex");
        if (typeof buscarPorIdp === "function") buscarPorIdp();
      }
    } catch (err) {
      console.error(err);
      alert("⚠️ Error de red al asignar funcionario");
    }
  });

  // === Manejo de sugerencias ===
  function mostrarSiguienteSugerencia() {
    if (indiceActual >= sugerenciasGlobal.length) {
      enviarConfirmacion();
      return;
    }

    const sug = sugerenciasGlobal[indiceActual];
    escalonTexto.textContent = `¿Qué hacer con ${sug.usuario_nombre}?`;
    selectorCargos.classList.add("hidden");
    selectCargos.innerHTML = "";

    // Planta → usa datos históricos, sin archivo
    document.getElementById("btnDevolverPlanta").onclick = () => {
      agregarDecision({
        usuario_id: sug.usuario_id,
        cargo_id: sug.opciones.find(o => o.tipo === "planta").cargo_id,
        tipo: "planta",
        num_doc: sug.num_doc,
        estadoVinculacion: sug.estadoVinculacion,
        salario: sug.salario,
        grado: sug.grado,
        resolucion: sug.resolucion,
        resolucion_archivo: sug.resolucion_archivo,
        fechaInicio: sug.fechaInicio,
        observacion: sug.observacion || ""
      });
      indiceActual++;
      mostrarSiguienteSugerencia();
    };

    // Mostrar selector de cargos temporales
    document.getElementById("btnAsignarOtro").onclick = () => {
      const temporales = sug.opciones.filter(o => o.tipo === "temporal");
      selectCargos.innerHTML = "";
      temporales.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt.cargo_id;
        option.textContent = `${opt.cargo_id} - ${opt.cargo_nombre || "Sin nombre"}`;
        selectCargos.appendChild(option);
      });
    };

    // Abrir modal temporal para capturar datos
    btnConfirmAsignar.onclick = () => {
      const cargoIdSel = parseInt(selectCargos.value);
      document.getElementById("temporalCargoId").value = cargoIdSel;
      document.getElementById("temporalUsuarioId").value = sug.usuario_id;
      temporalModal.classList.remove("hidden");
      temporalModal.classList.add("flex");
    };

    escalonModal.classList.remove("hidden");
    escalonModal.classList.add("flex");
  }

  closeEscalonModal.addEventListener("click", () => {
    escalonModal.classList.add("hidden");
    escalonModal.classList.remove("flex");
  });

  // === Formulario Temporal ===
  formTemporalAsignacion.addEventListener("submit", e => {
    e.preventDefault();
    const cargoIdSel = parseInt(document.getElementById("temporalCargoId").value);
    const usuarioId = parseInt(document.getElementById("temporalUsuarioId").value);

    const archivoTemp = document.getElementById("temporalArchivo").files[0];
    if (!archivoTemp) {
      alert("❌ Debes adjuntar el archivo de resolución del temporal");
      return;
    }

    agregarDecision({
      usuario_id: usuarioId,
      cargo_id: cargoIdSel,
      tipo: "temporal",
      grado: document.getElementById("temporalGrado").value,
      salario: document.getElementById("temporalSalario").value,
      resolucion: document.getElementById("temporalResolucion").value,
      resolucion_archivo: archivoTemp,
      estadoVinculacion: parseInt(document.getElementById("temporalEstado").value),
      fechaInicio: document.getElementById("temporalFechaInicio").value,
      observacion: document.getElementById("temporalObservacion").value || ""
    });

    temporalModal.classList.add("hidden");
    temporalModal.classList.remove("flex");

    indiceActual++;
    mostrarSiguienteSugerencia();
  });

  closeTemporalModal.addEventListener("click", () => {
    temporalModal.classList.add("hidden");
    temporalModal.classList.remove("flex");
  });

  // === POST Confirmación Final ===
  async function enviarConfirmacion() {
    if (!cargoIdInput.value) {
      alert("Error interno: no se detectó el cargo destino");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("root_usuario_id", rootUsuarioId);
      formData.append("cargo_destino_id", parseInt(cargoIdInput.value));
      formData.append("payload_root", JSON.stringify(payloadRootBase));

      if (archivoRoot) {
        formData.append("resolucion_archivo", archivoRoot);
      }
      decisiones.forEach((d, i) => {
        const { resolucion_archivo, ...rest } = d;
        formData.append(`decisiones[${i}]`, JSON.stringify(rest));
        if (resolucion_archivo instanceof File) {
          formData.append(`decisiones_archivo_${i}`, resolucion_archivo);
        }
      });

      const res = await fetch("http://127.0.0.1:8001/api/cargos/cargo-usuarios/confirmacion/", {
        method: "POST",
        body: formData
      });

      const data = await res.json().catch(() => ({}));
      if (!res.ok) {
        console.error("Error en confirmación:", data);
        alert("❌ Error al aplicar decisiones: revisa campos obligatorios");
        return;
      }

      alert("✅ Decisiones aplicadas correctamente");
      escalonModal.classList.add("hidden");
      escalonModal.classList.remove("flex");
      nuevoModal.classList.add("hidden");
      nuevoModal.classList.remove("flex");

      if (typeof buscarPorIdp === "function") buscarPorIdp();

    } catch (err) {
      console.error(err);
      alert("⚠️ Error de red al confirmar");
    }
  }
});
