// fetchUsers


const loadUsersRows = (users)=>{
    console.log(users)
    const tbody = document.querySelector('table tbody')
    users.map(user=>{
      const $row = (`<tr class="hover:bg-gray-100">
      <td class="px-4 py-2 border text-center">${user.nombre} ${user.apellido}</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${user.num_doc ? user.num_doc:'No definido'}</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${user.cargo.cargoNombre.nombre}</td>
      <td class="px-4 py-2 border text-center">${user.estado.nombre}</td>
      <td class="px-4 py-2 border text-center hidden md:table-cell">${user.correo}</td>
      <td class="border text-center relative">
        <button  data-user=${user.id} class="w-full h-full bg-white-600 text-black font-semibold py-2 rounded hover:bg-green-300 transition">
          Seleccionar
        </button>
      </td>
    </tr>`)
    tbody.innerHTML = $row.join('') 
    const $permisos = document.querySelector()
  })
}


document.addEventListener('DOMContentLoaded',()=>{
    try {
        apiFetch('http://127.0.0.1:8001/api/usuarios/usuario/cargarUsers', {method:'GET'})
        .then(res=> res.json()).then(data => {
          console.log('Usuarios fetched', data)
          loadUsersRows(data)
          console.log('Usuarios cargados')

        }).catch(e=>{
          console.error('Error adjuntando usuarios ', e)
          return
        })
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