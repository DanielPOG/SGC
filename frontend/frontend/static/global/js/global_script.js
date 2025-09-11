// Listener para validacion de acceso
document.addEventListener("DOMContentLoaded", () => {
  const access = localStorage.getItem("access")
  const refresh = localStorage.getItem("refresh")

  if (!access || !refresh) {
    localStorage.removeItem("access")
    localStorage.removeItem("refresh")
    window.location.href = "http://127.0.0.1:8000/login"
  }
})

async function tokenRefresh(){
  const refresh = localStorage.getItem('refresh')

  const res = await fetch('http://127.0.0.1:8001/api/usuarios/token-refresh/', {
    headers: {"Content-Type":"application/json", "Accept":"application/json"},
    method:'POST',
    body: JSON.stringify({refresh:refresh})
  })

  if (!res.ok) try 
  {
    localStorage.removeItem('access')
    localStorage.removeItem('refresh')
  } finally { window.location.reload() }
  
  
  const data = await res.json()
  localStorage.setItem('access', data.access)

  return data.access
}



window.apiFetch = async (url, options={}) => {
  let token = localStorage.getItem('access')

  const isFData = options.body instanceof FormData
  options.headers = {
    ...(options.headers || {}),
    ...(isFData ? {} : {"Content-Type":"application/json"}),
    "Accept": "application/json",
    "Authorization":`Bearer ${token}`
  }

  let res = await fetch(url, options)
  if(res.status === 401){
    console.warn("Token expirado, intentando refrescar...")
    try {
      token = await tokenRefresh()

      options.headers['Authorization'] = `Bearer ${token}`

      res = await fetch(url, options)
    } catch(e){
      console.error("No se pudo refrescar el token", e)
      throw e
    }
  } 
  return res
}

export default apiFetch



// Listener para cerrar sesión
document.getElementById('logout').addEventListener('click', ()=>{
  if(!localStorage.getItem('access') && !localStorage.getItem('refresh')) {
    console.warn(`No hay sesión que cerrar`)
    return
  }
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
  return location.href = location.href
})