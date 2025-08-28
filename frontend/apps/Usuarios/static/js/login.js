document.addEventListener('DOMContentLoaded', ()=>{

    const responseNode = document.getElementById('olvideContraseñaResponse')
    const inputMailNode = document.getElementById('usuario')

    console.log('Nodes loaded')

    // Creación de un state para el texto dinámico
    const response = {text:''}
    const setResponse = (text)=>{
        if(typeof text !== 'string') return
        response.text = text
        responseNode.innerText = response.text
    }
    
    inputMailNode
        .addEventListener('input', ()=> setResponse(''))

    document.getElementById('olvideContraseña').addEventListener('click', e => {
        setResponse('')
        if(e.target !== e.currentTarget) return
        const textOn = inputMailNode.value.trim()
        // ¿Texto vacío?
        if(textOn.length === 0){
            setResponse('Ingrese su correo para la recuperación')
            return
        }
        // ¿La dirección es valida?
        if(!textOn.includes("@") || textOn.split('@').length !== 2){
            setResponse("Ingrese una dirección de correo válida")
            return
        }
        // ¿Es un correo institucional?
        if(textOn.split('@')[1] !== 'soy.sena.edu.co'){ 
            setResponse("Correo sena requerido para recuperación")
        }
    })
})