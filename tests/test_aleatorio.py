import pytest
from datetime import date
from streaming_musical import Aleatorio, ServicioStreaming, Sesion, Cancion, Artista, ListaReproduccion

def test_busqueda_aleatoria():
    """Verifica que Aleatorio encuentre y devuelva el objeto (Artista o Lista)."""
    c1 = Cancion("C1", {"r": 0.0}, {"s": 0.0}, "Cancion Artista", date.today())
    c2 = Cancion("C2", {"r": 0.0}, {"s": 0.0}, "Cancion Lista", date.today())
    
    artista = Artista("Autor", [c1], date(1990, 1, 1))
    lista = ListaReproduccion([c2], "ListaReproduccion", date.today())
    
    catalogo = ServicioStreaming([], [artista], [lista])
    sesion = Sesion([]) # Media 0.0
    estrategia = Aleatorio()
    
    resultado = estrategia.buscar(catalogo, sesion)
    
    assert resultado in [artista, lista]
    assert isinstance(resultado, (Artista, ListaReproduccion))

def test_filtro_similitud():
    """Verifica que se filtren objetos cuyas canciones no coinciden con la sesión."""
    # Canción base para establecer la media en la sesión (0.5)
    c_base = Cancion("CB", {"r": 0.5}, {"s": 0.5}, "Base", date.today())
    
    # Canción que coincide exactamente
    c_match = Cancion("CM", {"r": 0.5}, {"s": 0.5}, "Match", date.today())
    
    # Canción que no coincide 
    c_fallo = Cancion("CF", {"r": 0.9}, {"s": 0.9}, "Fallo", date.today())
    
    # Catálogo con una canción que coincide y otra que no
    catalogo = ServicioStreaming([c_match, c_fallo], [], [])
    sesion = Sesion([c_base])
    estrategia = Aleatorio()
    
    resultado = estrategia.buscar(catalogo, sesion)
    
    assert resultado == c_match
    assert resultado != c_fallo

def test_aleatorio_sin_coincidencias():
    """Verifica que devuelva None si ninguna canción del catálogo es similar."""
    c_lejana = Cancion("CL", {"r": 0.8}, {"s": 0.8}, "Lejana", date.today())
    catalogo = ServicioStreaming([c_lejana], [], [])
    sesion = Sesion([]) # Media 0.0
    estrategia = Aleatorio()
    
    assert estrategia.buscar(catalogo, sesion) is None

def test_validacion_tipos_aleatorio():
    """Verifica el manejo de errores de tipo en los parámetros."""
    estrategia = Aleatorio()
    with pytest.raises(TypeError):
        estrategia.buscar("No catalogo", Sesion([]))
    
    with pytest.raises(TypeError):
        estrategia.buscar(ServicioStreaming([], [], []), "No sesion")