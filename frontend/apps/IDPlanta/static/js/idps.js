document.addEventListener("DOMContentLoaded", () => {
  try {
    fetch("http://127.0.0.1:8001/api/cargos/idps/", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        const tbody = document.querySelector("table tbody");
        data.forEach((idp) => {
          const tr = document.createElement("tr");
          tr.classList.add("hover:bg-gray-100");
          tr.innerHTML = `
                    <td class="px-4 py-2 border text-center">${idp.numero}</td>
                    <td class="px-4 py-2 border text-center hidden md:table-cell">${idp.fechaCreacion}</td>
                    <td class="px-4 py-2 border text-center relative">
                        <!-- Botón del Dropdown -->
                        <button id="dropdown_${idp.id}" data-dropdown-toggle="dropdown_${idp.numero}" class="inline-flex items-center p-2 text-sm font-medium text-center text-gray-900 bg-white rounded-lg hover:bg-gray-100 focus:ring-4 focus:outline-none dark:text-white focus:ring-gray-50 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-600" type="button"> 
                        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 3">
                            <path d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"/>
                        </svg>
                        </button>

                        <!-- Menú desplegable -->
                        <div id="dropdown_${idp.numero}" class="z-10 hidden absolute right-[.8vw] md:right-[2.8vw] bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 mt-2 -translate-x-20">
                        <ul class="py-2 text-sm text-gray-700">
                            <li>
                            <a href="{% url 'historial_funcionario' %}" class="block px-4 py-2 hover:bg-gray-100">Historial</a>
                            </li>
                            <li>
                            <a href="#" data-modal-target="modal_${idp.id}" class="block px-4 py-2 hover:bg-gray-100">Añadir Formación</a>
                            </li>
                            <li>
                            <a href="{% url 'editar_fun' %}" class="block px-4 py-2 hover:bg-gray-100">Editar</a>
                            </li>
                        </ul>
                        </div>
                    </td>
                `;
          tbody.appendChild(tr);
        });
      });
  } catch (e) {
    console.error("Error al cargar idps:", e);
    return;
  }
  const crearBtn = document.getElementById("crear-idp");
  crearBtn.addEventListener("click", () => (location.href = "../crear_idp"));

  document.addEventListener("click", function (e) {
    const button = e.target.closest("[data-dropdown-toggle]");
    const menu = e.target.closest(".dropdown-menu");

    // Si clic en botón → alternar menú
    if (button) {
      e.stopPropagation();
      // cerrar todos antes de abrir el nuevo
      document
        .querySelectorAll(".dropdown-menu")
        .forEach((m) => m.classList.add("hidden"));

      const menuId = button.dataset.dropdownToggle;
      const targetMenu = document.querySelector(`#${menuId}`);
      targetMenu.classList.toggle("hidden");
      return;
    }

    // Si clic fuera → cerrar todos los menús
    if (!menu) {
      document
        .querySelectorAll(".dropdown-menu")
        .forEach((m) => m.classList.add("hidden"));
    }
  });
});
