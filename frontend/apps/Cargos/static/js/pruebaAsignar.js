// ================== helpers modal escalonado ==================
function abrirEscalonModal() {
  document.getElementById("escalonModal").classList.remove("hidden");
  document.getElementById("escalonModal").classList.add("flex");
}
function cerrarEscalonModal() {
  document.getElementById("escalonModal").classList.add("hidden");
  document.getElementById("escalonModal").classList.remove("flex");
}

// ================== cargar lista de cargos ==================
async function cargarListaCargos() {
  try {
    const res = await fetch("http://127.0.0.1:8001/api/cargos/cargos/"); // endpoint de cargos
    if (!res.ok) return [];
    return await res.json(); // espera [{id, nombre}, ...]
  } catch (e) {
    console.error(e);
    return [];
  }
}

// ================== manejador principal escalonado ==================
async function manejarSugerenciasEscalonadas(sugerencias, startUsuarioId) {
  if (!Array.isArray(sugerencias) || sugerencias.length === 0) {
    alert("No hay sugerencias escalonadas.");
    return;
  }

  const queue = [...sugerencias];

  const texto = document.getElementById("escalonTexto");
  const btnDevolver = document.getElementById("btnDevolverPlanta");
  const btnAsignar = document.getElementById("btnAsignarOtro");
  const btnOmitir = document.getElementById("btnOmitir");
  const btnDevolverTodo = document.getElementById("btnDevolverTodo");
  const selectorCargos = document.getElementById("selectorCargos");
  const selectCargos = document.getElementById("selectCargos");
  const btnConfirmAsignar = document.getElementById("btnConfirmAsignar");

  // cargar cargos en el select
  const listaCargos = await cargarListaCargos();
  selectCargos.innerHTML = '<option value="">--Selecciona cargo--</option>';
  listaCargos.forEach((c) => {
    const opt = document.createElement("option");
    opt.value = c.id;
    opt.textContent = c.nombre || (c.cargo && c.cargo.nombre) || `Cargo ${c.id}`;
    selectCargos.appendChild(opt);
  });

  abrirEscalonModal();

  function mostrarActual() {
    const cur = queue[0];
    if (!cur) {
      cerrarEscalonModal();
      alert("Proceso escalonado finalizado ✅");
      if (typeof buscarPorIdp === "function") buscarPorIdp();
      return;
    }
    texto.textContent = `👤 Usuario: ${cur.usuario_nombre}`;
    selectorCargos.classList.add("hidden");
  }

  mostrarActual();

  // devolver a planta
  btnDevolver.onclick = async () => {
    const cur = queue.shift();
    if (!cur) return;
    try {
      const res = await fetch("http://127.0.0.1:8001/api/cargos/accion-escalon/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          usuario_id: cur.usuario_id,
          accion: "devolver_planta",
        }),
      });
      const j = await res.json();
      if (j.next_sugerencias && j.next_sugerencias.length) {
        queue.unshift(...j.next_sugerencias);
      }
      mostrarActual();
    } catch (err) {
      console.error(err);
      alert("❌ Error al devolver a planta");
      cerrarEscalonModal();
    }
  };

  // asignar a otro temporal
  btnAsignar.onclick = () => {
    selectorCargos.classList.remove("hidden");
  };

  btnConfirmAsignar.onclick = async () => {
    const cur = queue.shift();
    const destino = selectCargos.value;
    if (!destino) {
      alert("⚠️ Selecciona un cargo destino");
      return;
    }
    try {
      const res = await fetch("http://127.0.0.1:8001/api/cargos/accion-escalon/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          usuario_id: cur.usuario_id,
          accion: "asignar_temporal",
          cargo_destino_id: destino,
        }),
      });
      const j = await res.json();
      if (j.next_sugerencias && j.next_sugerencias.length) {
        queue.unshift(...j.next_sugerencias);
      }
      mostrarActual();
    } catch (err) {
      console.error(err);
      alert("❌ Error al asignar temporal");
      cerrarEscalonModal();
    }
  };

  // omitir
  btnOmitir.onclick = () => {
    queue.shift();
    mostrarActual();
  };

  // devolver todo
  btnDevolverTodo.onclick = async () => {
    if (!confirm("¿Seguro quieres devolver automáticamente toda la cadena?")) return;
    try {
      await fetch("http://127.0.0.1:8001/api/cargos/devolver-todo/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario_id: startUsuarioId }),
      });
      cerrarEscalonModal();
      alert("✅ Se aplicó la devolución completa automáticamente");
      if (typeof buscarPorIdp === "function") buscarPorIdp();
    } catch (err) {
      console.error(err);
      alert("❌ Error al aplicar devolución completa");
    }
  };

  // cerrar modal
  document.getElementById("closeEscalonModal").onclick = () => {
    cerrarEscalonModal();
  };
}

// ================== integración con submit ==================
async function asignarCargo(usuarioId, cargoId) {
  try {
    const res = await fetch(`http://127.0.0.1:8001/api/cargos/cargo-usuarios/?modo=escalonado`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario: usuarioId, cargo: cargoId }),
    });

    const data = await res.json();

    if (!res.ok) {
      console.error(data);
      alert("❌ Error al asignar cargo");
      return;
    }

    // 👉 si no hay sugerencias → directo
    if (!data.sugerencias || data.sugerencias.length === 0) {
      alert("✅ Asignación realizada directamente (sin cascada).");
      if (typeof buscarPorIdp === "function") buscarPorIdp();
      return;
    }

    // 🚨 si hay sugerencias → preguntamos
    if (
      confirm(
        "Se detectó una cadena de reasignaciones.\n\n¿Quieres hacer la reasignación de forma ESCALONADA?\n\nAceptar = Escalonado\nCancelar = Automático"
      )
    ) {
      manejarSugerenciasEscalonadas(data.sugerencias, usuarioId);
    } else {
      await fetch("http://127.0.0.1:8001/api/cargos/devolver-todo/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario_id: usuarioId }),
      });
      alert("✅ Se aplicó la devolución completa automáticamente");
      if (typeof buscarPorIdp === "function") buscarPorIdp();
    }
  } catch (err) {
    console.error(err);
    alert("❌ Error de red al asignar cargo");
  }
}
