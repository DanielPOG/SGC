// fetchUsers


const userRow = (user)=>{
    return (`<tr class="hover:bg-gray-100">
      <td class="px-4 py-2 border text-center">${user.nombre} ${user.apellido}</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${user.num_doc ? user.num_doc:'No definido'}</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${user.cargo.cargoNombre_id.nombre}</td>
      <td class="px-4 py-2 border text-center">${user.estado_id.nombre}</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${user.correo}</td>
      <td class="border text-center relative">
        <button id="openNuevoModal" class="w-full h-full bg-white-600 text-black font-semibold py-2 rounded hover:bg-green-300 transition">
          Seleccionar
        </button>
      </td>
    </tr>`)
}

document.addEventListener('DOMContentLoaded',()=>{
    try {
        apiFetch('http://127.0.0.1:8001/api/usuarios/usuario/', {method:'GET'})
        .then(res=> res.json()).then(data => {
          const tbody = document.querySelector('table tbody')
          console.log('Usuarios fetched', data)

          const rows = data.map(user => userRow(user))
          
          tbody.innerHTML = rows.join('')
        }).catch(e=>{
          console.error('Error adjuntando usuarios ', e)
          return
        })
        console.log('Usuarios cargados')
    } catch(e) {
        console.log(`Hubo un error cargando usuarios: ${e}`)
    }
})




// funcionario-permisos
// cargo-permisos
// grupos-permisos
// reportes-permisos
// idp-permisos
// solicitudes-permisos
// autorizacion-permisos

const funcionario = document.querySelector('[name="funcionario-permisos"]')
const cargo = document.querySelector('[name="cargo-permisos"]')
const grupos = document.querySelector('[name="grupos-permisos"]')
const reportes = document.querySelector('[name="reportes-permisos"]')
const idp = document.querySelector('[name="idp-permisos"]')
const solicitudes = document.querySelector('[name="solicitudes-permisos"]')
const autorizacion = document.querySelector('[name="autorizacion-permisos"]')