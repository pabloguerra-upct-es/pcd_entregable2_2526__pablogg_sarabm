import pytest
from datetime import date

from streaming_musical import RecomArtista, Recomendacion, ServicioStreaming, Cancion

def test_creacion_recom_artista_valida():
    """Verifica la correcta instanciación con todos los parámetros válidos."""
    c1 = Cancion("ID1", {}, {}, "Cancion", date.today())
    catalogo = ServicioStreaming([c1], [], [])
    rec_base = Recomendacion(c1)
    
    # Instanciación del decorador específico
    recom_artista = RecomArtista(rec_base, catalogo)
    
    # Comprobar que el resultado se delega correctamente
    assert recom_artista.obtenerResultado() == c1
    assert recom_artista._RecomArtista__catalogo == catalogo

def test_herencia_y_super_recom_artista():
    """Verifica que herede de DecoradorRecom y mantenga el elemento base."""
    c1 = Cancion("ID1", {}, {}, "Cancion", date.today())
    rec_base = Recomendacion(c1)
    catalogo = ServicioStreaming([], [], [])
    
    recom_artista = RecomArtista(rec_base, catalogo)
    
    assert recom_artista._elemento == c1

def test_validacion_tipos_recom_artista():
    """Verifica que el constructor proteja contra tipos de datos inválidos."""
    c1 = Cancion("ID1", {}, {}, "S1", date.today())
    rec_base = Recomendacion(c1)
    catalogo = ServicioStreaming([], [], [])

    # Error: El primer parámetro no es una Recomendacion
    with pytest.raises(TypeError) as excinfo:
        RecomArtista(c1, catalogo)
    assert "recomendacion tiene que ser un objeto de la clase Recomendacion" in str(excinfo.value)

    # Error: El segundo parámetro no es un ServicioStreaming
    with pytest.raises(TypeError) as excinfo:
        RecomArtista(rec_base, "No soy un catalogo")
    assert "catalogo debe ser un objeto de la clase ServicioStreaming" in str(excinfo.value)

def test_recom_artista_en_cadena():
    """Verifica que funcione incluso si envuelve a otro decorador."""
    from streaming_musical import DecoradorRecom
    
    c1 = Cancion("ID1", {}, {}, "S1", date.today())
    rec_base = Recomendacion(c1)
    dec_simple = DecoradorRecom(rec_base)
    catalogo = ServicioStreaming([], [], [])
    
    # Envolver un decorador con otro
    recom_artista = RecomArtista(dec_simple, catalogo)
    
    assert recom_artista.obtenerResultado() == c1