import { cargarIdps } from "./idps.js";
function showMessage(msg) {
  const node = `
    <div class="state-response fixed inset-0 flex justify-center items-center bg-black/60 z-10">
      <div class="w-fit px-5 py-5 bg-white rounded-md shadow-md">
        <p class="text-center font-bold text-xl">${msg}</p>
      </div>
    </div>
  `
  document.body.insertAdjacentHTML("afterbegin", node)
  const elem = document.querySelector(".state-response")
  setTimeout(() => elem.remove(), 2000)
}
export default async function toggleIdpState(idp) {
  try {
    const formData = new FormData()
    formData.append('idp_id',idp)
    const res = await fetch("http://127.0.0.1:8001/api/cargos/idps/cambiarEstado/", {
      method: "PATCH",
      body: formData
    })
    if(!res){
    showMessage("Error al actualizar estado")
    }
    const data = await res.json()

    if (data.error) {
      showMessage(data.error)
    } else if(data.msg) {
      showMessage(`${data.msg} correctamente`)
    }

    await cargarIdps(window.cargos)
  } catch (e) {
    console.error(`Error cambiando el estado de IDP:`, e)
    showMessage("Error al actualizar estado")
  }
}