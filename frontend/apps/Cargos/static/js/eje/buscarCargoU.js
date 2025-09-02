// Detectar el enter del input 
document.getElementById("buscarCargo").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      event.preventDefault(); // evita que recargue la página
      buscarPorIdp();
    }
  });

//Funcion para buscar cargo por IDP
async function buscarPorIdp() {
  const id = document.getElementById("buscarCargo").value;
  if (!id) {
    alert("Ingrese un IDP válido");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8001/api/cargos/cargo-usuarios/por-idp/${id}/`);
    if (!response.ok) {
      throw new Error("Cargo no encontrado");
    }

    const cargos = await response.json(); // ahora es una lista
    if (cargos.length === 0) { // Respuesta si no encontro
      throw new Error("Cargo no encontrado");
    }
    const tablaBody = document.querySelector("table tbody");

    // Limpio la tabla antes de agregar resultados
    tablaBody.innerHTML = "";

    cargos.forEach(cargo => {
      tablaBody.innerHTML += `
        <tr class="hover:bg-gray-100">
          <td class="px-4 py-2 border text-center">${cargo.cargo.cargoNombre?.nombre || "Sin nombre"}</td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">${cargo.cargo.centro?.nombre || "-"}</td>
          <td class="px-4 py-2 border text-center">${cargo.cargo.idp?.numero || "-"}</td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">${cargo.estado.estado || "-"}</td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">${cargo.usuario?.nombre || "Sin asignar"}</td>
          <td class="px-4 py-2 border text-center hidden md:table-cell">${cargo.cargo.fechaCreacion || "-"}</td>
          <td class="px-4 py-2 border text-center relative">
            <!-- Botón del Dropdown -->
            <button data-dropdown-toggle="dropdown-${cargo.id}" 
                    class="inline-flex items-center p-2 text-sm font-medium text-center text-gray-900 bg-white rounded-lg hover:bg-gray-100 focus:ring-4 focus:outline-none dark:text-white focus:ring-gray-50 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-600" 
                    type="button">
              <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 3">
                <path d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"/>
              </svg>
            </button>

            <!-- Menú desplegable -->
            <div id="dropdown-${cargo.id}" 
                 class="dropdown-menu z-10 hidden absolute bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 dark:bg-gray-700 dark:divide-gray-600 mt-2 -translate-x-20">
              <ul class="py-2 text-sm text-gray-700 dark:text-gray-200">
                <li>
                  <a href="{% url 'cargohistorial' %}" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Historial</a>
                </li>
                <li>
                  <a href="#" id="openNuevoModal" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Añadir Funcionario</a>
                </li>
                <li>
                  <a href="{% url 'editar_cargo' %}" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Editar</a>
                </li>
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

// Delegación de eventos (sirve para botones existentes y futuros)
// Para menu desplegable
document.addEventListener("click", function (e) {
  const button = e.target.closest("[data-dropdown-toggle]");
  const menu = e.target.closest(".dropdown-menu");

  if (button) {
    e.stopPropagation();
    const menuId = button.dataset.dropdownToggle;
    const targetMenu = document.querySelector(`#${menuId}`);
    targetMenu.classList.toggle("hidden");
    return;
  }

  // Si haces clic fuera → cerrar menús
  if (!menu) {
    document.querySelectorAll(".dropdown-menu").forEach(menu => {
      menu.classList.add("hidden");
    });
  }
});
