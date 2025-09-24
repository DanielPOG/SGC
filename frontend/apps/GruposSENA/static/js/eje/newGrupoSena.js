document.addEventListener("DOMContentLoaded", () => {

    // 🔹 Toggle del textarea de observación
    function toggleTextarea() {
        document.getElementById("textarea-observacion").classList.toggle("hidden");
    }
    window.toggleTextarea = toggleTextarea;

    // 🔹 Función para cargar selects dinámicamente (sin Select2)
    async function cargarSelect(url, selectId, labelField = null) {
        const select = document.getElementById(selectId);
        select.innerHTML = '<option value="">Cargando...</option>';

        try {
           const response = await fetch(url);
            if (!response.ok) throw new Error(`Error ${response.status}`);

            const data = await response.json();
            if (!data.length) {
                select.innerHTML = '<option value="">No hay datos disponibles</option>';
                return;
            }

            select.innerHTML = '<option value="">-- Selecciona --</option>';

            data.forEach(item => {
                const option = document.createElement("option");
                option.value = item.id;
                option.textContent = labelField ? item[labelField] : item.nombre;
                select.appendChild(option);
            });

        } catch (err) {
            console.error(`Error cargando ${selectId}:`, err);
            select.innerHTML = '<option value="">Error cargando datos</option>';
        }
    }

    // 🔹 Inicializar selects al cargar la página
    cargarSelect("http://127.0.0.1:8001/api/general/areas/", "area", "nombre");
    cargarSelect("http://127.0.0.1:8001/api/usuarios/usuarios/", "lider", null);
    cargarSelect("http://127.0.0.1:8001/api/gruposena/nombre-grupo/", "nombre", "nombre");
    cargarSelect("http://127.0.0.1:8001/api/gruposena/estado-grupo/", "estado", "estado");

    // 🔹 Formulario y validación
    const grupoForm = document.getElementById("grupoForm");
    function validarFormulario() {
        const campos = ["nombre", "area", "lider", "estado"];
        for (let id of campos) {
            const valor = document.getElementById(id).value;
            if (!valor) {
                alert(`❌ Por favor completa o selecciona: ${id}`);
                return false;
            }
        }
        return true;
    }

    // 🔹 Envío del formulario
    grupoForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        if (!validarFormulario()) return;

        const formData = new FormData(grupoForm);

        try {
            const response = await fetch("http://127.0.0.1:8001/api/gruposena/grupo-sena/", {
                method: "POST",
                body: formData
            });

            let body;
            try {
                body = await response.json();
            } catch {
                const textBody = await response.text();
                console.error("❌ Respuesta no es JSON:", textBody);
                alert("❌ Error creando grupo, revisa la consola");
                return;
            }

            if (!response.ok) {
                console.error("❌ Error backend:", body);
                alert("❌ Error creando grupo, revisa la consola");
                return;
            }

            alert("✅ Grupo SENA creado con éxito");
            grupoForm.reset();

            // 🔹 Reiniciar selects
            ["area", "lider", "nombre", "estado"].forEach(id => {
                document.getElementById(id).innerHTML = '<option value="">-- Selecciona --</option>';
            });

            // 🔹 Recargar selects
            cargarSelect("http://127.0.0.1:8001/api/general/areas/", "area", "nombre");
            cargarSelect("http://127.0.0.1:8001/api/usuarios/usuarios/", "lider", null);
            cargarSelect("http://127.0.0.1:8001/api/gruposena/nombre-grupo/", "nombre", "nombre");
            cargarSelect("http://127.0.0.1:8001/api/gruposena/estado-grupo/", "estado", "estado");

        } catch (err) {
            console.error("❌ Error creando grupo:", err);
            alert("❌ Error creando grupo, revisa la consola");
        }
    });

});
