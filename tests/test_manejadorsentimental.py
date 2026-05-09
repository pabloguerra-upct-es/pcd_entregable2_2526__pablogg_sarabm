import pytest
from datetime import date

from streaming_musical import ManejadorSentimental, Sesion, Cancion

def test_calculo_media_sentimental():
    """Verifica que la media se calcule correctamente sobre las características sentimentales."""
    c1 = Cancion("ID1", {}, {"alegria": 0.2}, "S1", date.today())
    c2 = Cancion("ID2", {}, {"alegria": 0.8}, "S2", date.today())
    
    manejador = ManejadorSentimental()
    resultado_media = manejador._calcularMedia([c1, c2])
    
    assert resultado_media == pytest.approx(0.5)

def test_calculo_desviacion_sentimental():
    """Verifica el cálculo de la desviación sentimental."""

    c1 = Cancion("ID1", {}, {"tristeza": 1.0}, "S1", date.today())
    c2 = Cancion("ID2", {}, {"tristeza": 3.0}, "S2", date.today())
    
    manejador = ManejadorSentimental()
    resultado_desv = manejador._calcularDesviacion([c1, c2], 2.0)
    
    assert resultado_desv == pytest.approx(1.0)

def test_procesar_actualiza_atributos_sesion():
    """Verifica que el método procesar escriba en los atributos privados de Sesion."""
    c1 = Cancion("ID1", {}, {"energia": 0.9}, "S1", date.today())
    sesion = Sesion([c1])
    manejador = ManejadorSentimental()
    
    manejador.procesar(sesion)
    
    assert sesion._Sesion__media_sentimental == pytest.approx(0.9) 
    assert sesion._Sesion__desviacion_sentimental == pytest.approx(0.0)

def test_manejador_sentimental_validacion_tipos():
    """Verifica que se lancen excepciones ante tipos de datos no permitidos."""
    manejador = ManejadorSentimental()
    
    with pytest.raises(TypeError):
        manejador.procesar("No sesion")
        
    with pytest.raises(TypeError):
        manejador._calcularMedia("No lista")
        
    with pytest.raises(TypeError):
        # Media debe ser float
        manejador._calcularDesviacion([], "media_invalida")

def test_procesar_sin_canciones():
    """Asegura que el manejador gestione sesiones vacías sin errores."""
    sesion = Sesion([])
    manejador = ManejadorSentimental()
    
    # No debe fallar y los valores deben permanecer en 0
    manejador.procesar(sesion)
    assert sesion._Sesion__media_sentimental == 0