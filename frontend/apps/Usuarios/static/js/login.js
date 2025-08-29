document.addEventListener('DOMContentLoaded', ()=>{

    const responseNode = document.getElementById('olvideContraseñaResponse')
    const inputMailNode = document.getElementById('usuario')

    console.log('Nodes loaded')

    // Creación de un state para el texto dinámico
    const response = {text:'', valid:false}
    const setResponse = (text, valid)=>{
        if(typeof text !== 'string') return
        response.text = text
        response.valid = valid
        responseNode.innerText = response.text
    }
    
    // Reset response al escribir en el input
    inputMailNode
        .addEventListener('input', ()=> setResponse('', false))


    document.getElementById('olvideContraseña').addEventListener('click', e => {
        setResponse('')
        if(e.target !== e.currentTarget) return
        const textOn = inputMailNode.value.trim()

        // ¿Texto vacío?
        if(textOn.length === 0 || textOn === ''){
            setResponse('Ingrese su correo para la recuperación', false)
            return
        }

        // ¿La dirección es valida?
        if(!textOn.includes("@") || textOn.split('@').length !== 2){
            setResponse("Ingrese una dirección de correo válida", false)
            return
        }

        // ¿Es un correo institucional?
        if(textOn.split('@')[1] !== 'soy.sena.edu.co'){ 
            setResponse("Correo sena requerido para recuperación", false)
            return
        }

        try{
            const {data} = fetch('api/usuarios/mail-check')
            setResponse('Enviando correo de recuperación...', true)
        }catch(err){
            console.error(`Error al comprobar el correo institucional: ${err}`)
            setResponse('No se pudo enviar correo de recuperación...', false)
        }
    })
})