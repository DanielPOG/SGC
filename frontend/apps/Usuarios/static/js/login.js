document.addEventListener('DOMContentLoaded', async () => {
    // Función para mostrar alertas o mensajes
    const responseNode = document.getElementById('response-node');
    const paragraphNode = document.querySelector('#response-node p');
    const closeResponseNode = document.querySelector('#response-node button');

    window.Response = ({ text, valid }) => {
        if (!responseNode || !paragraphNode) return;
        responseNode.style.display = 'flex';
        paragraphNode.innerText = text;
        if (valid) closeResponseNode?.style?.setProperty('display', 'none');
        else closeResponseNode?.addEventListener('click', () => {
            responseNode.style.display = 'none';
            paragraphNode.innerText = '';
        });
    };

    // ----------------------
    // Login
    // ----------------------
    const formNode = document.getElementById('login-form');
    if (formNode) {
        formNode.addEventListener('submit', async e => {
            e.preventDefault();

            const correo = formNode.usuario.value.trim();
            const password = formNode.password.value.trim();

            if (!correo || !password) {
                Response({ text: 'Todos los campos son obligatorios', valid: false });
                return;
            }

            try {
                console.log("Intentando login con:", { correo, password });

                const res = await fetch("http://127.0.0.1:8001/api/usuarios/login/", {
                    method: 'POST',
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ correo, password })
                });

                const data = await res.json();
                console.log("Respuesta de la API:", data);

                if (!res.ok) {
                    Response({ text: data.detail || "Credenciales inválidas", valid: false });
                    return;
                }

                // Guardar JWT y datos del usuario en localStorage
                const userInfo = {
                    correo: correo,
                    nombre: data.nombre,
                    rol: data.rol,
                    user_id: data.user_id
                };
                localStorage.setItem('user', JSON.stringify(userInfo));
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);

                console.log("Login exitoso. Usuario:", userInfo);
                Response({ text: 'Sesión iniciada correctamente', valid: true });

                setTimeout(() => {
                    window.location.href = "../principal"; // Redirigir a principal
                }, 800);

            } catch (error) {
                console.error("Error en fetch/login:", error);
                Response({ text: 'Error al iniciar sesión', valid: false });
            }
        });
    }

    // ----------------------
    // Mostrar usuario en principal
    // ----------------------
    if (window.location.pathname.includes('principal')) {
        const userData = localStorage.getItem('user');
        if (!userData) {
            console.log("No hay usuario logueado. Redirigiendo a login...");
            window.location.href = "/login.html";
        } else {
            const user = JSON.parse(userData);
            console.log("Usuario actual en principal:", user);

            // Ejemplo: mostrar en pantalla si tienes un elemento con id 'usuario-nombre'
            const nombreNode = document.getElementById('usuario-nombre');
            if (nombreNode) nombreNode.innerText = user.nombre;
        }
    }




});
