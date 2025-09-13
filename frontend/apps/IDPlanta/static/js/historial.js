const params = new URLSearchParams(location.search)
const idp_id = params.get('idp_id')
console.log(`Locacion/pathname idp_id: ${idp_id}`)

document.addEventListener('DOMContentLoaded',async ()=>{
  const res = await apiFetch(`http://127.0.0.1:8001/api/cargos/idps/historialCargos/?idp_id=${idp_id}`,{
    headers:{'Accept':'text/html'}
  })    
  const data = await res.text()
    console.log('Historial:',data)

})