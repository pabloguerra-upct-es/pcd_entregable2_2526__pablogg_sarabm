import pytest
from datetime import date

from streaming_musical import ServicioStreaming, Cancion, Artista, ListaReproduccion

def test_creacion_servicio_valido():
    """Verifica que el servicio se inicie correctamente con listas válidas."""
    # Preparación de datos mínimos
    c1 = Cancion("ID1", {}, {}, "S1", date.today())
    a1 = Artista("Artista 1", [c1], date(1990, 1, 1))
    l1 = ListaReproduccion([c1], "Lista Reproduccion 1", date.today())
    
    canciones = [c1]
    artistas = [a1]
    listas = [l1]
    
    servicio = ServicioStreaming(canciones, artistas, listas)
    
    assert servicio._ServicioStreaming__canciones == canciones
    assert servicio._ServicioStreaming__artistas == artistas
    assert servicio._ServicioStreaming__listas_repro == listas

def test_getters_servicio():
    """Prueba que los métodos get devuelvan las listas correctas."""
    c1 = Cancion("ID1", {}, {}, "S1", date.today())
    servicio = ServicioStreaming([c1], [], [])
    
    assert servicio.getCanciones() == [c1]
    assert isinstance(servicio.getArtistas(), list)
    assert len(servicio.getListasRepro()) == 0

def test_validacion_tipos_servicio():
    """Verifica que el constructor lance TypeError ante datos incorrectos."""
    c1 = Cancion("ID1", {}, {}, "S1", date.today())
    
    # Error: canciones no es una lista
    with pytest.raises(TypeError):
        ServicioStreaming(c1, [], [])
    
    # Error: la lista de artistas contiene un tipo erróneo
    with pytest.raises(TypeError):
        ServicioStreaming([c1], ["No artista"], [])
        
    # Error: la lista de reproducción contiene un tipo erróneo
    with pytest.raises(TypeError):
        ServicioStreaming([c1], [], [12345])

def test_listas_vacias_validas():
    """Asegura que el servicio se pueda crear con listas vacías."""

    servicio = ServicioStreaming([], [], [])
    assert len(servicio.getCanciones()) == 0