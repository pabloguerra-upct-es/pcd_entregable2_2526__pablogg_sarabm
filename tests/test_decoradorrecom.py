import pytest
from datetime import date

from streaming_musical import DecoradorRecom, Recomendacion, Cancion

def test_validacion_tipos_decorador():
    """Verifica que el constructor lance TypeError antes de intentar acceder a atributos."""
    cancion = Cancion("ID1", {}, {}, "Test", date.today())

    with pytest.raises(TypeError) as excinfo:
        DecoradorRecom(cancion) 
    
    assert "recomendacion debe ser un objeto de la clase Recomendacion" in str(excinfo.value)

def test_delegacion_decorador_funcional():
    """Verifica la delegación correcta al objeto envuelto."""
    c1 = Cancion("ID_VAL", {}, {}, "Cancion", date.today())
    rec_base = Recomendacion(c1)
    decorador = DecoradorRecom(rec_base)
    
    assert decorador.obtenerResultado() == c1