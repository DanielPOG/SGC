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
    