
import { cargarIdps } from "./idps.js"
    const fileInput = document.getElementById('file-input')
    const submitButton = document.getElementById('upload-excel')

    submitButton.addEventListener('click', async ()=>{
    const file = fileInput.files[0]
    if(!file){
      alert("Por favor selecciona un archivo excel")
      return
    }

    const formData = new FormData()
    console.log(`Catched file: ${file.name}`)
    formData.append("file", file)

    try {
      const res = await apiFetch("http://127.0.0.1:8001/api/cargos/idps/cargarExcel/", {
        method: "POST",
        body: formData
      })
      const data = await res.json()
      if(res.ok){
        alert(`✅ ${data.msg}\nCreados: ${data.creados}\nActualizados: ${data.actualizados}`)
        if (data.errores && data.errores.length > 0) {
          console.log("Errores:", data.errores)
        }
        await cargarIdps(window.cargos)
      }else{
        alert(`❌ Error: ${data.error || "No se pudo procesar el archivo"}`)
      }
    }catch(e){
      console.error(e)
      alert('Hubo un error de conexión con el servidor')
    }
  })