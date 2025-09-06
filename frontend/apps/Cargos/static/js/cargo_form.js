
document.addEventListener("DOMContentLoaded", async () => {
    const form = document.getElementById("cargoForm");
    const mode = form.dataset.mode;   // "create" o "edit"
    const cargoId = form.dataset.id;  // solo existe en edit

    // 🔹 Cargar selects
    async function cargarSelect(url, selectId, labelField="nombre") {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">-- Selecciona --</option>';
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error("Error en la API");
            const data = await response.json();
            data.forEach(item => {
                const option = document.createElement("option");
                option.value = item.id;
                option.textContent = item[labelField];
                select.appendChild(option);
            });
        } catch (err) {
            console.error("⚠️ Error cargando " + selectId, err);
        }
    }

    await cargarSelect("http://127.0.0.1:8001/api/cargos/cargo-nombres/", "cargoNombre", "nombre");
    await cargarSelect("http://127.0.0.1:8001/api/cargos/idps/", "idp", "idp_id");
    await cargarSelect("http://127.0.0.1:8001/api/cargos/estado-cargo/", "estadoCargo", "estado");
    await cargarSelect("http://127.0.0.1:8001/api/general/centros/", "centro", "nombre");

    // 🔹 Si estamos en modo EDITAR → precargar datos
    if (mode === "edit" && cargoId) {
        try {
            const resp = await fetch(`http://127.0.0.1:8001/api/cargos/cargos/${cargoId}/`);
            if (!resp.ok) throw new Error("No se pudo obtener el cargo");
            const data = await resp.json();

            document.getElementById("cargoNombre").value = data.cargoNombre.id;
            document.getElementById("idp").value = data.idp.idp_id;
            document.getElementById("estadoCargo").value = data.estadoCargo.id;
            document.getElementById("centro").value = data.centro.id;
            document.getElementById("resolucion_numero").value = data.resolucion;
            document.getElementById("observacion").value = data.observacion;

            // 👇 Mostrar link al archivo si ya existe
            if (data.resolucion_archivo) {
                const archivoDiv = document.getElementById("archivoActual");
                if (archivoDiv) {
                    archivoDiv.innerHTML = `
                        <p class="text-sm text-gray-700">
                            Archivo actual: 
                            <a href="${data.resolucion_archivo}" 
                            target="_blank" 
                            class="text-blue-600 underline">
                            Ver archivo
                            </a>
                        </p>
                    `;
                }
            }


        } catch (err) {
            console.error("❌ Error precargando datos:", err);
        }
    }


    // Validación simple
    function validarFormulario() {
    const campos = {
        cargoNombre: "cargo",
        idp: "ID",
        estadoCargo: "estado",
        centro: "centro",
        resolucion_numero: "resolución",
        resolucion_archivo: "archivo de resolución"
    };
    
    // Recorremos y validamos
    for (let id in campos) {
        const valor = document.getElementById(id).value;
        if (!valor) {
        Swal.fire({
            icon: "error", // Tipo de alerta: 'success', 'error', 'warning', 'info', 'question'
            title: "❌ Oops...", 
            text: `Por favor selecciona o ingresa: ${campos[id]}`, // Mensaje de error
            confirmButtonText: "Entendido",
            confirmButtonColor: "#d33", // Estilo del botón
            customClass: { // Clases personalizadas para estilos
            popup: "custom-popup",
            title: "custom-title",
            content: "custom-text"
            },
            showClass: {
            popup: "animate__animated animate__bounceIn" // Animación de entrada
            },
            hideClass: {
            popup: "animate__animated animate__bounceOut" // Animación de salida
            }
        });
        return false;
        }
    }
    return true;
    }



// 🔹 Submit → POST o PUT
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!validarFormulario()) return;

    const formData = new FormData();
    formData.append("cargoNombre", document.getElementById("cargoNombre").value);
    formData.append("idp", document.getElementById("idp").value);
    formData.append("estadoCargo", document.getElementById("estadoCargo").value);
    formData.append("centro", document.getElementById("centro").value);
    formData.append("resolucion", document.getElementById("resolucion_numero").value);

    const archivo = document.getElementById("resolucion_archivo").files[0];
    if (archivo) formData.append("resolucion_archivo", archivo);

    formData.append("observacion", document.getElementById("observacion").value);

    let url = "http://127.0.0.1:8001/api/cargos/cargos/";
    let method = "POST";

    if (mode === "edit" && cargoId) {
        url = `http://127.0.0.1:8001/api/cargos/cargos/${cargoId}/`;
        method = "PUT";
    }

    try {
        const response = await fetch(url, { method, body: formData });
        const body = await response.json();

        if (!response.ok) {
            console.error("❌ Errores del backend:", body);
            alert("❌ Error guardando cargo, revisa la consola");
            return;
        }

    // Redirigimos con query param que Django usará para mostrar el mensaje
    if (mode === "edit") {
        window.location.href = "/cargos/cargos/index?updated=1";
    } else {
        window.location.href = "/cargos/cargos/index?created=1";
    }

    } catch (err) {
        console.error("❌ Error:", err.message);
        alert("❌ Error guardando cargo");
    }
});


});
