async function tokenRefresh(){
  const refresh = localStorage.getItem('refresh')

  const res = await fetch('http://127.0.0.1:8001/api/token/refresh', {
    headers: {"Content-Type":"application/json"},
    method:'POST',
    body: JSON.stringify({refresh})
  })

  if(!res.ok){
    throw new Error("Sesión expirada, vuelva a inicar sesión.")
  }

  const data = await res.json()
  localStorage.setItem('access', data.access)

  return data.access
}

export const apiFetch = async (url, options={}) => {
  let token = localStorage.getItem('access')

  options.headers = {
    ...(options.headers || {}),
    "Content-Type":"application/json",
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