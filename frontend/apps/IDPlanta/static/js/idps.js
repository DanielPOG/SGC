import toggleIdpState from "./acciones.js";

const palette = {
  green: "hover:bg-green-600/5 border-green-600/10 text-green-600/80",
  red: "hover:bg-red-600/5 border-red-600/10 text-red-600/80",
};
export const colorDiv = (color, text = "") => {
  if (!palette[color]) return "";
  const divClass = `
      ${palette[color]} mx-auto w-fit px-0 py-[.40em] text-[13px] font-bold
      rounded-r-none rounded-md min-w-20 -me-5 border-2 border-r-0
    `;
  return `<div class="${divClass}">${text}</div>`;
};

export function idpRow(idp, cargos) {
  const state = idp.estado
    ? colorDiv("green", "ACTIVO")
    : colorDiv("red", "INACTIVO");
  const cargosIDP = cargos.filter((c) => c.idp?.numero === idp.numero).length;

 
  const hasCargo = () => {
    const cargo = cargos.find((c) => c.idp?.numero === idp.numero);
    if (!cargo) return "Sin cargo asignado";
    else return cargo.cargoNombre.nombre;
  };
  const hasRegional = () => {
    const cargo = cargos.find((c) => c.idp?.numero === idp.numero);
    if (!cargo) return "Sin Regional Asignada";

    // 1. Si existe objeto regional directo
    if (cargo.regional && cargo.regional.nombre) {
      return cargo.regional.nombre;
    }

    // 2. Si solo viene desde centro
    if (cargo.centro?.regional?.nombre) {
      return cargo.centro.regional.nombre;
    }

    return "Sin Regional Asignada";
  };
  return ` 
        <td class="px-4 py-2 border text-center">${idp.numero}</td>  
        <td class="px-4 py-2 border text-center hidden md:table-cell">${
          idp.fechaCreacion
        }</td>
        <td class="px-4 py-2 border text-center hidden md:table-cell">
        ${hasRegional()}
        </td>
        <td class="px-4 py-2 border text-center hidden md:table-cell">
        ${hasCargo()}
        </td>
        <td class="px-4 py-2 border text-center ">
          <div class="flex justify-center items-center gap-2 "> 
            <div class="border-r border-black/10 relative pe-5">
              ${state}
            </div>
            <p class=" border-r-2 rounded-r-[.7rem] border-black/20 -ms-2 font-semibold shadow-md">
              <a href="http://127.0.0.1:8000/idplanta/historial/?idp_id=${
                idp.numero
              }" class="hover:bg-black/25 px-2 py-1 pb-[.30em] rounded-e-md border-y-2 border-black/50 pe-3 rounded-r-[10rem]">Historial</a>
            </p>
            <strong class="border-l-2 ps-1" >Acciones:</strong>
          <button
    data-estado="${idp.estado ? 0 : 1}"
    id="${idp.numero}"
    ${cargosIDP > 0 ? "disabled" : ""}
    data-idp="${idp.numero}"
    data-cargos-count="${cargosIDP}"
    class="min-w-32 text-white rounded-xl px-2
      ${
        cargosIDP < 1
          ? idp.estado
            ? "bg-red-500/80 hover:bg-red-700 font-semibold"
            : "bg-green-600/80 hover:bg-green-600 font-semibold"
          : "font-bold bg-gray-500/50 pointer-events-none opacity-50"
      }">
    ${idp.estado ? (cargosIDP > 0 ? "OCUPADO" : "DESACTIVAR") : "ACTIVAR"}
  </button >
  ${
    cargosIDP > 0 || idp.estado == 0
      ? ``
      : `
  <button 
    data-action="abrir-modal" 
    data-idpmodal="${idp.numero}"
    class="añadir-cargo bg-blue-600 text-white px-5 py-[1px] rounded-[1rem]">
    Añadir&nbsp;cargo
  </button>
`
  }</div>
        </td>

      `;
}

