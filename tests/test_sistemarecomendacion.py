import pytest
import anyio
from datetime import date

from streaming_musical import (
    SistemaRecomendacion, ServicioStreaming, Sesion, Cancion, 
    Alfabetico, Artista, ListaReproduccion, SesionError
)
@pytest.fixture
def anyio_backend():
    return 'asyncio'

@pytest.fixture(autouse=True)
def reset_singleton():
    """Limpia la instancia del Singleton antes de cada test."""
    SistemaRecomendacion._SistemaRecomendacion__instancia = None

def test_singleton_identidad():
    """Verifica que getInstancia siempre devuelva la misma referencia."""
    s1 = SistemaRecomendacion.getInstancia()
    s2 = SistemaRecomendacion.getInstancia()
    assert s1 is s2
    
    with pytest.raises(SesionError):
        SistemaRecomendacion()

@pytest.mark.anyio
async def test_procesar_cancion_flujo():
    """Prueba el flujo asíncrono de procesamiento de una canción."""
    c1 = Cancion("ID_123", {"r": 0.05}, {"s": 0.05}, "Hit", date.today())
    catalogo = ServicioStreaming([c1], [], [])
    sesion = Sesion([])
    
    sistema = SistemaRecomendacion.getInstancia()
    sistema.setSesion(sesion)
    
    await sistema.procesarCancion("ID_123", date.today(), catalogo)
    
    assert len(sesion.obtenerCanciones()) == 1
    assert sesion.obtenerCanciones()[0] == c1

def test_recomendar_con_decorador_artista():
    """Verifica que el sistema devuelva un Artista."""
    c1 = Cancion("ID1", {"r": 0.05}, {"s": 0.05}, "CancionA", date.today())
    # El constructor de Artista recibe el nombre como primer parámetro
    nombre_artista = "Nombre Artista"
    artista = Artista(nombre_artista, [c1], date(1990, 1, 1))
    catalogo = ServicioStreaming([c1], [artista], [])
    
    sistema = SistemaRecomendacion.getInstancia()
    sistema.setSesion(Sesion([]))
    sistema.setEstrategia(Alfabetico())
    sistema.setTipoRecomendacion(Artista)
    
    resultado = sistema.recomendar(catalogo)
    
    assert isinstance(resultado, Artista)
    assert resultado._Artista__nombre == nombre_artista

def test_errores_configuracion_incompleta():
    """Verifica que se lance SesionError si faltan configuraciones."""
    sistema = SistemaRecomendacion.getInstancia()
    catalogo = ServicioStreaming([], [], [])
    
    with pytest.raises(SesionError):
        sistema.recomendar(catalogo)

def test_procesar_cancion_no_encontrada():
    """Verifica que se lance ValueError si el ID no existe en el catálogo."""
    catalogo = ServicioStreaming([], [], [])
    sistema = SistemaRecomendacion.getInstancia()
    sistema.setSesion(Sesion([]))
    
    with pytest.raises(ValueError):
        anyio.run(sistema.procesarCancion, "ID_FALSO", date.today(), catalogo)