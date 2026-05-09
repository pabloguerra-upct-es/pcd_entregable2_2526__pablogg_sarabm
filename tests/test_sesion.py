import pytest
from datetime import date

from streaming_musical import Sesion, Cancion, Manejador, DuplicatedError

class MockManejador(Manejador):
    def procesar(self, sesion: Sesion):
        sesion._Sesion__media_sonora = 0.5
        sesion._Sesion__media_sentimental = 0.7

def test_creacion_sesion_vacia():
    """Verifica que la sesión se inicie correctamente vacía."""
    sesion = Sesion([])
    assert len(sesion.obtenerCanciones()) == 0
    assert sesion._Sesion__media_sonora == 0

def test_agregar_cancion_y_duplicados():
    """Verifica la inserción y que se lance DuplicatedError si ya existe."""
    c1 = Cancion("ID1", {}, {}, "Cancion1", date.today())
    sesion = Sesion([c1])
    
    # Intentar añadir la misma canción debe fallar
    with pytest.raises(DuplicatedError):
        sesion.agregarCancion(c1)
    
    # Añadir una nueva debe funcionar
    c2 = Cancion("ID2", {}, {}, "Cancion2", date.today())
    sesion.agregarCancion(c2)
    assert len(sesion.obtenerCanciones()) == 2

def test_obtener_caracteristicas_manejador():
    """Verifica que el método llame del manejador."""
    c1 = Cancion("ID1", {}, {}, "Song 1", date.today())
    sesion = Sesion([c1])
    manejador = MockManejador()
    
    # El método devuelve el diccionario tras pasar por el manejador
    stats = sesion.obtenerCaracteristicas(manejador)
    
    assert stats["Media Sonora"] == 0.5
    assert stats["Media Sentimental"] == 0.7
    assert "Desviacion Sonora" in stats

def test_validacion_tipos_sesion():
    """Valida que el constructor y métodos protejan contra tipos erróneos."""
    with pytest.raises(TypeError):
        Sesion("no lista")
        
    sesion = Sesion([])
    with pytest.raises(TypeError):
        sesion.agregarCancion("no objeto clase Cancion")
    
    with pytest.raises(TypeError):
        sesion.obtenerCaracteristicas("no Manejador")