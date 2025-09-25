document.addEventListener("DOMContentLoaded", async () => {
  // 🔹 Toggle del textarea de observación
  function toggleTextarea() {
    document.getElementById("textarea-observacion").classList.toggle("hidden");
  }
  window.toggleTextarea = toggleTextarea;

  const grupoForm = document.getElementById("grupoForm");
  const modo = grupoForm.dataset.mode || "create";
  const grupoId = grupoForm.dataset.id;

  let grupoData = {};

  // 🔹 Cargar usuarios para el select de líder
  async function cargarUsuarios() {
    const select = document.getElementById("lider");
    select.innerHTML = '<option value="">Cargando...</option>';
    try {
      // URL CORRECTA con puerto 8001
      const res = await fetch("http://127.0.0.1:8001/api/gruposena/usuarios/usuarios/");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      
      select.innerHTML = '<option value="">-- Selecciona --</option>';
      data.forEach(u => {
        const option = document.createElement("option");
        option.value = u.id;
        option.textContent = u.nombre_completo || `${u.nombre} ${u.apellido}`;
        select.appendChild(option);
      });
    } catch (err) {
      console.error("Error cargando usuarios:", err);
      // Fallback: usar datos del template
      select.innerHTML = `
        <option value="">-- Selecciona --</option>
        {% for lider in lideres %}
          <option value="{{ lider.id }}" {% if grupo.lider and grupo.lider.id == lider.id %}selected{% endif %}>
            {{ lider.nombre }} {{ lider.apellido }}
          </option>
        {% endfor %}
      `;
    }
  }

  // 🔹 Precargar datos del grupo
  async function cargarGrupo() {
    if (modo === "edit" && grupoId) {
      try {
        const res = await fetch(`http://127.0.0.1:8001/api/gruposena/grupo-sena/${grupoId}/`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const grupo = await res.json();

        grupoData = grupo;

        // Llenar campos del formulario
        document.getElementById("fechaIngreso").value = grupo.fecha_creacion || "";
        document.getElementById("fechaCierre").value = grupo.fecha_cierre || "";
        document.getElementById("observacion").value = grupo.observacion || "";

        // Llenar nombre y área (solo lectura)
        if (grupo.nombre && grupo.nombre.nombre) {
          const nombreInput = document.querySelector("input[name='nombre_id']").previousElementSibling;
          if (nombreInput) nombreInput.value = grupo.nombre.nombre;
        }
        if (grupo.area && grupo.area.nombre) {
          const areaInput = document.querySelector("input[name='area_id']").previousElementSibling;
          if (areaInput) areaInput.value = grupo.area.nombre;
        }

        // Líder (esperar a que se carguen los usuarios)
        setTimeout(() => {
          if (grupo.lider) {
            const liderSelect = document.getElementById("lider");
            liderSelect.value = grupo.lider.id;
          }
        }, 500);

        // Mostrar links de resoluciones si existen
        if (grupo.resolucion1) {
          const cont1 = document.getElementById("link_resolucion1");
          if (cont1) {
            cont1.innerHTML = `<a href="http://127.0.0.1:8001${grupo.resolucion1}" target="_blank" class="text-blue-600 hover:underline">Ver Resolución 1</a>`;
          }
        }

        if (grupo.resolucion2) {
          const cont2 = document.getElementById("link_resolucion2");
          if (cont2) {
            cont2.innerHTML = `<a href="http://127.0.0.1:8001${grupo.resolucion2}" target="_blank" class="text-blue-600 hover:underline">Ver Resolución 2</a>`;
          }
        }

      } catch (err) {
        console.error("Error cargando grupo:", err);
      }
    }
  }


  // Cargar datos
  await cargarUsuarios();
  await cargarGrupo();

  // 🔹 Enviar formulario - USANDO EL MÉTODO TRADICIONAL DE DJANGO
  // Para evitar problemas CORS y de archivos, es mejor usar el método tradicional
  grupoForm.addEventListener("submit", function(e) {
    // Para edición, usar el método POST tradicional de Django
    if (modo === "edit") {
      // Agregar un campo hidden para indicar que es una actualización
      const methodInput = document.createElement('input');
      methodInput.type = 'hidden';
      methodInput.name = '_method';
      methodInput.value = 'PUT';
      grupoForm.appendChild(methodInput);
    }
    
    // Validación básica de fechas
    const fechaCierre = document.getElementById("fechaCierre").value;
    const fechaIngreso = document.getElementById("fechaIngreso").value;
    
    if (fechaCierre && fechaIngreso && fechaCierre < fechaIngreso) {
      e.preventDefault();
      alert("La fecha de cierre no puede ser anterior a la fecha de creación");
      return false;
    }
    
    console.log("Formulario enviado tradicionalmente a Django");
  });

});