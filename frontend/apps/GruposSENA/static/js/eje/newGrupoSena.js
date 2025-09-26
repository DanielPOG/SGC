document.addEventListener("DOMContentLoaded", async () => {

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
                if (selectId === "lider") {
                    option.textContent = `${item.nombre} ${item.apellido}`;
                } else {
                    option.textContent = labelField ? item[labelField] : item.nombre;
                }
                select.appendChild(option);
            });

        } catch (err) {
            console.error(`Error cargando ${selectId}:`, err);
            select.innerHTML = '<option value="">Error cargando datos</option>';
        }
    }

    // 🔹 Función para formatear fecha a "yyyy-MM-dd" (para input type="date")
    function formatearFechaParaInput(fecha) {
        if (!fecha) return '';
        // Si viene en formato dd/MM/yyyy
        if (fecha.includes('/')) {
            const [dia, mes, anio] = fecha.split('/');
            return `${anio}-${mes}-${dia}`;
        }
        // Si viene en ISO o yyyy-MM-dd
        return fecha.split('T')[0]; // elimina hora si viene en ISO
    }

    // 🔹 Función para obtener fecha de hoy en formato yyyy-MM-dd usando hora local
    function fechaHoyLocal() {
        const hoy = new Date();
        const dia = String(hoy.getDate()).padStart(2, "0");
        const mes = String(hoy.getMonth() + 1).padStart(2, "0");
        const anio = hoy.getFullYear();
        return `${anio}-${mes}-${dia}`;
    }

    // 🔹 Inicializar selects
    await cargarSelect("http://127.0.0.1:8001/api/general/areas/", "area", "nombre");
    await cargarSelect("http://127.0.0.1:8001/api/usuarios/usuarios/", "lider", null);
    await cargarSelect("http://127.0.0.1:8001/api/gruposena/nombre-grupo/", "nombre", "nombre");
    await cargarSelect("http://127.0.0.1:8001/api/gruposena/estado-grupo/", "estado", "estado");

    const fechaInput = document.getElementById("fecha_creacion");

    // 🔹 Detectar si estamos en modo "editar" o "crear"
    const grupoForm = document.getElementById("grupoForm");
    const modo = grupoForm.dataset.mode || "create"; // create / edit
    const grupoId = grupoForm.dataset.id; // solo para editar

    if (modo === "edit" && grupoId) {
        // 🔹 Cargar datos del grupo desde backend
        try {
            const res = await fetch(`http://127.0.0.1:8001/api/gruposena/grupo-sena/${grupoId}/`);
            if (!res.ok) throw new Error("Error cargando datos del grupo");

            const grupo = await res.json();

            // Asignar valores a los inputs
            document.getElementById("nombre").value = grupo.nombre || '';
            document.getElementById("area").value = grupo.area || '';
            document.getElementById("lider").value = grupo.lider || '';
            document.getElementById("estado").value = grupo.estado || '';

            if (fechaInput) {
                fechaInput.value = formatearFechaParaInput(grupo.fecha_creacion);
            }

        } catch (err) {
            console.error("❌ Error cargando grupo:", err);
            alert("Error cargando datos del grupo, revisa la consola");
        }
    } else {
        // Crear: poner fecha de hoy
        if (fechaInput) {
            fechaInput.value = fechaHoyLocal();
        }
    }

    // 🔹 Validación simple
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
            const url = modo === "edit"
                ? `http://127.0.0.1:8001/api/gruposena/${grupoId}/`
                : "http://127.0.0.1:8001/api/gruposena/";


            const method = modo === "edit" ? "PUT" : "POST";

            const response = await fetch(url, {
                method: method,
                body: formData
            });

            let body;
            try {
                body = await response.json();
            } catch {
                const textBody = await response.text();
                console.error("❌ Respuesta no es JSON:", textBody);
                alert("❌ Error en el servidor, revisa la consola");
                return;
            }

            if (!response.ok) {
                console.error("❌ Error backend:", body);
                alert("❌ Error creando/actualizando grupo, revisa la consola");
                return;
            }

            alert(modo === "edit" ? "✅ Grupo actualizado con éxito" : "✅ Grupo creado con éxito");
            grupoForm.reset();

            // 🔹 Reiniciar selects
            ["area", "lider", "nombre", "estado"].forEach(id => {
                document.getElementById(id).innerHTML = '<option value="">-- Selecciona --</option>';
            });

            // 🔹 Recargar selects
            await cargarSelect("http://127.0.0.1:8001/api/general/areas/", "area", "nombre");
            await cargarSelect("http://127.0.0.1:8001/api/usuarios/usuarios/", "lider", null);
            await cargarSelect("http://127.0.0.1:8001/api/gruposena/nombre-grupo/", "nombre", "nombre");
            await cargarSelect("http://127.0.0.1:8001/api/gruposena/estado-grupo/", "estado", "estado");

            // 🔹 Volver a poner fecha
            if (fechaInput) {
                fechaInput.value = fechaHoyLocal();
            }

        } catch (err) {
            console.error("❌ Error creando/actualizando grupo:", err);
            alert("❌ Error en el servidor, revisa la consola");
        }
    });

});
