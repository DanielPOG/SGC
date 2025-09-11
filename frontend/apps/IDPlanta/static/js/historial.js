
const params = new URLSearchParams(location.search)
const idp_id = params.get('idp_id')
console.log(`Locacion/pathname idp_id: ${idp_id}`)

//Nodos

document.addEventListener('DOMContentLoaded', ()=>{
    try {
      const data = apiFetch('', {
        
      })
    } catch(e) {
      console.error(`Hubo un error al cargar y renderizar el historial: ${e}`)
    }
})