
const params = new URLSearchParams(location.search)
const idp_id = params.get('idp_id')
console.log(`Locacion/pathname idp_id: ${idp_id}`)

//Nodos

function processHistorial(historial){
  return(`
      <td class="px-4 py-2 border text-center">${historial.cargo_id.nombre}</td>
      <td class="px-4 py-2 border text-center">${historial.fecha_asignacion}</td>  
      <td class="px-4 py-2 border text-center">${historial.fecha_desasignacion}</td>  
  `)

}

async function loadHistorial(){
    try {
      const params = new URLSearchParams(location.search)
      const idp_id = params.get('idp_id')
      const res = await apiFetch(`http://127.0.0.1:8001/api/cargos/idps/historialCargos/?idp_id=${idp_id}`, {
        method:'GET'
      })
      const data = await res.json()
      const historial = data.idp_historial.map(element =>{
        processHistorial(element)
      }).join("")
      document.querySelector('table tbody').innerHTML = historial
    } catch(e) {
      console.error(`Hubo un error al cargar y renderizar el historial: ${e}`)
    }
}

document.addEventListener('DOMContentLoaded', async ()=>{
    await loadHistorial()
})