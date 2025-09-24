const loadUsersRows = (users, auths) => {
  console.log(`Usuarios recibidos:`, users);
  console.log(`Autorizaciones recibidas:`, auths);
  const tbody = document.querySelector("table tbody");
  users.map((user) => {
    const $row = `<tr class="hover:bg-gray-100">
      <td class="px-4 py-2 border text-center">${user.nombre} ${
      user.apellido
    }</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${
        user.num_doc ? user.num_doc : "No definido"
      }</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">
        ${user.cargo.nombre || "Sin cargo"}
      </td>
      <td class="px-4 py-2 border text-center">${user.estado.nombre}</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${
        user.correo
      }</td>
      <td class="border text-center relative">
        <button  data-user=${
          user.id
        } class="w-full h-full bg-white-600 text-black font-semibold py-2 rounded hover:bg-green-300 transition">
          Autorizaciones
        </button>
      </td>
    </tr>`;
    tbody.innerHTML += $row;


    // AUTORIZACIONES
    const $permisos = document.querySelector(`[data-user="${user.id}"]`);

    $permisos.addEventListener("click", (e) => {
      if (e.target !== $permisos || e.target.dataset.user != user.id) return;
      // HTML del modal para la autorizacion

      const $modal = `
  <div id="auths-${
    user.id
  }" class="fixed flex inset-0 bg-slate-500/40 hidden justify-center mx-auto items-center z-20">
    <div class="bg-white rounded-lg w-96 p-6 relative h-auto">
      <!-- Botón para cerrar -->
      <button id="closeAuths" class="absolute top-2 right-3 text-gray-600 hover:text-black text-xl font-bold">×</button>
      <!-- Formulario -->
      <form class="space-y-3">
        ${auths.auths
          .map((auth) => {
            console.log('AAAA',auth.permisos)
            return `
            <div>
              <label class="flex items-center space-x-2 cursor-pointer">
                <input 
                  type="checkbox" 
                  name="${auth.permisos.codigo}-permisos"
                  class="principal w-5 h-5 text-green-600" 
                  data-target="submenu-${auth.permisos.codigo}" 
                />
                <span>${auth.nombre}</span>
              </label>
              <!-- Submenu dinámico -->
              <div 
                id="submenu-${auth.permisos.codigo}" 
                class="ml-6 mt-2 space-y-2 max-h-0 overflow-hidden opacity-0 transition-all duration-300"
              >
                <label class="flex items-center space-x-2">
                  <input 
                    type="checkbox" 
                    class="select-all w-5 h-5 text-green-600" 
                    data-group="${auth.permisos.codigo}" 
                  />
                  <span>Seleccionar todos</span>
                </label>
                ${auth.permisos
                  .map(
                    (perm) => `
                  <label class="flex items-center space-x-2">
                    <input 
                      type="checkbox" 
                      class="submenu-${auth.permisos.codigo} w-5 h-5 text-green-600" 
                      data-group="${auth.permisos.codigo}" 
                      value="${perm.codigo}"
                    />
                    <span>${perm.nombre}</span>
                  </label>
                `
                  )
                  .join("")}
              </div>
            </div>
          `;
          })
          .join("")}
      </form>
    </div>
  </div>
`;

      if (document.getElementById(`auths-${user.id}`)) {
        console.log("Ya hay un modal abierto");
        return;
      }
      document.body.insertAdjacentHTML("afterbegin", $modal);

      const $$modal = document.getElementById(`auths-${user.id}`);
      const $close = document.getElementById("closeAuths");

      $$modal.classList.toggle("hidden");
      $$modal.addEventListener("click", (e) => {
        if (e.target == document.getElementById(`auths-${user.id}`)) {
          document.body.removeChild($$modal);
        }
      });
      $close.addEventListener("click", () => {
        document.body.removeChild($$modal);
      });
      document.querySelectorAll(".principal").forEach((principal) => {
        principal.addEventListener("change", function () {
          const target = document.getElementById(this.dataset.target);

          // Ocultar todos menos el actual
          document.querySelectorAll("[id^='submenu-']").forEach((sub) => {
            if (sub !== target) {
              sub.style.maxHeight = null;
              sub.style.opacity = 0;
            }
          });

          // Mostrar/ocultar actual
          if (this.checked) {
            target.style.transition = "all 0.3s ease";
            target.style.maxHeight = target.scrollHeight + "px";
            target.style.opacity = 1;
          } else {
            target.style.maxHeight = null;
            target.style.opacity = 0;
          }
        });
      });
    });
  });
};

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const itsResOk = (res) => res && res.ok;
    const loadUsersNAuths = async () => {
      try {
        // Fetch users
        const res = await apiFetch(
          "http://127.0.0.1:8001/api/usuarios/usuario/cargarUsers"
        );
        if (!itsResOk(res)) throw new Error("Error fetching users");
        const users = await res.json();
        console.log("Usuarios fetched");

        // Fetch auths
        const resA = await apiFetch(
          "http://127.0.0.1:8001/api/usuarios/asignar-permisos/getAuths/"
        );
        if (!itsResOk(resA))
          throw new Error(`Error fetching auths ${JSON.stringify(resA)}`);
        const auths = await resA.json();
        console.log("Autorizaciones fetched");

        return { users, auths };
      } catch (err) {
        console.error("Hubo un error cargando usuarios:", err);
        return null; // 👈 important
      }
    };
    // Usage
    const data = await loadUsersNAuths();
    if (data) {
      const { users, auths } = data;
      loadUsersRows(users, auths);
      console.log("Usuarios cargados");
    } else {
      console.warn("No se pudieron cargar usuarios/autorizaciones");
    }
  } catch (e) {
    console.log(`Hubo un error cargando usuarios: ${e}`);
  }
});

// funcionario-permisos
// cargo-permisos
// grupos-permisos
// reportes-permisos
// idp-permisos
// solicitudes-permisos
// autorizacion-permisos

const funcionario = document.querySelector('[name="funcionario-permisos"]');
const cargo = document.querySelector('[name="cargo-permisos"]');
const grupos = document.querySelector('[name="grupos-permisos"]');
const reportes = document.querySelector('[name="reportes-permisos"]');
const idp = document.querySelector('[name="idp-permisos"]');
const solicitudes = document.querySelector('[name="solicitudes-permisos"]');
const autorizacion = document.querySelector('[name="autorizacion-permisos"]');
