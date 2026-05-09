import pytest
import sys
import os

from streaming_musical import Manejador, Sesion

# 1. Crear una implementación concreta para poder testear la base
class ManejadorPrueba(Manejador):
    def procesar(self, sesion: Sesion):
        # Llamamos al procesar de la superclase para verificar la cadena
        return super().procesar(sesion)

def test_instanciacion_y_siguiente():
    """Verifica que se asigne correctamente el siguiente manejador en el constructor."""
    m2 = ManejadorPrueba()
    m1 = ManejadorPrueba(siguiente=m2)
    
    # Comprobamos que el atributo protegido se haya asignado
    assert m1._siguiente == m2

def test_set_siguiente():
    """Verifica que el método setSiguiente cambie el eslabón de la cadena."""
    m1 = ManejadorPrueba()
    m2 = ManejadorPrueba()
    
    m1.setSiguiente(m2)
    assert m1._siguiente == m2

def test_flujo_cadena_responsabilidad():
    """Verifica que el procesamiento se delegue al siguiente manejador."""
    # Clase que marca cuando se ejecuta
    class ManejadorFinal(Manejador):
        def procesar(self, sesion: Sesion):
            return "FIN"

    m2 = ManejadorFinal()
    m1 = ManejadorPrueba(m2)
    
    # Creamos una sesión vacía para la prueba
    sesion = Sesion([])
    
    # Al procesar m1, debería devolver lo que devuelve m2

    resultado = m1.procesar(sesion)
    assert resultado == "FIN"

def test_validacion_tipos_manejador():
    """Verifica que se lancen TypeError ante tipos incorrectos."""
    # El siguiente debe ser un Manejador
    with pytest.raises(TypeError):
        ManejadorPrueba(siguiente="No manejador")
    
    m1 = ManejadorPrueba()
    with pytest.raises(TypeError):
        m1.setSiguiente(12345)

    # El método procesar debe recibir una Sesion 
    with pytest.raises(TypeError):
        m1.procesar("No sesion")

def test_fin_de_cadena_retorna_none():
    """Verifica que si no hay siguiente, el método base retorna None."""
    m1 = ManejadorPrueba() # Sin siguiente
    sesion = Sesion([])
    assert m1.procesar(sesion) is None