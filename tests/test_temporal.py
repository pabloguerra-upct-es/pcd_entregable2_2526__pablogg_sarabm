import pytest
from datetime import date

from streaming_musical import Temporal, ServicioStreaming, Sesion, Cancion, Artista, ListaReproduccion

def test_ordenacion_temporal_mixta():
    """Verifica que el catálogo se ordene de más reciente a más antiguo."""
    # Creamos elementos con diferentes fechas
    c_antigua = Cancion("ID_A", {"r": 0.0}, {"s": 0.0}, "Vieja", date(2020, 1, 1))
    c_nueva = Cancion("ID_N", {"r": 0.0}, {"s": 0.0}, "Nueva", date(2025, 1, 1))
    
    # Artista con fecha intermedia
    artista = Artista("Intermedio", [c_antigua], date(2022, 1, 1))
    
    catalogo = ServicioStreaming([c_antigua, c_nueva], [artista], [])
    sesion = Sesion([]) # Media 0.0, Desviación 0.0
    estrategia = Temporal()
    
    # El primer elemento debería ser la canción de 2025
    resultado = estrategia.buscar(catalogo, sesion)
    assert resultado == c_nueva

def test_filtro_similitud_temporal():
    """Verifica que se descarte un elemento reciente si no es similar a la sesión."""
    # Canción escuchada (Media 0.5)
    c_escuchada = Cancion("ID_E", {"r": 0.5}, {"s": 0.5}, "Escuchada", date.today())
    
    # Canción nueva pero NO similar (ritmo 0.9 != 0.5)
    c_nueva_diferente = Cancion("ID_D", {"r": 0.9}, {"s": 0.9}, "Nueva Dif", date(2026, 1, 1))
    
    # Canción antigua pero similar (ritmo 0.5 == 0.5)
    c_vieja_similar = Cancion("ID_S", {"r": 0.5}, {"s": 0.5}, "Vieja Sim", date(2020, 1, 1))
    
    catalogo = ServicioStreaming([c_nueva_diferente, c_vieja_similar], [], [])
    sesion = Sesion([c_escuchada])
    estrategia = Temporal()
    
    resultado = estrategia.buscar(catalogo, sesion)
    assert resultado == c_vieja_similar

def test_busqueda_artista_y_lista():
    """Verifica que la estrategia pueda devolver Artistas o Listas de Reproducción."""
    c_match = Cancion("ID_M", {"r": 0.0}, {"s": 0.0}, "Match", date.today())
    
    # Lista de reproducción creada hoy
    lista = ListaReproduccion([c_match], "Mi Lista", date.today())
    
    # Canción individual creada ayer
    c_ayer = Cancion("ID_Y", {"r": 0.0}, {"s": 0.0}, "Ayer", date(2026, 5, 1))
    
    catalogo = ServicioStreaming([c_ayer], [], [lista])
    sesion = Sesion([])
    estrategia = Temporal()
    
    resultado = estrategia.buscar(catalogo, sesion)
    # Debe devolver la lista por ser más reciente que la canción individual
    assert isinstance(resultado, ListaReproduccion)
    assert resultado == lista

def test_temporal_sin_resultados():
    """Verifica que devuelva None si nada coincide temporalmente con la sesión."""
    c_lejana = Cancion("ID_L", {"r": 1.0}, {"s": 1.0}, "Lejana", date.today())
    catalogo = ServicioStreaming([c_lejana], [], [])
    sesion = Sesion([]) # Media 0.0
    estrategia = Temporal()
    
    assert estrategia.buscar(catalogo, sesion) is None