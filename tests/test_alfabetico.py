from datetime import date

from streaming_musical import Alfabetico, ServicioStreaming, Sesion, Cancion

def test_ordenacion_alfabetica():
    """Verifica la ordenación con valores que superan el filtro de similitud."""
    # Usamos valores cercanos a 0.0 para que coincidan con una sesión vacía (media 0)

    c_z = Cancion("ID_Z", {"r": 0.05}, {"s": 0.05}, "CancionZ", date.today())
    c_a = Cancion("ID_A", {"r": 0.05}, {"s": 0.05}, "CancionA", date.today())
    c_b = Cancion("ID_B", {"r": 0.05}, {"s": 0.05}, "CancionB", date.today())

    catalogo = ServicioStreaming([c_z, c_a, c_b], [], [])
    sesion = Sesion([]) # Media sonora/sentimental inicial es 0.0
    estrategia = Alfabetico()

    resultado = estrategia.buscar(catalogo, sesion)
    
    assert resultado is not None
    assert resultado._Cancion__titulo == "CancionA"

def test_filtro_canciones_escuchadas():
    """Verifica que no se recomienden canciones ya presentes en la sesión."""
    c1 = Cancion("ID1", {"r": 0.0}, {"s": 0.0}, "CancionA", date.today())
    c2 = Cancion("ID2", {"r": 0.0}, {"s": 0.0}, "CancionB", date.today())
    
    catalogo = ServicioStreaming([c1, c2], [], [])
    sesion = Sesion([c1]) # CancionA ya ha sido escuchada
    estrategia = Alfabetico()
    
    resultado = estrategia.buscar(catalogo, sesion)
    assert resultado._Cancion__titulo == "CancionB"

def test_filtro_similitud_estricto():
    """Verifica que se descarte la canción si supera el margen de 0.1."""
    # Canción candidata con valor 0.5. Sesión con media 0.0.

    c_lejana = Cancion("ID_L", {"ritmo": 0.5}, {"sent": 0.5}, "Lejana", date.today())
    
    catalogo = ServicioStreaming([c_lejana], [], [])
    sesion = Sesion([])
    estrategia = Alfabetico()
    
    assert estrategia.buscar(catalogo, sesion) is None