document.addEventListener("DOMContentLoaded", () => {
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


    cargarSelect("http://127.0.0.1:8001/api/cargos/cargo-nombres/", "cargoNombre", "nombre");
    cargarSelect("http://127.0.0.1:8001/api/cargos/idps/", "idp", "numero");
    cargarSelect("http://127.0.0.1:8001/api/cargos/estado-cargo/", "estadoCargo", "estado");
    cargarSelect("http://127.0.0.1:8001/api/general/centros/", "centro", "nombre");


    
    const cargoForm = document.getElementById("cargoForm");

    // Validación simple de campos obligatorios
    function validarFormulario() {
        const campos = ["cargoNombre", "idp", "estadoCargo", "centro", "resolucion_numero"];
        for (let id of campos) {
            const valor = document.getElementById(id).value;
            if (!valor) {
                alert(`❌ Por favor selecciona o ingresa: ${id}`);
                return false;
            }
        }
        return true;
    }

    cargoForm.addEventListener("submit", async (e) => {
        e.preventDefault(); // Evita recarga

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

        try {
            const response = await fetch("http://127.0.0.1:8001/api/cargos/cargos/", {
                method: "POST",
                body: formData
                // NO headers: FormData lo maneja automáticamente
            });

            // Leer cuerpo solo una vez
            const contentType = response.headers.get("content-type");
            let body;
            if (contentType && contentType.includes("application/json")) {
                body = await response.json();
            } else {
                body = await response.text();
            }

            if (!response.ok) {
                console.error("❌ Errores del backend:", body);
                alert("❌ Error creando cargo, revisa la consola para más detalles");
                return;
            }

            alert("✅ Cargo creado con éxito");
            cargoForm.reset(); // Limpia el formulario

        } catch (err) {
            console.error("❌ Error creando cargo:", err.message);
            alert("❌ Error creando cargo, revisa la consola");
        }
    });



});