export async function cargarIdps(cargos) {
  try {
    const res = await apiFetch("http://127.0.0.1:8001/api/cargos/idps/", {
      method: "GET",
    });
    const resR = await apiFetch(
      "http://127.0.0.1:8001/api/general/regionales/"
    );
    window.regionales = await resR.json();
    if (!res.ok)
      throw new Error(`ERROR HTTP GET IDPS ${res.status} / ${res.statusText}`);
    const data = await res.json();

    console.log("Datos recibidos:", data);
    const tbody = document.querySelector("table tbody");
    tbody.innerHTML = ""; // limpiar antes de volver a pintar
    data.forEach(async (idp) => {
      const tr = document.createElement("tr");
      tr.classList.add("hover:bg-gray-100");
      tr.innerHTML = idpRow(idp, cargos);

      tbody.appendChild(tr);
    });
  } catch (e) {
    console.error("Error al cargar idps:", e);
  }
}
document.addEventListener("click", async (e) => {
  const btn = e.target.closest("[data-action='abrir-modal']");

  if (!btn) return;

  const idpNumero = btn.dataset.idpmodal;

  // Crear modal dinámico solo si no existe
  let modal = document.getElementById(`modal-idp-cargo-${idpNumero}`);
  if (!modal) {
    modal = document.createElement("div");
    modal.id = `modal-idp-cargo-${idpNumero}`;
    modal.className =
      "fixed inset-0 z-50 bg-black bg-opacity-50 hidden items-center justify-center";
    modal.innerHTML = `
      <div class="bg-white rounded-lg shadow-lg w-96 p-6 m-auto mt-36 relative">
        <button 
          class="close-modal absolute top-2 right-3 text-gray-500 hover:text-black text-xl font-bold"
          data-idpclose=${idpNumero}>
          ×
        </button>
        <h2 class="text-xl font-bold mb-4">Asignar Cargo</h2>
        <select id="cargoSelect-${idpNumero}" class="w-full border rounded-lg p-2 mb-4">
          <option value="">Seleccione...</option>
          ${window.cargos
            .map(
              (c) => `<option value="${c.id}">${c.cargoNombre.nombre}</option>`
            )
            .join("")}
        </select>
        <h2 class="text-xl font-bold mb-4">Asignar Regional</h2>

        <select id="regionalSelect-${idpNumero
        }" class="w-full border rounded-lg p-2 mb-4">
          <option value="">Seleccione...</option>
          ${window.regionales
            .map((c) => `<option value="${c.id}">${c.nombre}</option>`)
            .join("")}
        </select>
        <button 
          class="guardar-cargo w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700"
          data-asignarcargo="${idpNumero}">
          Guardar
        </button>
      </div>`;
    
    document.body.appendChild(modal);
    const button = document.querySelector(".guardar-cargo");

    const asign = async () => {
      const numero = button.dataset.asignarcargo;
      const regional_id = await document.getElementById(`regionalSelect-${idpNumero}`).value
      const cargo_id = document.getElementById(`cargoSelect-${idpNumero}`).value
      const formData = new FormData()
      formData.append('numero', numero)
      formData.append('regional_id', regional_id)
      formData.append('cargo_id', cargo_id)
      console.log(formData)

      apiFetch("http://127.0.0.1:8001/api/cargos/idps/asignarCargo/", {
        method: "POST",
        body: formData,
      })
        .then((res) => {
          if (!res.ok) throw new Error("Error asignando cargo");
          return res.json();
        })
        .then(async (data) => {
          console.log("Asignación exitosa:", data);
          alert(data.msg);

          // Si quieres actualizar la tabla dinámicamente:
          if (data.cargos) {
            window.cargos = data.cargos
            await cargarIdps(data.cargos); // -> función tuya para refrescar UI
          }
        })
        .catch((err) => console.error("Error:", err));
    };
    button.addEventListener("click", asign);

  }

  // Mostrar modal
  modal.classList.remove("hidden");
  document.addEventListener("click", (e) => {
    const btnClose = e.target.closest(".close-modal");
    if (!btnClose) return;

    const idpNumero = btnClose.dataset.idpclose;
    const modal = document.getElementById(`modal-idp-cargo-${idpNumero}`);
    if (modal) {modal.classList.add("hidden")};
  });
});
// Cerrar modal

