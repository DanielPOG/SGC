FRONTEND

# Entrar a la carpeta frontend
    # Crear entorno virtual (Solo una vez en local )
        python -m venv venv
        venv\Scripts\activate      #SIEMPRE UTILIZAR 
    # Descargar dependencias
    pip install django

BACKEND 

# Entrar a la carpeta backend
    # Crear entorno virtual (Solo una vez en local )
        python -m venv venv
        venv\Scripts\activate      #SIEMPRE UTILIZAR 

    # Descargar dependencias
    pip install django djangorestframework (logica)
    pip install psycopg2-binary (para desarrollo) (Base de datos) CAMBIAR EN PRODUCCION A  psycopg2
    pip install django-cors-headers (para autorizaciones de los navegadores)
    pip install coreapi (para documentacion automatica hacer para cada app, hacerla para cada una)
    pip install setuptools (para que maneje los package)
