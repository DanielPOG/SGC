document.addEventListener('DOMContentLoaded',()=>{
    const newIdpModal = document.querySelector('.new-idp-modal')
    const closeBtn = document.querySelector('.close')
    function close() {
        
        if (!newIdpModal.classList.contains('hidden')) {
            newIdpModal.classList.add('hidden') 
            document.body.style.overflow = "auto";
        }
        else closeBtn.removeEventListener('click', close)
    }
    closeBtn.addEventListener('click', close)

    // Envio del formulario
        const form = document.getElementById('crear-nueva-idp')
        const newIdpRes = document.getElementById('new-idp-response')
        form.addEventListener('submit', async e => {
            e.preventDefault()
            
                const numero = form.querySelector('#numero-new')?.value.trim()
                const fecha = form.querySelector('#fecha')?.value.trim()

                if (!numero || !fecha) {
                    newIdpRes.innerText = 'Debes llenar todos los campos'
                    newIdpRes.classList.add('bg-red-600')
                    return
                }
            try {
                const response = await fetch('http://127.0.0.1:8001/api/cargos/idps/', {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        idp_id: numero, 
                        fechaCreacion: fecha  
                    })
                });

                if (!response.ok) {
                    newIdpRes.innerText = 'No se pudo crear la IDP'
                    newIdpRes.classList.add('bg-red-600')
                    const errorData = await response.json();
                    console.error("Error en la solicitud:", errorData);
                    return;
                }

                const data = await response.json();
                newIdpRes.innerText = 'IDP Creado correctamente'
                newIdpRes.classList.add('bg-green-600')
                console.log("IDP creado:", data);
                
                

            } catch (e) {
                console.error('Sucedió un error al crear el IDP', e);
                return
            } finally {
                form.reset()
                setTimeout(()=>{
                    close()
                    newIdpRes.innerText = ''
                    newIdpRes.classList.remove('bg-green-600')
                    newIdpRes.classList.remove('bg-red-600')
                }, 2000)
            }
    })
})