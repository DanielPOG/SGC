document.addEventListener('DOMContentLoaded', ()=>{

    const inputMailNode = document.getElementById('usuario')
    const formNode = document.getElementById('login-form')
    
    // Nodos para insertar respuestas
    const recoverResponseNode = document.getElementById('olvideContraseñaResponse')
    const responseNode = document.getElementById('response-node')
    const paragraphNode = document.querySelector('#response-node p')
    const closeResponseNode = document.querySelector('#response-node button')

    console.log('Nodes loaded')

    // Creación de un state para loginResponse
    const LResponse = async(newVal)=>{
        responseNode.style.display = 'flex'
        paragraphNode.innerText = newVal.text
        if(newVal.valid){
            closeResponseNode.style.display = 'none'
            setTimeout(()=>location.href = '../principal', 800)
            return
        }
        const handleClose = ()=>{
            responseNode.style.display = 'none'
            paragraphNode.innerText = ''
            closeResponseNode.removeEventListener('click', handleClose)            
        }
        closeResponseNode.addEventListener('click', handleClose)
    }
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
            formNode.reset()
        }catch(e){
            console.warn(`Hubo un error al procesar el formulario ${e}`)
            LResponse({text:'Credenciales inválidas', valid:false})
        }
    })



    // Creación de un state para recoverResponse de contraseña debajo del input usuario 
    const recoverResponse = {text:'', valid:false}
    const setRecoverResponse = (text, valid)=>{
        if(typeof text !== 'string' || typeof valid !== 'boolean'){
            console.error(`
                Error setLoginResponse: El tipo de dato de uno o ambos parametros
                es incorrecto
                `)
            return
        }
        recoverResponse.text = text
        recoverResponse.valid = valid
        recoverResponseNode.innerText = recoverResponse.text
    }
    
    // Reset recoverResponse al escribir en el input
    inputMailNode
        .addEventListener('input', ()=> setRecoverResponse('', false))

    // Olvidé mi contraseña
    document.getElementById('olvideContraseña').addEventListener('click', async e => {
        setRecoverResponse('')
        if(e.target !== e.currentTarget) return
        const textOn = inputMailNode.value.trim()

        // ¿Texto vacío?
        if(textOn.length === 0 || textOn === ''){
            setRecoverResponse('Ingrese su correo para la recuperación', false)
            return
        }

        // ¿La dirección es valida?
        if(!textOn.includes("@") || textOn.split('@').length !== 2){
            setRecoverResponse("Ingrese una dirección de correo válida", false)
            return
        }
        // ¿Es un correo institucional?
        if(textOn.split('@')[1] !== 'soy.sena.edu.co'){ 
            setRecoverResponse("Correo sena requerido para recuperación", false)
            return
        }
        try{    
            const res = await fetch('api/usuarios/pw-reset/', {
                method:'POST',
                headers:{
                    "Content-Type":'application/json',
                    //"X-CSRFToken":
                },
                body:JSON.stringify({email:textOn})
            })
            const data = await res.json()
            if(data.error){
                setRecoverResponse(res.error, false)
                return
            }
            setRecoverResponse('Enviando correo de recuperación..')
            setTimeout(()=>setRecoverResponse(res.msg), 1000)
        }catch(err){
            console.error(`Error al comprobar el correo institucional: ${err}`)
            setRecoverResponse('No se pudo enviar correo de recuperación...', false)
        }
    })
})