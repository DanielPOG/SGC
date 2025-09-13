from core_apps.general.models import Regional, Centro, Red, Area, Dependencia
from core_apps.usuarios_api.models import TipoDocumento, Genero, EstudioFormal, Rol, Estado
from core_apps.cargos_api.models import CargoNombre, EstadoCargo, EstadoVinculacion, Idp
from core_apps.grupoSena_api.models import EstadoGrupo

def run():
    # General
    reg, _ = Regional.objects.get_or_create(codigoRegional="01", nombre="Regional Cauca")
    cen, _ = Centro.objects.get_or_create(codigoCentro="001", nombre="Centro de Desarrollo", regional=reg)
    red, _ = Red.objects.get_or_create(codigoRed="R01", nombre="Red TIC", centro=cen)
    Area.objects.get_or_create(codigoArea="A01", nombre="Área Software", red=red)
    Dependencia.objects.get_or_create(codigoDependencia="000", nombre="General")

    # Usuarios
    TipoDocumento.objects.get_or_create(sigla="CC", nombre="Cédula")
    Genero.objects.get_or_create(sigla="ND", nombre="No definido")
    EstudioFormal.objects.get_or_create(nombre="No aplica")
    Rol.objects.get_or_create(nombre="ADMIN")
    Estado.objects.get_or_create(nombre="Activo")

    # Cargos
    CargoNombre.objects.get_or_create(nombre="ADMIN")
    EstadoCargo.objects.get_or_create(estado="ACTIVO")
    EstadoVinculacion.objects.get_or_create(estado="Vinculado")
    Idp.objects.get_or_create(idp_id="1001")

    # GrupoSena
    EstadoGrupo.objects.get_or_create(estado="Activo")
