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
      estadoSelect.innerHTML = '<option value="">-- Selecciona --</option>';
      const temporalEstado = document.getElementById("temporalEstado");
      temporalEstado.innerHTML = '<option value="">-- Selecciona --</option>';
      estados.forEach(estado => {
        estadoSelect.innerHTML += `<option value="${estado.id}">${estado.estado}</option>`;
        temporalEstado.innerHTML += `<option value="${estado.id}">${estado.estado}</option>`;
      });
    } catch (err) {
      console.error(err);
      alert("⚠️ Error cargando estados");
    }
  }
  cargarEstados();

  // Abrir modal
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

  formAsignarFuncionario.addEventListener("submit", async e => {
    e.preventDefault();
    const camposRoot = [
      { id: "usuarioId", nombre: "Número de documento" },
      { id: "grado", nombre: "Grado" },
      { id: "salario", nombre: "Salario" },
      { id: "resolucion", nombre: "Resolución" },
      { id: "resolucionArchivo", nombre: "Resolución_Archivo" },
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
      formData.append("payload_root", JSON.stringify(payloadRootBase));
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

  function mostrarSiguienteSugerencia() {
    if (indiceActual >= sugerenciasGlobal.length) {
      enviarConfirmacion();
      return;
    }

    const sug = sugerenciasGlobal[indiceActual];
    escalonTexto.textContent = `¿Qué hacer con ${sug.usuario_nombre}?`;
    selectorCargos.classList.add("hidden");
    selectCargos.innerHTML = "";

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
        fechaInicio: sug.fechaInicio,
        observacion: sug.observacion || "",
        resolucion_archivo: archivoRoot
      });
      indiceActual++;
      mostrarSiguienteSugerencia();
    };

    document.getElementById("btnAsignarOtro").onclick = () => {
      selectorCargos.classList.remove("hidden");
      const temporales = sug.opciones.filter(o => o.tipo === "temporal");
      selectCargos.innerHTML = "";
      temporales.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt.cargo_id;
        option.textContent = `${opt.cargo_id} - ${opt.cargo_nombre || "Sin nombre"}`;
        selectCargos.appendChild(option);
      });
    };

    btnConfirmAsignar.onclick = () => {
      const cargoIdSel = parseInt(selectCargos.value);
      agregarDecision({
        usuario_id: sug.usuario_id,
        cargo_id: cargoIdSel,
        tipo: "temporal",
        num_doc: sug.num_doc,
        estadoVinculacion: parseInt(document.getElementById("temporalEstado").value),
        salario: document.getElementById("temporalSalario").value,
        grado: document.getElementById("temporalGrado").value,
        resolucion: document.getElementById("temporalResolucion").value,
        fechaInicio: document.getElementById("temporalFechaInicio").value,
        observacion: document.getElementById("temporalObservacion").value || "",
        resolucion_archivo: archivoRoot
      });
      indiceActual++;
      mostrarSiguienteSugerencia();
    };

    escalonModal.classList.remove("hidden");
    escalonModal.classList.add("flex");
  }

  closeEscalonModal.addEventListener("click", () => {
    escalonModal.classList.add("hidden");
    escalonModal.classList.remove("flex");
  });

  async function enviarConfirmacion() {
  if (!cargoIdInput.value) {
    alert("Error interno: no se detectó el cargo destino");
    return;
  }

  try {
    const formData = new FormData();

    // Agregar root_usuario y cargo_destino
    formData.append("root_usuario_id", rootUsuarioId);
    formData.append("cargo_destino_id", parseInt(cargoIdInput.value));

    // Construir payload_root con todos los campos + archivo
    const payloadRootForm = payloadRootBase;
    if (archivoRoot) {
      payloadRootForm.resolucion_archivo = archivoRoot;
    }

    // Añadir campos de payload_root individualmente al FormData
    for (const key in payloadRootForm) {
      if (payloadRootForm[key] instanceof File) {
        formData.append(`payload_root[${key}]`, payloadRootForm[key]);
      } else {
        formData.append(`payload_root[${key}]`, payloadRootForm[key]);
      }
    }

    // Añadir decisiones y sus archivos
    decisiones.forEach((d, i) => {
      const { resolucion_archivo, ...rest } = d;
      formData.append(`decisiones[${i}]`, JSON.stringify(rest));
      if (resolucion_archivo instanceof File) {
        formData.append(`decisiones_archivo_${i}`, resolucion_archivo);
      }
    });

    // Enviar POST
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

    // Cerrar modales
    escalonModal.classList.add("hidden");
    escalonModal.classList.remove("flex");
    nuevoModal.classList.add("hidden");
    nuevoModal.classList.remove("flex");

    // Refrescar tabla / lista
    if (typeof buscarPorIdp === "function") buscarPorIdp();

  } catch (err) {
    console.error(err);
    alert("⚠️ Error de red al confirmar");
  }
}

});
