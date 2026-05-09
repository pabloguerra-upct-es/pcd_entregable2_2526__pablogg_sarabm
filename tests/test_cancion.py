import pytest
from datetime import date

from streaming_musical import Cancion, ElementoCatalogo

def test_creacion_cancion_valida():
    """Verifica la instancia para datos privados."""
    id_test = "C100"
    sonoras = {"volumen": 0.8}
    sentimentales = {"alegria": 0.5}
    titulo = "Cancion de Prueba"
    fecha = date(2024, 1, 1)

    cancion = Cancion(id_test, sonoras, sentimentales, titulo, fecha)

    assert cancion._Cancion__id == id_test
    assert cancion._Cancion__titulo == titulo
    assert cancion._Cancion__fecha_creacion == fecha

def test_obtener_caracteristicas():
    """Verifica que se devuelvan las caracteristicas correctamente."""

    sonoras = {"ritmo": 0.5}
    sentimentales = {"pasion": 0.9}
    cancion = Cancion("ID1", sonoras, sentimentales, "Test", date.today())
    
    resultado = cancion.obtenerCaracteristicas()

    assert "Caracteristicas Sonoras" in resultado
    assert resultado["Caracteristicas Sonoras"] == sonoras

def test_validacion_tipos_cancion():
    """Verifica que el constructor lance TypeError."""
    
    with pytest.raises(TypeError):
        # El constructor valida que el ID sea str
        Cancion(123, {}, {}, "Titulo", date.today())

def test_herencia_elemento_catalogo():
    """Verifica la jerarquía de clases."""
    cancion = Cancion("ID1", {}, {}, "Test", date.today())
    # Cancion hereda de ElementoCatalogo
    assert isinstance(cancion, ElementoCatalogo)