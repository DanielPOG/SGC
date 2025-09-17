from django.shortcuts import render

SOLICITUDES = [
    {"id": 1, "titulo": "Cambio de carrera", "estado": "pendiente", "fecha": "2025-04-10", "ver_detalle": "Ver"},
    {"id": 2, "titulo": "Solicitud beca", "estado": "aprobada", "fecha": "2025-04-12", "ver_detalle": "Ver", "fecha_aprobacion": "2025-04-15"},
    {"id": 3, "titulo": "Certificado", "estado": "pendiente", "fecha": "2025-04-13", "ver_detalle": "Ver"},
]

def estado_solicitud(request):
    estado = request.GET.get("estado")  

    if estado:
        solicitudes_filtradas = [s for s in SOLICITUDES if s["estado"] == estado]
    else:
        solicitudes_filtradas = SOLICITUDES  

    return render(request, "layout/estado_solicitud.html", {
        "solicitudes": solicitudes_filtradas,
        "estado_actual": estado,
    })


# Otras vistas básicas
def solicitudes(request):
    return render(request, 'layout/solicitudes.html')

def todas_solicitudes(request):
    return render(request, 'pages/todas_solicitudes.html', {"solicitudes": SOLICITUDES})


def solicitud_pendiente(request, id):
    solicitud = next((s for s in SOLICITUDES if s["id"] == id), None)
    return render(request, "pages/solicitud_pendiente.html", {"solicitud": solicitud})

def solicitud_revicion(request, id):
    solicitud = next((s for s in SOLICITUDES if s["id"] == id), None)
    return render(request, "pages/solicitud_revicion.html", {"solicitud": solicitud})

def solicitud_aprovada(request, id):
    solicitud = next((s for s in SOLICITUDES if s["id"] == id), None)
    return render(request, "pages/solicitud_aprovada.html", {"solicitud": solicitud})
