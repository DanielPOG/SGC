//puto html node que hice para nada (ni lo hice yo) pero lo guardo para despues

`<th class="px-4 py-2 border">Acciones</th>


<td class="px-4 py-2 border text-center relative">
          
         <!-- Botón del Dropdown --> 
          
          <button id="dropdown_${idp.idp_id}" data-dropdown-toggle="dropdown-${idp.idp_id}" class="inline-flex items-center p-2 text-sm font-medium text-center text-gray-900 bg-white rounded-lg hover:bg-gray-100 focus:ring-4 focus:outline-none dark:text-white focus:ring-gray-50 dark:bg-gray-800 dark:hover:bg-gray-700 dark:focus:ring-gray-600" type="button">
            <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 16 3">
              <path d="M2 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm6.041 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM14 0a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z" />
            </svg>
          </button>

          
           <!--Menú desplegable--> 
          
          <div id="dropdown-${idp.idp_id}" class="dropdown-menu z-10 hidden absolute right-[.8vw] md:right-[2.8vw] bg-white divide-y divide-gray-100 rounded-lg shadow-sm w-44 mt-2 -translate-x-20">
            <ul class="py-2 text-sm text-gray-700">
              <li>
                <a href="{% url 'historial_funcionario' %}" class="block px-4 py-2 hover:bg-gray-100">Historial</a>
              </li>
              <li>
                <a href="#" data-modal-target="modal_${idp.idp_id}" class="block px-4 py-2 hover:bg-gray-100">Editar</a>
              </li>
            </ul>
          </div>
        </td>`


        /// puto script de mierda que hice para nada pero guardo para despues:
        document.addEventListener("click", function (e) {
  if (e.target.closest("[data-dropdown-toggle]")) {
    const button = e.target.closest("[data-dropdown-toggle]");
    const menuId = button.dataset.dropdownToggle;
    const menu = document.getElementById(menuId);

    //Cierra todos los demás menús antes de abrir otro
    document.querySelectorAll(".dropdown-menu").forEach(m => {
      if (m.id !== menuId) {
        m.classList.add("hidden");
      }
    });

    // Toggle solo del menú clickeado
    menu.classList.toggle("hidden");

  } else {
    // Si haces click fuera, se cierran todos
    document.querySelectorAll(".dropdown-menu").forEach(menu => {
      menu.classList.add("hidden");
    });
  }
});