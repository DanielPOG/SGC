

FRONTEND

# Entrar a la carpeta frontend
    # Crear entorno virtual (Solo una vez en local )
        python -m venv venv
        venv\Scripts\activate      #SIEMPRE UTILIZAR 
    # Descargar dependencias
    pip install django
    # Tailwind
    pip install django-tailwind   
    python manage.py tailwind install 
    python manage.py tailwind build   
    SIEMPRE PARA TAILWIND INICIAR CON: (PARA VER LOS CAMBIOS)
    python manage.py tailwind start (y en otra terminal trabajar el runserver)
BACKEND 

## SweetAlert2 (Frontend JS)
    Instalado vía:
    npm install sweetalert2


# Entrar a la carpeta backend

    # Correr el servidor en un puerto diferente al del frontend.
    py manage.py runserver 127.0.0.1:8001 --settings=backend.settings

    # Crear entorno virtual (Solo una vez en local )
        python -m venv venv
        venv\Scripts\activate      #SIEMPRE UTILIZAR 

    # Descargar dependencias
    pip install django djangorestframework (logica)
    pip install psycopg2-binary (para desarrollo) (Base de datos) CAMBIAR EN PRODUCCION A  psycopg2
    pip install django-cors-headers (para autorizaciones de los navegadores)
    pip install coreapi (para documentacion automatica hacer para cada app, hacerla para cada una)
    pip install setuptools (para que maneje los package)



    pip install pandas openpyxl (PARA CARGAR POR EXCEL)
