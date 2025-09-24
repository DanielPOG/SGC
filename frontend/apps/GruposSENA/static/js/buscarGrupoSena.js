document.addEventListener("DOMContentLoaded", () => {
  const tbody = document.getElementById("tabla-grupos");
  const inputBuscar = document.getElementById("buscarCargo");
  const btnBuscar = document.getElementById("btnBuscar");

  // Elementos de modales
  const openModal = document.getElementById('openModal');
  const closeModal = document.getElementById('closeModal');
  const modalExcel = document.getElementById('modalExcel');
  const fileInput = document.getElementById('fileInput');
  const fileName = document.getElementById('fileName');
  const nuevoModal = document.getElementById('nuevoModal');
  const closeNuevoModal = document.getElementById('closeNuevoModal');
  const cancelNuevoModal = document.getElementById('cancelNuevoModal');

  // Inicialmente mostrar mensaje de carga
  tbody.innerHTML = "";

  // Función para mostrar alertas
  function mostrarAlerta(mensaje, tipo = 'info') {
    const colores = {
      success: 'bg-green-100 border-green-400 text-green-700',
      error: 'bg-red-100 border-red-400 text-red-700',
      warning: 'bg-yellow-100 border-yellow-400 text-yellow-700',
      info: 'bg-blue-100 border-blue-400 text-blue-700'
    };

    const alerta = document.createElement('div');
    alerta.className = `fixed top-4 right-4 p-4 rounded-lg border ${colores[tipo]} z-50 transition-all duration-300`;
    alerta.innerHTML = `
      <div class="flex items-center justify-between">
        <span>${mensaje}</span>
        <button class="ml-4 text-lg font-bold" onclick="this.parentElement.parentElement.remove()">&times;</button>
      </div>
    `;
    
    document.body.appendChild(alerta);
    
    // Auto-eliminar después de 5 segundos
    setTimeout(() => {
      if (alerta.parentElement) {
        alerta.remove();
      }
    }, 5000);
  }

  // Cargar grupos desde la API
  async function cargarGrupos(search = "") {
    try {
      mostrarAlerta('Cargando grupos...', 'info');
      
      let url = "http://127.0.0.1:8001/api/gruposena/grupo-sena/";
      if (search) url += `?search=${encodeURIComponent(search)}`;

      const res = await fetch(url);
      if (!res.ok) throw new Error("Error al cargar los grupos");

      const grupos = await res.json();
      tbody.innerHTML = "";

      if (grupos.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center py-4">No se encontraron grupos</td></tr>`;
        mostrarAlerta('No se encontraron grupos con los criterios de búsqueda', 'warning');
      } else {
       grupos.forEach(grupo => {
        const row = document.createElement('tr');
        row.className = 'hover:bg-gray-100';
        row.innerHTML = `
          <td class="px-4 py-2 border text-center">${grupo.nombre?.nombre || ""}</td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">${grupo.area?.nombre || ""}</td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">${grupo.estado?.estado || ""}</td>
          <td class="px-4 py-2 border text-center">${grupo.lider ? grupo.lider.nombre_completo : ""}</td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">${grupo.resolucion_definicion || ""}</td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">
            ${grupo.resolucion_creacion ? `<a href="${grupo.resolucion_creacion}" target="_blank" class="text-blue-600 hover:underline">Archivo</a>` : ""}
          </td>
          <td class="px-4 py-2 border text-center relative">
            <button data-dropdown-toggle="dropdown-${grupo.id}" 
                    class="inline-flex items-center p-2 text-sm font-medium text-center text-gray-900 bg-white rounded-lg hover:bg-gray-100 focus:ring-4 focus:outline-none dark:text-white focus:ring-gray-50 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-600" 
                    type="button">
              <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 3">
                <path d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"/>
              </svg>
            </button>
            <div id="dropdown-${grupo.id}" 
                class="dropdown-menu z-10 hidden absolute bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 dark:bg-gray-700 dark:divide-gray-600 mt-2 -translate-x-20">
              <ul class="py-2 text-sm text-gray-700 dark:text-gray-200">
                <li>
                  <a href="/historial_grupo/${grupo.id}" class="block px-4 py-2 hover:bg-gray-100">Historial</a>
                </li>
                <li>
                  <a href="#" data-id="${grupo.id}" class="open-nuevo-modal block px-4 py-2 hover:bg-gray-100">Añadir Funcionario</a>
                </li>
                <li>
                  <a href="/gruposena/gruposena/editar_grupo/${grupo.id}/" class="block px-4 py-2 hover:bg-gray-100">Editar</a>
                </li>
              </ul>
            </div>
          </td>
        `;
        tbody.appendChild(row);
      });

        mostrarAlerta(`Se cargaron ${grupos.length} grupos correctamente`, 'success');
      }

      activarDropdowns();
      activarModalesNuevos();

    } catch (err) {
      console.error(err);
      tbody.innerHTML = `<tr><td colspan="7" class="text-center py-4">Error al cargar los grupos</td></tr>`;
      mostrarAlerta('Error al cargar los grupos. Verifique la conexión.', 'error');
    }
  }

  // Activar dropdowns
  function activarDropdowns() {
    document.querySelectorAll('[data-dropdown-toggle]').forEach(button => {
      const menuId = button.dataset.dropdownToggle;
      const menu = document.getElementById(menuId);

      if (menu) {
        button.addEventListener('click', (e) => {
          e.stopPropagation();
          // Cerrar otros dropdowns
          document.querySelectorAll('.dropdown-menu').forEach(m => {
            if (m.id !== menuId) m.classList.add('hidden');
          });
          menu.classList.toggle('hidden');
        });
      }
    });

    // Cerrar al hacer click fuera
    document.addEventListener('click', () => {
      document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.add('hidden'));
    });
  }

  // Activar modales de "Añadir Funcionario"
  function activarModalesNuevos() {
    document.querySelectorAll('.open-nuevo-modal').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const grupoId = e.target.closest('a').dataset.id;
        if (nuevoModal) {
          nuevoModal.classList.remove('hidden');
          nuevoModal.classList.add('flex');
          mostrarAlerta(`Preparando para añadir funcionario al grupo ID: ${grupoId}`, 'info');
        }
      });
    });
  }

  // EVENTOS 

  // Buscar con Enter
  inputBuscar?.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      const searchTerm = inputBuscar.value.trim();
      if (searchTerm) {
        mostrarAlerta(`Buscando: "${searchTerm}"`, 'info');
      }
      cargarGrupos(searchTerm);
    }
  });

  // Buscar con botón
  btnBuscar?.addEventListener("click", () => {
    const searchTerm = inputBuscar.value.trim();
    if (searchTerm) {
      mostrarAlerta(`Buscando: "${searchTerm}"`, 'info');
    }
    cargarGrupos(searchTerm);
  });

  // Abrir modal Excel
  openModal?.addEventListener('click', () => {
    modalExcel?.classList.remove('hidden');
    modalExcel?.classList.add('flex');
    mostrarAlerta('Modal de importación Excel abierto', 'info');
  });

  // Cerrar modal Excel
  closeModal?.addEventListener('click', () => {
    modalExcel?.classList.add('hidden');
    mostrarAlerta('Modal de Excel cerrado', 'warning');
  });

  // Cerrar modal "Añadir Funcionario"
  closeNuevoModal?.addEventListener('click', () => {
    nuevoModal?.classList.add('hidden');
    mostrarAlerta('Operación de añadir funcionario cancelada', 'warning');
  });

  cancelNuevoModal?.addEventListener('click', () => {
    nuevoModal?.classList.add('hidden');
    mostrarAlerta('Operación de añadir funcionario cancelada', 'warning');
  });

  // Cerrar modales al hacer clic fuera
  window.addEventListener('click', (e) => {
    if (e.target === modalExcel) {
      modalExcel.classList.add('hidden');
      mostrarAlerta('Modal de Excel cerrado', 'warning');
    }
    if (e.target === nuevoModal) {
      nuevoModal.classList.add('hidden');
      mostrarAlerta('Operación de añadir funcionario cancelada', 'warning');
    }
  });

  // Mostrar nombre del archivo seleccionado
  fileInput?.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      fileName.textContent = file.name;
      mostrarAlerta(`Archivo seleccionado: ${file.name}`, 'success');
    } else {
      fileName.textContent = "Ningún archivo";
    }
  });

  // Cargar grupos inicialmente
  cargarGrupos();
});