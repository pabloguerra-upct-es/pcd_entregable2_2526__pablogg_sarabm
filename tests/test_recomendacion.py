import pytest
from datetime import date

from streaming_musical import Recomendacion, Cancion, Artista, ElementoCatalogo

def test_creacion_recomendacion_con_cancion():
    """Verifica que Recomendacion acepte una Cancion y la devuelva correctamente."""
    cancion = Cancion("ID1", {}, {}, "Test Song", date.today())
    
    # Recomendacion debe aceptar cualquier ElementoCatalogo
    rec = Recomendacion(cancion)
    
    # Verificación del método público
    assert rec.obtenerResultado() == cancion
    assert isinstance(rec.obtenerResultado(), ElementoCatalogo)

def test_creacion_recomendacion_con_artista():
    """Verifica que Recomendacion acepte un Artista (que también es ElementoCatalogo)."""
    artista = Artista("Nombre Artista", [], date(1990, 1, 1))
    
    rec = Recomendacion(artista)
    
    assert rec.obtenerResultado() == artista
    assert rec._elemento == artista

def test_validacion_tipos_recomendacion():
    """Verifica que el constructor lance TypeError si el objeto no es del catálogo."""
    # Intentar pasar un string en lugar de un ElementoCatalogo
    with pytest.raises(TypeError) as excinfo:
        Recomendacion("No soy un elemento")
    
    assert "elemento debe ser un elemento del catalogo" in str(excinfo.value)

def test_obtener_resultado_identidad():
    """Asegura que obtenerResultado devuelva exactamente la misma instancia."""
    c1 = Cancion("ID1", {}, {}, "S1", date.today())
    rec = Recomendacion(c1)
    
    assert rec.obtenerResultado() is c1