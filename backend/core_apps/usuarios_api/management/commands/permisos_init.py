from django.core.management.base import BaseCommand
from core_apps.usuarios_api.models import Autorizacion, Permiso

class Command(BaseCommand):
    help = 'Carga las autorizaciones y permisos iniciales.'

    def handle(self, *args, **kwargs):
        datos = {
            "Funcionario": [
                ("Agregar Funcionario", "funcionario_agregar"),
                ("Historiales", "funcionario_historiales"),
                ("Añadir Formación", "funcionario_formacion"),
                ("Consultar Datos", "funcionario_consultar"),
                ("Cargar Excel", "funcionario_excel"),
                ("Editar Funcionario", "funcionario_editar"),
            ],
            "Cargo": [
                ("Agregar Cargo", "cargo_agregar"),
                ("Historiales", "cargo_historiales"),
                ("Añadir Funcionario", "cargo_añadir_funcionario"),
                ("Cargar Excel", "cargo_excel"),
                ("Consultar Datos", "cargo_consultar"),
                ("Editar Cargo", "cargo_editar"),
            ],
            "Grupo SENA": [
                ("Agregar Grupo", "grupo_agregar"),
                ("Consultar Datos", "grupo_consultar"),
                ("Cargar Excel", "grupo_excel"),
                ("Historial", "grupo_historial"),
                ("Añadir Funcionario", "grupo_añadir_funcionario"),
                ("Editar Grupo", "grupo_editar"),
            ],
            "Reportes": [
                ("Generar Reporte", "reportes_generar"),
                ("Descargar Reporte", "reportes_descargar"),
            ],
            "ID Planta": [
                ("Registrar IDP", "idplanta_registrar"),
                ("Cargar Excel", "idplanta_excel"),
                ("Asignar", "idplanta_asignar"),
                ("Consultar Datos", "idplanta_consultar"),
                ("Editar IDP", "idplanta_editar"),
            ],
            "Solicitudes": [
                ("Consultar Solicitudes", "solicitudes_consultar"),
                ("Solicitudes Pendientes", "solicitudes_pendientes"),
                ("Solicitudes En Revisión", "solicitudes_revision"),
                ("Solicitudes Aprobadas", "solicitudes_aprobadas"),
                ("Revisar Solicitud", "solicitudes_revisar"),
            ],
            "Autorizaciones": [
                ("Consultar Datos", "autorizaciones_consultar"),
                ("Aprobar", "autorizaciones_aprobar"),
                ("Rechazar", "autorizaciones_rechazar"),
            ],
        }

        for nombre_autorizacion, permisos in datos.items():
            autorizacion, _ = Autorizacion.objects.get_or_create(nombre=nombre_autorizacion)
            for nombre_permiso, codigo in permisos:
                Permiso.objects.get_or_create(
                    autorizacion=autorizacion,
                    nombre=nombre_permiso,
                    codigo=codigo
                )
        self.stdout.write(self.style.SUCCESS("✅ Permismos cargados correctamente."))