// Cambiar el estado de una IDP
// Cambiar el estado de una IDP
document.addEventListener("click", (e) => {
  // encuentra el botón real aunque hagas click en un hijo
  const btn = e.target.closest("button[data-idp]");
  if (!btn) return;

  // si está deshabilitado, no hagas nada
  if (btn.disabled) return;

  const idp = btn.dataset.idp;
  const estado = btn.dataset.estado === "0" ? "desactivar" : "activar";

  // ← lee el conteo de ESTA fila (lo pusiste como data-cargos-count en el botón)
  const cargosCount = parseInt(btn.dataset.cargosCount || "0", 10);

  const buttons =
    cargosCount > 0
      ? `<button id="close" class="rounded-md px-2 text-green-600 hover:text-white hover:bg-green-600 border border-green-600">Aceptar</button>`
      : `<button id="accept" class="rounded-md px-2 text-green-600 hover:text-white hover:bg-green-600 border border-green-600">Aceptar</button>
        <button id="decline" class="rounded-md px-2 text-red-600 hover:text-white hover:bg-red-600 border border-red-600">Cancelar</button>`;

  const confirmHtml = `
      <div id="confirm-estado" class="bg-black/50 inset-0 z-50 w-screen h-screen fixed overflow-y-hidden">
        <div class="flex items-center h-full">
          <div class="w-1/3 h-fit px-2 rounded-md bg-white mx-auto py-4">
            ${
              cargosCount > 0
                ? `<p class="text-center font-semibold text-xl">No es posible modificar el estado de una IDP ocupada</p>`
                : `<p class="text-center font-semibold text-xl">¿Estas seguro de ${estado} esta IDP?</p>`
            }
            <div class="flex justify-center mt-5 font-bold gap-5">
              ${buttons}
            </div>
          </div>
        </div>
      </div>
    `;

  const cambiarEstado = async (ev) => {
    const modal = document.getElementById("confirm-estado");
    if (!modal) return;

    if (ev.target === modal.querySelector("#accept")) {
      modal.remove();
      await toggleIdpState(idp);
      document.removeEventListener("click", cambiarEstado);
    } else if (
      ev.target === modal.querySelector("#decline") ||
      ev.target === modal.querySelector("#close")
    ) {
      modal.remove();
      document.removeEventListener("click", cambiarEstado);
    }
  };

  document.body.insertAdjacentHTML("afterbegin", confirmHtml);
  document.addEventListener("click", cambiarEstado);
});

document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await apiFetch("http://127.0.0.1:8001/api/cargos/cargos/");
    if (!res.ok) throw new Error(`ERROR HTTP GET CARGOS ${res.status}`);
    const data = await res.json();
    window.cargos = [...data];
    console.log(
      `Cargos anidados correctamente: ${JSON.stringify(window.cargos, null, 2)}`
    );
  } catch (e) {
    console.error("Error al cargar cargos:", e);
  }

  const buscarForm = document.getElementById("buscar-idp");
  buscarForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!buscarForm.querySelector("#numero").value) {
      await cargarIdps(window.cargos);
      return;
    }
    apiFetch(
      `http://localhost:8001/api/cargos/idps/${
        buscarForm.querySelector("#numero").value
      }`,
      {
        method: "GET",
      }
    )
      .then((res) => {
        if (!res.ok)
          throw new Error(
            `ERROR HTTP BUSCAR IDP ${res.status} / ${res.statusText}`
          );
        return res.json();
      })
      .then((idp) => {
        console.log("IDP Encontrada:", idp);
        const tbody = document.querySelector("table tbody");
        tbody.innerHTML = "";
        const row = document.createElement("tr");
        row.classList.add("hover:bg-gray-100");
        console.error(`ERROR NOMBRE ID PLANTA ${idp.numero}`);
        row.innerHTML = idpRow(idp, window.cargos);
        tbody.appendChild(row);
      });
  });
  await cargarIdps(window.cargos);
});
// Crear idp
const crearBtn = document.getElementById("crear-idp");
crearBtn.addEventListener("click", () => {
  const modal = document.querySelector(".new-idp-modal");
  if (!modal.classList.contains("hidden")) return;
  modal.classList.remove("hidden");
  document.body.style.overflow = "hidden";
  modal.classList.add("flex");
});
