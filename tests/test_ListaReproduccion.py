import pytest
from datetime import date

from streaming_musical import ListaReproduccion, Cancion

def test_creacion_lista_reproduccion_valida():
    """Verifica la instanciación."""
    c1 = Cancion("ID1", {}, {}, "CancionA", date(2025, 1, 1))
    c2 = Cancion("ID2", {}, {}, "CancionB", date(2025, 2, 1))
    canciones = [c1, c2]
    nombre = "Lista Reproduccion"
    fecha = date(2026, 5, 2)

    lista = ListaReproduccion(canciones, nombre, fecha)

    # Verificación de atributos privados
    assert lista._ListaReproduccion__nombre == nombre
    assert lista._ListaReproduccion__canciones == canciones
    assert lista._ListaReproduccion__fecha_creacion == fecha

def test_metodo_obtener_canciones():
    """Prueba el funcionamiento del método público obtenerCanciones."""
    c1 = Cancion("T1", {}, {}, "Test", date.today())
    lista = ListaReproduccion([c1], "Favs", date.today())
    
    resultado = lista.obtenerCanciones()
    assert len(resultado) == 1
    assert resultado[0] == c1

def test_obtener_caracteristicas_formato():
    """Verifica que el diccionario generado use el título como clave."""
    nombre_track = "Cancion"
    c1 = Cancion("ID_X", {"vol": 0.8}, {"bpm": 128}, nombre_track, date.today())
    lista = ListaReproduccion([c1], "Hits", date.today())

    caracteristicas = lista.obtenerCaracteristicas()
    
    # Comprobar estructura del diccionario
    assert nombre_track in caracteristicas
    assert "Caracteristicas Sonoras" in caracteristicas[nombre_track]

def test_excepciones_tipos_lista():
    """Valida que el constructor proteja contra tipos de datos inválidos."""
    # El nombre debe ser una cadena
    with pytest.raises(TypeError):
        ListaReproduccion([], 999, date.today())
    
    # La lista solo debe contener objetos Cancion
    with pytest.raises(TypeError):
        ListaReproduccion(["no ancion"], "Error", date.today())

    # La fecha debe ser un objeto date
    with pytest.raises(TypeError):
        ListaReproduccion([], "Error", "2026-05-02")