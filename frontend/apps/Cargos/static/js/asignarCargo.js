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

  // 👉 helper para evitar duplicados
  function agregarDecision(decision) {
    decisiones = decisiones.filter(d => d.usuario_id !== decision.usuario_id);
    decisiones.push(decision);
  }

  // Cargar estados
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

  // Abrir modal nuevo
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

  // Validar formulario
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

  // Guardar root y obtener sugerencias
  formAsignarFuncionario.addEventListener("submit", async e => {
    e.preventDefault();

    const camposRoot = [
      { id: "usuarioId", nombre: "Número de documento" },
      { id: "grado", nombre: "Grado" },
      { id: "salario", nombre: "Salario" },
      { id: "resolucion", nombre: "Resolución" },
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
      fechaInicio: document.getElementById("fechaInicio").value,

    };

    try {
      const formData = new FormData();
      Object.entries(payloadRootBase).forEach(([k, v]) => formData.append(k, v));

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

  // Mostrar sugerencia
  function mostrarSiguienteSugerencia() {
    if (indiceActual >= sugerenciasGlobal.length) {
      enviarConfirmacion();
      return;
    }

    const sug = sugerenciasGlobal[indiceActual];
    escalonTexto.textContent = `¿Qué hacer con ${sug.usuario_nombre}?`;
    selectorCargos.classList.add("hidden");
    selectCargos.innerHTML = "";

    // Devolver a PLANTA
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
        resolucion_archivo: null
      });
      indiceActual++;
      mostrarSiguienteSugerencia();
    };

    // Asignar a TEMPORAL
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
        resolucion_archivo: null
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

  // Confirmación final
  async function enviarConfirmacion() {
    const destino = parseInt(cargoIdInput.value);
    if (!destino) {
      alert("Error interno: no se detectó el cargo destino");
      return;
    }

    try {
      const payload = {
        root_usuario_id: rootUsuarioId,
        cargo_destino_id: destino,
        decisiones: decisiones.map(d => {
          d.fechaInicio = d.fechaInicio.split("T")[0];
          if (d.fechaRetiro) {
            d.fechaRetiro = d.fechaRetiro.split("T")[0];
          } else {
            delete d.fechaRetiro;
          }
          if (!d.resolucion_archivo) delete d.resolucion_archivo;
          return d;
        }),
        payload_root: { ...payloadRootBase, fechaInicio: payloadRootBase.fechaInicio.split("T")[0] }
      };

      const res = await fetch("http://127.0.0.1:8001/api/cargos/cargo-usuarios/confirmacion/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json().catch(() => ({}));

      if (!res.ok) {
        console.error("Error en confirmación:", data);
        alert("❌ Error al aplicar decisiones");
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
