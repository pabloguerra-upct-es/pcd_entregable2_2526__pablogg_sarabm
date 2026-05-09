import pytest
from datetime import date

from streaming_musical import Artista, Cancion, ElementoCatalogo

def test_creacion_artista_valida():
    """Verifica la correcta instanciación de Artista y sus atributos privados."""
    c1 = Cancion("ID1", {}, {}, "CancionA", date(2020, 1, 1))
    lista_canciones = [c1]
    fecha_nac = date(1990, 5, 15)
    nombre = "Cantante de Prueba"

    artista = Artista(nombre, lista_canciones, fecha_nac)

    assert artista._Artista__nombre == nombre
    assert artista._Artista__canciones == lista_canciones
    assert artista._Artista__fecha_nacimiento == fecha_nac

def test_obtener_canciones():
    """Verifica que el método público devuelva la lista de canciones."""
    c1 = Cancion("ID1", {}, {}, "Test", date.today())
    artista = Artista("Nombre", [c1], date(1980, 1, 1))
    
    resultado = artista.obtenerCanciones()
    assert isinstance(resultado, list)
    assert len(resultado) == 1
    assert resultado[0] == c1

def test_obtener_caracteristicas_artista():
    """Verifica que genere el diccionario indexado por el título de la canción 4]."""

    nombre_esperado = "Titulo"
    c1 = Cancion("ID1", {"ritmo": 0.5}, {"mood": 0.8}, nombre_esperado, date.today())
    artista = Artista("Paco", [c1], date(1970, 1, 1))

    caracteristicas = artista.obtenerCaracteristicas()
    
    assert nombre_esperado in caracteristicas
    assert "Caracteristicas Sonoras" in caracteristicas[nombre_esperado]
    assert caracteristicas[nombre_esperado]["Caracteristicas Sonoras"]["ritmo"] == 0.5

def test_validacion_tipos_artista():
    """Comprueba que el constructor lance TypeError ante datos inválidos."""
    c1 = Cancion("ID1", {}, {}, "Cancion", date.today())
    
    # El nombre debe ser string
    with pytest.raises(TypeError):
        Artista(123, [c1], date(1990, 1, 1))

    # La lista de canciones debe contener solo objetos Cancion
    with pytest.raises(TypeError):
        Artista("Nombre", ["No cancion"], date(1990, 1, 1))

def test_herencia_artista():
    """Asegura que Artista sea reconocido como un ElementoCatalogo."""
    artista = Artista("Nombre", [], date(1980, 1, 1))
    assert isinstance(artista, ElementoCatalogo)