import useState from "./hooks.js"

export function idpRow(idp, cargos) {
  const state = idp.estado
    ? `<div class="mx-auto w-fit px-2 text-white font-bold rounded-full bg-green-600/80 min-w-32">ACTIVO</div>`
    : `<div class="mx-auto w-fit px-2 text-white font-bold rounded-full bg-red-600/80 min-w-32">INACTIVO</div>`

  const cargosIDP = cargos.filter(c => c.idp.idp_id === idp.idp_id).length
  return (
    ` 
      <td class="px-4 py-2 border text-center">${idp.idp_id}</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${idp.fechaCreacion}</td>
      <td class="px-4 py-2 border text-center ">
        <div class="flex justify-center gap-2 "> 
          <div>${state}</div>
          <p class="border-r-2 pe-2 border-black"><strong>Cargos activos:</strong> ${cargosIDP}</p>
          <strong>Acciones:</strong>
          <button  class="min-w-32 text-white rounded-xl px-2 ${cargosIDP < 1 ? (idp.estado ? 'bg-red-500 hover:bg-red-700 font-bold' :'bg-green-600 font-bold hover:bg-green-700' ): 'bg-gray-500/50 pointer-events-none'}">
            ${idp.estado ? 'DESACTIVAR': 'ACTIVAR '}
          </button> 
          
        </div>
      </td>
    `
  )
}
export async function cargarIdps(cargos) {
  try {
    const res = await fetch("http://127.0.0.1:8001/api/cargos/idps/", {
      method: "GET",
      headers: { "Content-Type": "application/json" },
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

document.addEventListener("DOMContentLoaded", async () => {
  const [ cargos, setCargos ] = useState([])
  try {
    const res = await fetch('http://127.0.0.1:8001/api/cargos/cargos/')
    if (!res.ok) throw new Error(`ERROR HTTP GET CARGOS ${res.status}`)
    const data = await res.json()
    window.cargos = [...data]
    setCargos(window.cargos)
    console.log(`Cargos anidados correctamente: ${JSON.stringify(cargos(), null, 2)}`)
  } catch (e) {
    console.error("Error al cargar cargos:", e)
  }
  
  const buscarForm = document.getElementById("buscar-idp")
  buscarForm.addEventListener("submit", async (e) => {
    e.preventDefault()
    if (!buscarForm.querySelector("#numero").value){
      await cargarIdps(cargos())
      return
      }
    fetch(
      `http://localhost:8001/api/cargos/idps/${buscarForm.querySelector("#numero").value
      }`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
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
        row.innerHTML = idpRow(idp, cargos())
        tbody.appendChild(row)
      })
  })
  await cargarIdps(cargos())
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