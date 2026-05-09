import pytest

from streaming_musical import EstrategiaBusqueda, ServicioStreaming, Sesion

# Implementación concreta para el test
class EstrategiaPrueba(EstrategiaBusqueda):
    def buscar(self, catalogo: ServicioStreaming, sesion: Sesion):
        super().buscar(catalogo, sesion)
        return "Busqueda ejecutada"

def test_instanciacion_clase_abstracta():
    """Verifica que no se puede instanciar la clase abstracta directamente."""
    with pytest.raises(TypeError):
        EstrategiaBusqueda()

def test_validacion_tipos_buscar():
    """Verifica la validación de tipos."""
    estrategia = EstrategiaPrueba()
    catalogo_valido = ServicioStreaming([], [], [])
    sesion_valida = Sesion([])

    assert estrategia.buscar(catalogo_valido, sesion_valida) == "Busqueda ejecutada"

    # Verificar que las validaciones internas de la clase base funcionan
    with pytest.raises(TypeError):
        estrategia.buscar("No catalogo", sesion_valida)