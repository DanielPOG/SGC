document.addEventListener("DOMContentLoaded", async () => {
  const form = document.querySelector("form") || document.createElement("form"); // tu div no tiene form
  const modo = form.dataset.mode || "create";  // "create" o "edit"
  const grupoId = form.dataset.id;            // solo en edit

  // 🔹 Función para cargar selects desde API
  async function cargarSelect(url, selectId, labelField = "nombre") {
    const select = document.getElementById(selectId);
    if (!select) return;
    select.innerHTML = '<option value="">-- Selecciona --</option>';
    try {
      const resp = await fetch(url);
      if (!resp.ok) throw new Error("Error en la API");
      const data = await resp.json();
      data.forEach(item => {
        const option = document.createElement("option");
        option.value = item.id;
        option.textContent = item[labelField];
        select.appendChild(option);
      });
    } catch (err) {
      console.error(`⚠️ Error cargando ${selectId}:`, err);
    }
  }

  // 🔹 Cargar selects
  await cargarSelect("http://127.0.0.1:8001/api/general/centros/", "opcion", "nombre");
  await cargarSelect("http://127.0.0.1:8001/api/usuarios/usuarios/", "lider", "get_full_name");

  // 🔹 Si estamos en modo EDITAR → precargar datos
  if (modo === "edit" && grupoId) {
    try {
      const resp = await fetch(`http://127.0.0.1:8001/api/gruposena/grupo-sena/${grupoId}/`);
      if (!resp.ok) throw new Error("No se pudo obtener el grupo");
      const data = await resp.json();

      document.querySelector("input[type=text]").value = data.nombre_grupo?.nombre || "";
      document.querySelector("input#fechaIngreso").value = data.fecha_creacion || "";
      document.getElementById("opcion").value = data.centro?.id || "";
      document.getElementById("lider").value = data.lider?.id || "";
      document.getElementById("observacion").value = data.observacion || "";

    } catch (err) {
      console.error("❌ Error precargando grupo:", err);
    }
  }

  // 🔹 Validación simple
  function validarFormulario() {
    const campos = ["opcion", "lider"];
    for (let id of campos) {
      const val = document.getElementById(id)?.value;
      if (!val) {
        alert(`❌ Por favor selecciona: ${id}`);
        return false;
      }
    }
    return true;
  }

  // 🔹 Submit → POST o PUT
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!validarFormulario()) return;

    const formData = new FormData();
    formData.append("centro", document.getElementById("opcion").value);
    formData.append("lider", document.getElementById("lider").value);
    formData.append("observacion", document.getElementById("observacion").value);

    // Archivos
    const archivos = document.querySelectorAll("input[type=file]");
    archivos.forEach((fileInput, idx) => {
      if (fileInput.files[0]) {
        formData.append(`resolucion_${idx + 1}`, fileInput.files[0]);
      }
    });

    let url = "http://127.0.0.1:8001/api/gruposena/grupo-sena/";
    let method = "POST";
    if (modo === "edit" && grupoId) {
      url += `${grupoId}/`;
      method = "PUT";
    }

    try {
      const resp = await fetch(url, { method, body: formData });
      const body = await resp.json();
      if (!resp.ok) {
        console.error("❌ Errores backend:", body);
        alert("❌ Error guardando grupo, revisa consola");
        return;
      }
      alert(modo === "edit" ? "✅ Grupo actualizado" : "✅ Grupo creado");
      window.location.href = "/gruposena/grupo_sena"; // redirigir
    } catch (err) {
      console.error("❌ Error:", err);
      alert("❌ Error guardando grupo");
    }
  });
});
