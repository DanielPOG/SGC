
import toggleIdpState from "./acciones.js"

export function idpRow(idp, cargos) {
  const state = idp.estado
    ? `<div class="mx-auto w-fit px-0 py-[.40em] text-[13px] font-bold rounded-md rounded-r-none hover:bg-green-600/4 border-2 border-r-0 border-green-600/10 text-green-600/80 min-w-20 -me-5">ACTIVO</div>`
    : `<div class="mx-auto w-fit px-0 py-[.40em] text-[13px] font-bold rounded-md rounded-r-none hover:bg-red-600/4 border-2 border-r-0 border-red-600/10 text-red-600/80 min-w-20 -me-5">INACTIVO</div>`
  const cargosIDP = cargos.filter(c =>c.idp.idp_id === idp.idp_id).length
  return (
    ` 
      <td class="px-4 py-2 border text-center">${idp.idp_id}</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${idp.fechaCreacion}</td>
      <td class="px-4 py-2 border text-center ">
        <div class="flex justify-center items-center gap-2 "> 
          <div class="border-r border-black/10 relative pe-5">${state}</div>
          <p class="border-r-1 rounded-r-sm border-black/70 -ms-2 font-semibold">
          
            <a href="http://127.0.0.1:8000/idplanta/historial/?idp_id=${idp.idp_id}" class="hover:bg-black/25 px-2 py-1 pb-[.30em] rounded-e-md border-y-2 border-black/50">Historial</a>
          </p>
          <strong class="border-l-2 ps-1" >Acciones:</strong>
          <button data-estado="${idp.estado ? 0 : 1}" id=${idp.idp_id} ${cargosIDP > 0 ? 'disabled' : ''} data-idp=${idp.idp_id} class="min-w-32 text-white rounded-xl px-2 ${cargosIDP < 1 ? (idp.estado ? 'bg-red-500 hover:bg-red-700 ' :'bg-green-600  hover:bg-green-700' ): 'font-bold bg-gray-500/50 pointer-events-none opacity-[0.5]'}">
            ${idp.estado ? 'DESACTIVAR': 'ACTIVAR '}
          </button> 
          
        </div>
      </td>
    `
    
  )
}
export async function cargarIdps(cargos) {
  try {
    const res = await apiFetch("http://127.0.0.1:8001/api/cargos/idps/", {
      method: "GET",
    })
    if (!res.ok) throw new Error(`ERROR HTTP GET IDPS ${res.status} / ${res.statusText}`)
    const data = await res.json()

    console.log("Datos recibidos:", data)
    const tbody = document.querySelector("table tbody")
    tbody.innerHTML = "" // limpiar antes de volver a pintar
    data.forEach((idp) => {
      const tr = document.createElement("tr")
      tr.classList.add("hover:bg-gray-100")
      tr.innerHTML = idpRow(idp, cargos)

      tbody.appendChild(tr)
    })
  } catch (e) {
    console.error("Error al cargar idps:", e)
  }
}

// Cambiar el estado de una IDP
document.addEventListener("click", (e) => {
        if (e.target.matches("[data-idp]")) {
          const idp = e.target.dataset.idp
          const estado = e.target.dataset.estado == 0 ? 'desactivar' : 'activar'

          const confirmHtml = `
            <div id="confirm-estado" class="bg-black/50 inset-0 z-50 w-screen h-screen fixed overflow-y-hidden">
            <div class="flex items-center h-full">
              <div class="w-1/3 h-fit px-2 rounded-md bg-white mx-auto py-4">
               <p class="text-center font-semibold text-xl">¿Estas seguro de ${estado} esta IDP?</p>
                <div class="flex justify-center mt-5 font-bold gap-5">
                  <button id="accept" class="rounded-md px-2 text-green-600 hover:text-white hover:bg-green-600  border border-green-600">Aceptar</button>
                  <button id="decline" class="rounded-md px-2 text-red-600 hover:text-white hover:bg-red-600 border border-red-600 ">Cancelar</button>
                </div>
              </div>
              </div>
            </div>
          `
          const cambiarEstado = async (e)=>{
              if(e.target == modal.querySelector('#accept')){
                document.querySelector('#confirm-estado').remove()
                toggleIdpState(idp)
                document.removeEventListener('click', cambiarEstado)
              } else if (e.target == modal.querySelector('#decline')) {
                document.querySelector('#confirm-estado').remove()
                document.removeEventListener('click', cambiarEstado)
              }
          }
          document.querySelector('body').insertAdjacentHTML('afterbegin', confirmHtml)
          const modal = document.getElementById('confirm-estado')
          document.addEventListener('click', cambiarEstado)
        }
      })
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await apiFetch('http://127.0.0.1:8001/api/cargos/cargos/')
    if (!res.ok) throw new Error(`ERROR HTTP GET CARGOS ${res.status}`)
    const data = await res.json()
    window.cargos = [...data]
    console.log(`Cargos anidados correctamente: ${JSON.stringify(window.cargos, null, 2)}`)
  } catch (e) {
    console.error("Error al cargar cargos:", e)
  }
  
  const buscarForm = document.getElementById("buscar-idp")
  buscarForm.addEventListener("submit", async (e) => {
    e.preventDefault()
    if (!buscarForm.querySelector("#numero").value){
      await cargarIdps(window.cargos)
      return
      }
    apiFetch(
      `http://localhost:8001/api/cargos/idps/${buscarForm.querySelector("#numero").value
      }`,
      {
        method: "GET",
      }
    )
      .then((res) => {
        if (!res.ok) throw new Error(`ERROR HTTP BUSCAR IDP ${res.status} / ${res.statusText}`)
        return res.json()
      })
      .then((idp) => {
        console.log("IDP Encontrada:", idp)
        const tbody = document.querySelector("table tbody")
        tbody.innerHTML = ""
        const row = document.createElement("tr")
        row.classList.add("hover:bg-gray-100")
        console.error(`ERROR NOMBRE ID PLANTA ${idp.idp_id}`)
        row.innerHTML = idpRow(idp, window.cargos)
        tbody.appendChild(row)
      })
  })
  await cargarIdps(window.cargos)
})
// Crear idp
const crearBtn = document.getElementById("crear-idp")
crearBtn.addEventListener("click", () => {
  const modal = document.querySelector(".new-idp-modal")
  if (!modal.classList.contains("hidden")) return
  modal.classList.remove("hidden")
  document.body.style.overflow = "hidden"
  modal.classList.add("flex")
})