const newIdpModal = document.querySelector('.new-idp-modal')
const closeBtn = document.querySelector('.close')
function close() {
  if (!newIdpModal.classList.contains('hidden')) newIdpModal.classList.add('hidden')
  else closeBtn.removeEventListener('click', close)
}
closeBtn.addEventListener('click', close)

// Envio del formulario
if (!newIdpModal.classList.contains('hidden')) {
  const form = document.getElementById('crear-nueva-idp')

  form.addEventListener('submit', async (e )=> {
    e.preventDefault()
    try {
      const response = await fetch('http://127.0.0.1:8001/api/cargos/idps/', {
        method: 'POST',
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          numero: form.querySelector('input#numero').value, // Atributo data-numero en tu form
          fechaCreacion: form.querySelector('input#fecha').value  // Atributo data-nombre en tu form
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error en la solicitud:", errorData);
        return;
      }

      const data = await response.json();
      console.log("IDP creado:", data);

    } catch (e) {
      console.error('Sucedió un error al crear el IDP', e);
      return
    } finally {
      form.reset()
    }
  })