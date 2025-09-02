from django.shortcuts import render

# Simulación de datos (como si fueran registros de una base de datos)
SOLICITUDES = [
    {"id": "001", "titulo": "Cambio de carrera", "estado": "pendiente", "fecha": "2025-04-10"},
    {"id": "002", "titulo": "Cambio de datos", "estado": "en_revision", "fecha": "2025-04-11"},
    {"id": "003", "titulo": "Solicitud beca", "estado": "aprobada", "fecha": "2025-04-12"},
    {"id": "004", "titulo": "Certificado", "estado": "pendiente", "fecha": "2025-04-13"},
]

# Vista principal que filtra por estado
def estado_solicitud(request):
    estado = request.GET.get("estado")  # Captura el estado desde la URL (GET)
    
    if estado:
        solicitudes_filtradas = [s for s in SOLICITUDES if s["estado"] == estado]
    else:
        solicitudes_filtradas = SOLICITUDES  # Si no hay estado, muestra todas

    # 👇 Debug (puedes eliminarlo después de probar)
    print("Estado actual:", estado)
    print("Solicitudes filtradas:", solicitudes_filtradas)

    return render(request, "layout/estado_solicitud.html", {
        "solicitudes": solicitudes_filtradas,
        "estado_actual": estado,
    })


# Otras vistas básicas (según tu estructura)
def solicitudes(request):
    return render(request, 'layout/solicitudes.html')

def todas_solicitudes(request):
    return render(request, 'pages/todas_solicitudes.html')

def solicitud_pendiente(request):    
    return render(request, 'pages/solicitud_pendiente.html')

def solicitud_revicion(request):
    return render(request, 'pages/solicitud_revicion.html')

def solicitud_aprovada(request):
    return render(request, 'pages/solicitud_aprovada.html')


