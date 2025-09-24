// Nodos para insertar respuestas
    const responseNode = document.getElementById('response-node')
    const paragraphNode = document.querySelector('#response-node p')
    const closeResponseNode = document.querySelector('#response-node button')

    
    // Validacion: Comprueba si ya hay una sesión iniciada
window.checkSessions = ()=>{
    const access = localStorage.getItem("access")
    const refresh = localStorage.getItem("refresh")

    if (access || refresh) {
        window.location.href = "http://127.0.0.1:8000/principal"
    }
}

    // Creación de un state para loginResponse
window.Response = async(newVal)=>{
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

window.setRecoverResponse = (recoverResponse ,text, valid)=>{

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
    