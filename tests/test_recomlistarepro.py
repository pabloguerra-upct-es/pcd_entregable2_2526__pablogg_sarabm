import pytest
from datetime import date

from streaming_musical import RecomListaRepro, Recomendacion, ServicioStreaming, Cancion, ListaReproduccion

def test_transformacion_a_lista_reproduccion():
    """Verifica que el decorador devuelva la lista si la canción está contenida en una."""
    c1 = Cancion("ID1", {}, {}, "Cancion en Lista", date.today())
    # Creamos una lista que contiene la canción
    lista_esperada = ListaReproduccion([c1], "Mix Favoritos", date.today())
    
    catalogo = ServicioStreaming([c1], [], [lista_esperada])
    rec_base = Recomendacion(c1)
    
    decorador = RecomListaRepro(rec_base, catalogo)
    
    # El resultado debe ser la lista, no la canción individual
    resultado = decorador.obtenerResultado()
    assert isinstance(resultado, ListaReproduccion)
    assert resultado == lista_esperada

def test_retorno_cancion_si_no_hay_lista():
    """Verifica que devuelva la canción original si no pertenece a ninguna lista."""
    c1 = Cancion("ID1", {}, {}, "Cancion Suelta", date.today())
    # Catálogo sin listas de reproducción
    catalogo = ServicioStreaming([c1], [], [])
    rec_base = Recomendacion(c1)
    
    decorador = RecomListaRepro(rec_base, catalogo)
    
    # Al no encontrar lista, debe devolver la canción
    resultado = decorador.obtenerResultado()
    assert isinstance(resultado, Cancion)
    assert resultado == c1

def test_validacion_tipos_recom_lista():
    """Valida los errores de tipo en el constructor."""
    c1 = Cancion("ID1", {}, {}, "S1", date.today())
    rec_base = Recomendacion(c1)
    catalogo = ServicioStreaming([], [], [])

    with pytest.raises(TypeError):
        RecomListaRepro(c1, catalogo) # Error: recomendacion no es objeto Recomendacion

    with pytest.raises(TypeError):
        RecomListaRepro(rec_base, "Catalogo Invalido") # Error: catalogo no es ServicioStreaming

def test_estado_interno_recom_lista():
    """Verifica el almacenamiento del catálogo."""
    c1 = Cancion("ID1", {}, {}, "S1", date.today())
    catalogo = ServicioStreaming([], [], [])
    rec_base = Recomendacion(c1)
    
    decorador = RecomListaRepro(rec_base, catalogo)
    
    assert decorador._RecomListaRepro__catalogo == catalogo