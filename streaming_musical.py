class Date:
    def __init__(self, dia:int, mes:int, año:int):
        if not isinstance(dia, int):
            raise TypeError("dia debe ser un numero entero")
        
        if not isinstance(mes, int):
            raise TypeError("mes debe ser un numero entero")
        
        if not isinstance(año, int):
            raise TypeError("año debe ser un numero entero")
        
        if ((dia < 1 or dia > 12) or (dia > 29 and mes == 2)):
            raise ValueError("El dia introducido no es coherente")
        
        if mes < 1 or mes > 12:
            raise ValueError("El mes introducido no es coherente")
        
        if año < 0:
            raise ValueError("El mes introducido no es coherente")
        
        self.dia = dia
        self.mes = mes
        self.año = año

class Cancion:
    def __init__(self, id:str, c_sonoras:dict, c_sentimentales:dict, titulo:str, fecha_creacion: Date):
        if not isinstance(id, str):
            raise TypeError("id tiene que ser un numero entero")
        
        if not isinstance(c_sonoras, dict):
            raise TypeError("c_sonoras debe ser un diccionario")
        
        if not isinstance(c_sentimentales, dict):
            raise TypeError("c_sentimentales debe ser un diccionario")
        
        if not isinstance(titulo, str):
            raise TypeError("titulo debe ser una cadena de texto")
        
        if not isinstance(fecha_creacion, Date):
            raise TypeError("fecha_creacion debe ser una fecha")
        
        self.__id = id
        self.__c_sonoras = c_sonoras
        self.__c_sentimentales = c_sentimentales
        self.__titulo = titulo
        self.__fecha_creacion = fecha_creacion

class Sesion:
    def __init__(self, canciones:list[Cancion], media_sonora:float, media_sentimental:float, desviacion_sonora:float, desviacion_sentimental:float):
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser canciones")  
            
        if not isinstance(media_sonora, float):
            raise TypeError("media_sonora debe ser un numero decimal (float)")
        
        if not isinstance(media_sentimental, float):
            raise TypeError("media_sentimental debe ser un numero decimal (float)")
        
        if not isinstance(desviacion_sonora, float):
            raise TypeError("desviacion_sonora debe ser un numero decimal (float)")
        
        if not isinstance(desviacion_sentimental, float):
            raise TypeError("desviacion_sentimental debe ser un numero decimal (float)")
        
        self.__canciones = canciones
        self.__media_sonora = media_sonora
        self.__media_sentimental = media_sentimental
        self.__desviacion_sonora = desviacion_sonora
        self.__desviacion_sentimental = desviacion_sentimental

class Manejador:
    def __init__(self, siguiente:Manejador):
        if not isinstance(siguiente, Manejador):
            raise TypeError("siguiente debe ser un Manejador")
        self._siguiente = siguiente

class ManejadorSonoro:
    pass

class ManejadorSentimental:
    pass

class ElementoCatalogo:
    pass

class Recomendacion:
    def __init__(self, elemento:ElementoCatalogo):
        if not isinstance(elemento, ElementoCatalogo):
            raise TypeError("elemento debe ser un elemento del catalogo")
        
        self._elemento = elemento

class DecoradorRecom:
    def __init__(self, recomendacion:Recomendacion):
        if not isinstance(recomendacion, Recomendacion):
            raise TypeError("recomendacion debe ser una recomendacion")
        self.__recomendacion = recomendacion

class EstrategiaBusqueda:
    pass

class SistemaRecomendacion:
    def __init__(self, instancia:SistemaRecomendacion, estrategia: EstrategiaBusqueda, manejador_inicial:Manejador, sesion:Sesion, tipo_recomendacion):
        if not isinstance(instancia, SistemaRecomendacion):
            raise TypeError("instancia debe ser el sistema de recomendacion")
        
        if not isinstance(estrategia, EstrategiaBusqueda):
            raise TypeError("estrategia debe ser una estrategia de busqueda")
        
        if not isinstance(manejador_inicial, Manejador):
            raise TypeError("manejador debe ser el manejador")
        
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe ser la sesion")
        
        if not isinstance(tipo_recomendacion, (Cancion, Artista, ListaReproduccion)):
            raise TypeError("tipo_recomendacion debe ser una cancion, un artista o una lista de reproduccion")
        
        self.__instancia = instancia
        self.__estrategia = estrategia
        self.__manejador_inicial = manejador_inicial
        self.__sesion = sesion
        self.__tipo_recomendacion = tipo_recomendacion

class Artista:
    def __init__(self, nombre:str, canciones:list[Cancion], fecha_nacimiento:Date):
        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser una cadena de texto")
        
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser canciones")  
        
        if not isinstance(fecha_nacimiento, Date):
            raise TypeError("fecha_nacimiento debe ser una fecha de nacimiento")

        self.__nombre = nombre
        self.__canciones = canciones
        self.__fecha_nacimiento = fecha_nacimiento

class ListaReproduccion:
    def __init__(self, canciones:list[Cancion]):
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser canciones") 
        
        self.__canciones = canciones
        
class ServicioStreaming:
    def __init__(self, canciones:list[Cancion], artistas:list[Artista], listas_repro:list[ListaReproduccion]):
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser canciones") 

        if not isinstance(artistas, list):
            raise TypeError("artistas debe ser una lista")

        if not all(isinstance(a, Artista) for a in artistas):
            raise TypeError("Todos los elementos deben ser artistas") 

        if not isinstance(listas_repro, list):
            raise TypeError("listas_repro debe ser una lista")

        if not all(isinstance(l, ListaReproduccion) for l in listas_repro):
            raise TypeError("Todos los elementos deben ser listas de reproduccion")
         
        self.__canciones = canciones
        self.__artistas = artistas
        self.__listas_repro = listas_repro

class RecomArtista:
    pass

class RecomListaRepro:
    pass

class EstrategiaBusqueda:
    pass

class Temporal:
    pass

class Alfabetico:
    pass

class Aleatorio:
    pass

