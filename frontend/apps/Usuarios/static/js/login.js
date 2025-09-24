
document.addEventListener('DOMContentLoaded', ()=>{

    // Validacion: Comprueba si ya hay una sesión iniciada
    checkSessions()    

    const inputMailNode = document.getElementById('usuario')
    const formNode = document.getElementById('login-form')

    console.log('Nodes loaded')

    formNode.addEventListener('submit', async e =>{
        e.preventDefault()
        try {
            const correo = formNode.usuario.value
            const password = formNode.password.value
            if(!correo || !password){
                LResponse({text:'Todos los campos son obligatorios', valid:false})
                return
            }
            const res = await fetch("http://127.0.0.1:8001/api/usuarios/login/", {
                method:'POST', 
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({correo, password})
            })
            const data = await res.json()
            if(data.detail){
                LResponse({text:'Credenciales inválidas', valid:false})
                return
            }
            console.log("Respuesta del servidor:", data)
           
            await LResponse({text:'Sesión iniciada correctamente', valid:true})
            localStorage.setItem('access', data.access)
            localStorage.setItem('refresh', data.refresh)
            localStorage.setItem('user', correo)
            formNode.reset()
        }catch(e){
            console.warn(`Hubo un error al procesar el formulario ${e}`)
            LResponse({text:'Credenciales inválidas', valid:false})
        }
    })

    
    const recoverResponse = {text:'', valid:false}
    // Reset recoverResponse al escribir en el input
    inputMailNode.addEventListener('input', ()=> window.setRecoverResponse(recoverResponse, '', false))
    // Olvidé mi contraseña
    document.getElementById('olvideContraseña').addEventListener('click', async e => {
        window.setRecoverResponse(recoverResponse, '', undefined)
        if(e.target !== e.currentTarget) return
        const textOn = inputMailNode.value.trim()

        // ¿Texto vacío?
        if(textOn.length === 0 || textOn === ''){
            window.setRecoverResponse(recoverResponse, 'Ingrese su correo para la recuperación', false)
            return
        }

        // ¿La dirección es valida?
        if(!textOn.includes("@") || textOn.split('@').length !== 2){
            window.setRecoverResponse(recoverResponse, "Ingrese una dirección de correo válida", false)
            return
        }
        // ¿Es un correo institucional?
        if(textOn.split('@')[1] !== 'soy.sena.edu.co'){ 
            window.setRecoverResponse(recoverResponse, "Correo sena requerido para recuperación", false)
            return
        }
        try{    
            const res = await fetch('api/usuarios/pw-reset/', {
                method:'POST',
                headers:{
                    "Content-Type":'application/json'
                },
                body:JSON.stringify({email:textOn})
            })
            const data = await res.json()
            if(data.error){
                window.setRecoverResponse(recoverResponse, res.error, false)
                return
            }
            window.setRecoverResponse(recoverResponse, 'Enviando correo de recuperación..')
            setTimeout(()=>window.setRecoverResponse(res.msg), 1000)
        }catch(err){
            console.error(`Error al comprobar el correo institucional: ${err}`)
            window.setRecoverResponse(recoverResponse, 'No se pudo enviar correo de recuperación...', false)
        }
    })
})