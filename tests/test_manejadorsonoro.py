import pytest
from datetime import date

from streaming_musical import ManejadorSonoro, Sesion, Cancion

def test_calculo_media_sonora():
    """Verifica que el cálculo de la media aritmética de los valores sonoros sea exacto."""
    # Creamos canciones con valores conocidos para facilitar la verificación
    c1 = Cancion("ID1", {"ritmo": 0.4}, {}, "S1", date.today())
    c2 = Cancion("ID2", {"ritmo": 0.6}, {}, "S2", date.today())
    
    manejador = ManejadorSonoro()
    # La media de 0.4 y 0.6 es 0.5
    resultado_media = manejador._calcularMedia([c1, c2])
    
    assert resultado_media == pytest.approx(0.5)

def test_calculo_desviacion_sonora():
    """Verifica que el cálculo de la desviación sonora sea correcto."""
    c1 = Cancion("ID1", {"ritmo": 10.0}, {}, "S1", date.today())
    c2 = Cancion("ID2", {"ritmo": 20.0}, {}, "S2", date.today())
    media = 15.0
    
    manejador = ManejadorSonoro()
    resultado_desv = manejador._calcularDesviacion([c1, c2], media)
    
    assert resultado_desv == pytest.approx(5.0)

def test_procesar_actualiza_sesion():
    """Verifica que el método procesar asigne los valores a los atributos privados de la sesión."""
    c1 = Cancion("ID1", {"ritmo": 0.8}, {}, "S1", date.today())
    sesion = Sesion([c1])
    manejador = ManejadorSonoro()
    
    manejador.procesar(sesion)
    
    assert sesion._Sesion__media_sonora == pytest.approx(0.8) 
    assert sesion._Sesion__desviacion_sonora == pytest.approx(0.0)

def test_validacion_tipos_manejador_sonoro():
    """Verifica que los métodos privados y públicos lancen TypeError ante entradas inválidas."""
    manejador = ManejadorSonoro()
    
    with pytest.raises(TypeError):
        manejador.procesar("No sesion")
        
    with pytest.raises(TypeError):
        manejador._calcularMedia("No lista")
        
    with pytest.raises(TypeError):
        # La media debe ser float, no string
        manejador._calcularDesviacion([], "media_erronea")

def test_procesar_vacio():
    """Verifica que el manejador no falle si la sesión no tiene canciones."""
    sesion = Sesion([])
    manejador = ManejadorSonoro()
    
    # No debería lanzar excepción y los valores deberían seguir en 0
    manejador.procesar(sesion)
    assert sesion._Sesion__media_sonora == 0