class Date:
    def __init__(self, dia:int, mes:int, año:int):
        self.dia = dia
        self.mes = mes
        self.año = año

class Cancion:
    def __init__(self, id:str, c_sonoras:dict, c_sentimentales:dict, titulo:str, fecha_creacion: Date):
        self.__id = id
        self.__c_sonoras = c_sonoras
        self.__c_sentimentales = c_sentimentales
        self.__titulo = titulo
        self.__fecha_creacion = fecha_creacion

class Sesion:
    def __init__(self, canciones:list[Cancion], media_sonora:float, media_sentimental:float, desviacion_sonora:float, desviacion_sentimental:float):
        self.__canciones = canciones
        self.__media_sonora = media_sonora
        self.__media_sentimental = media_sentimental
        self.__desviacion_sonora = desviacion_sonora
        self.__desviacion_sentimental = desviacion_sentimental

class Manejador:
    def __init__(self, siguiente:Manejador):
        self._siguiente = siguienteç

class ManejadorSonoro:
    pass

class ManejadorSentimental:
    pass

class Recomendacion:
    def __init__(self, elemento):
        self._elemento = elemento

class DecoradorRecom:
    def __init__(self, recomendacion):
        self.__recomendacion = recomendacion

class EstrategiaBusqueda:
    pass

class SistemaRecomendacion:
    def __init__(self, instancia:SistemaRecomendacion, estrategia: EstrategiaBusqueda, manejador_inicial:Manejador, sesion:Sesion, tipo_recomendacion):
        self.__instancia = instancia
        self.__estrategia = estrategia
        self.__manejador_inicial = manejador_inicial
        self.__sesion = sesion
        self.__tipo_recomendacion = tipo_recomendacion

class Artista:
    def __init__(self, nombre:str, canciones:list[Cancion], fecha_nacimiento:Date):
        self.__nombre = nombre
        self.__canciones = canciones
        self.__fecha_nacimiento = fecha_nacimiento

class ListaReproduccion:
    def __init__(self, canciones:list[Cancion]):
        self.__canciones = canciones
        
class ServicioStreaming:
    def __init__(self, canciones:list[Cancion], artistas:list[Artista], listas_repro:list[ListaReproduccion]):
        self.__canciones = canciones
        self.__artistas = artistas
        self.__listas_repro = listas_repro

class RecomArtista:
    pass

class RecomListaRepro:
    pass

class EstrategiaBusqueda:
    pass

class ElementoCatalogo:
    pass

class Temporal:
    pass

class Alfabetico:
    pass

class Aleatorio:
    pass

class ElementoCatalogo:
    pass





