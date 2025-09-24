const formNode = document.getElementById('login-form')

formNode.addEventListener('submit', async e => {
    e.preventDefault()
    const correo = formNode.usuario.value
    const password = formNode.password.value

    if (!correo || !password) {
        Response({text:'Todos los campos son obligatorios', valid:false})
        return
    }

    try {
        const res = await fetch("http://127.0.0.1:8001/api/usuarios/login/", {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ correo, password })
        })

        const data = await res.json()

        if (!res.ok) {
            Response({text: data.detail || "Credenciales inválidas", valid:false})
            return
        }

        localStorage.setItem('access', data.access)
        localStorage.setItem('refresh', data.refresh)
        localStorage.setItem('user', correo)

        Response({text:'Sesión iniciada correctamente', valid:true})

    } catch (error) {
        console.error(error)
        Response({text:'Error al iniciar sesión', valid:false})
    }
})
