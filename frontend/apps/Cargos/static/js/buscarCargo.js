document.addEventListener("DOMContentLoaded", () => {
// Detectar el Enter del input
document.getElementById("buscarCargo").addEventListener("keypress", function (event) {
  if (event.key === "Enter") {
    event.preventDefault(); // evita que recargue la página
    buscarPorIdp();
  }
});
// Detectar click en el botón
document.getElementById("btnBuscar").addEventListener("click", buscarPorIdp);


// Función para buscar cargos por IDP
async function buscarPorIdp() {
  const id = document.getElementById("buscarCargo").value.trim();
  if (!id) {
    alert("Ingrese un IDP válido");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8001/api/cargos/cargos/por-idp/${id}/`);
    
    // Manejo de errores del backend
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const errorMessage = errorData?.detail || "Error en la búsqueda de cargos";
      throw new Error(errorMessage);
    }

    const cargos = await response.json(); // siempre es lista
    if (!Array.isArray(cargos) || cargos.length === 0) {
      throw new Error("No se encontraron cargos para este IDP");
    }

    const tablaBody = document.querySelector("table tbody");
    tablaBody.innerHTML = ""; // limpio la tabla


    cargos.forEach(cargo => {
      tablaBody.innerHTML += `
        <tr class="hover:bg-gray-100">
          <!-- Cargo -->
          <td class="px-4 py-2 border text-center">${cargo.cargo?.nombre || "Sin nombre"}</td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">${cargo.cargo?.centro || "-"}</td>
          <td class="px-4 py-2 border text-center">${cargo.cargo?.idp || "-"}</td>

          <!-- Titular Planta -->
          <td class="px-4 py-2 border text-center hidden md:table-cell">
            ${cargo.titular ? cargo.titular.nombre : "Sin titular"}
          </td>

          <!-- Encargados Temporales -->
          <td class="px-4 py-2 border text-center hidden md:table-cell">
            ${cargo.encargados?.length 
              ? cargo.encargados.map(e => `${e.nombre} (${e.estado})`).join("<br>")
              : "Sin encargado"}
          </td>

          <!-- Fecha último encargo -->
          <td class="px-4 py-2 border text-center hidden md:table-cell">
            ${cargo.encargados?.length ? cargo.encargados[cargo.encargados.length - 1].fechaInicio : "-"} 
    
          </td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">
            ${cargo.cargo.fechaCreacion}
          </td>

          <!-- Acciones -->
          <td class="px-4 py-2 border text-center relative">
            <button data-dropdown-toggle="dropdown-${cargo.cargo.id}" 
                    class="inline-flex items-center p-2 text-sm font-medium text-center text-gray-900 bg-white rounded-lg hover:bg-gray-100 focus:ring-4 focus:outline-none dark:text-white focus:ring-gray-50 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-600" 
                    type="button">
              <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 3">
                <path d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"/>
              </svg>
            </button>
            <div id="dropdown-${cargo.cargo.id}" 
                class="dropdown-menu z-10 hidden absolute bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 dark:bg-gray-700 dark:divide-gray-600 mt-2 -translate-x-20">
              <ul class="py-2 text-sm text-gray-700 dark:text-gray-200">
                <li><a href="{% url 'cargohistorial' %}" class="block px-4 py-2 hover:bg-gray-100">Historial</a></li>
                <li><a href="#" id="openNuevoModal" class="block px-4 py-2 hover:bg-gray-100">Añadir Funcionario</a></li>
                <li><a  href="${window.urlEditarCargoBase}${cargo.cargo.id}/"   class="block px-4 py-2 hover:bg-gray-100">Editar</a></li>
              </ul>
            </div>
          </td>
        </tr>
      `;
    });
  } catch (error) {
    alert(error.message);
  }
}


// Script para manejar el menú desplegable
document.addEventListener("click", function (e) {
  const button = e.target.closest("[data-dropdown-toggle]");
  const menu = e.target.closest(".dropdown-menu");

  // Si clic en botón → alternar menú
  if (button) {
    e.stopPropagation();
    // cerrar todos antes de abrir el nuevo
    document.querySelectorAll(".dropdown-menu").forEach(m => m.classList.add("hidden"));

    const menuId = button.dataset.dropdownToggle;
    const targetMenu = document.querySelector(`#${menuId}`);
    targetMenu.classList.toggle("hidden");
    return;
  }

  // Si clic fuera → cerrar todos los menús
  if (!menu) {
    document.querySelectorAll(".dropdown-menu").forEach(m => m.classList.add("hidden"));
  }
});

});