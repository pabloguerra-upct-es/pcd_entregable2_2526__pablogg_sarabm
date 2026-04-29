from abc import ABCMeta, abstractmethod
from functools import reduce
from datetime import date

class DuplicatedError(Exception):
    pass

class ElementoCatalogo(metaclass = ABCMeta):
    @abstractmethod
    def obtenerCaracteristicas(self):
        pass

class Cancion(ElementoCatalogo):
    def __init__(self, id:str, c_sonoras:dict, c_sentimentales:dict, titulo:str, fecha_creacion: date):
        if not isinstance(id, str):
            raise TypeError("id tiene que ser un numero entero")
        
        if not isinstance(c_sonoras, dict):
            raise TypeError("c_sonoras debe ser un diccionario")
        
        if not isinstance(c_sentimentales, dict):
            raise TypeError("c_sentimentales debe ser un diccionario")
        
        if not isinstance(titulo, str):
            raise TypeError("titulo debe ser una cadena de texto")
        
        if not isinstance(fecha_creacion, date):
            raise TypeError("fecha_creacion debe ser una fecha")
        
        self.__id = id
        self.__c_sonoras = c_sonoras
        self.__c_sentimentales = c_sentimentales
        self.__titulo = titulo
        self.__fecha_creacion = fecha_creacion        

    def obtenerCaracteristicas(self) -> dict:
        solucion = {}
        solucion["Caracteristicas Sonoras"] = self.__c_sonoras
        solucion["Caracteristicas Sentimentales"] = self.__c_sentimentales
        return solucion
    
class Artista(ElementoCatalogo):
    def __init__(self, nombre:str, canciones:list[Cancion], fecha_nacimiento:date):
        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser una cadena de texto")
        
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser canciones")  
        
        if not isinstance(fecha_nacimiento, date):
            raise TypeError("fecha_nacimiento debe ser una fecha de nacimiento")

        self.__nombre = nombre
        self.__canciones = canciones
        self.__fecha_nacimiento = fecha_nacimiento

    def obtenerCaracteristicas(self) -> dict:
        solucion = {}
        for cancion in self.__canciones:            
            titulo = cancion.__titulo 
            solucion[titulo] = cancion.obtenerCaracteristicas()
            
        return solucion
    
class ListaReproduccion:
    def __init__(self, canciones:list[Cancion], nombre:str):
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser canciones") 
        
        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser una cadena de texto")
        
        self.__canciones = canciones
        self.__nombre = nombre

    def obtenerCaracteristicas(self) -> dict:
        solucion = {}
        for cancion in self.__canciones:            
            titulo = cancion.__titulo 
            solucion[titulo] = cancion.obtenerCaracteristicas()
            
        return solucion

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

    def agregarCancion(self, c):
        if not isinstance(c, Cancion):
            raise TypeError("c debe pertenecer a la clase Cancion")
        
        for i in self.__canciones:
            if i == c:
                raise DuplicatedError("Esa cancion ya se encuentra en la lista de canciones")
            
        self.__canciones.append(c)

    def obtenerCanciones(self):
        return self.__canciones
    
    def obtenerCaracteristicas(self):
        solucion = {}
        solucion["Media Sonora"] = self.__media_sonora
        solucion["Media Sentimental"] = self.__media_sentimental
        solucion["Desviacion Sonora"] = self.__desviacion_sonora
        solucion["Desviacion Sentimental"] = self.__desviacion_sentimental
        return solucion

class Manejador:
    def __init__(self, siguiente:Manejador):
        if not isinstance(siguiente, Manejador):
            raise TypeError("siguiente debe ser un Manejador")
        self._siguiente = siguiente

class ManejadorSonoro:
    pass

class ManejadorSentimental:
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

    def getCanciones(self):
        return self.__canciones
    
    def getArtistas(self):
        return self.__artistas
    
    def getListasRepro(self):
        return self.__listas_repro

class EstrategiaBusqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscar(catalogo:ServicioStreaming, sesion:Sesion):
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un servicio de streaming")
        
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe ser una sesion")
        
        pass

class Alfabetico(EstrategiaBusqueda):
    def buscar(self, catalogo:ServicioStreaming, sesion:Sesion):
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe pertenecer a la clase ServicioStreaming")
        
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe pertenecer a la clase Sesion")

        catalogo_completo = set(catalogo.getCanciones())
        for artista in catalogo.getArtistas():
            catalogo_completo.update(artista.__canciones)

        for lista in catalogo.getListasRepro():
            catalogo_completo.update(lista.__canciones)

        canciones_ordenadas = sorted(
            list(catalogo_completo), 
            key=lambda c: c._Cancion__titulo.lower()
        )

        estadisticas_sesion = sesion.obtenerCaracteristicas()

        def coincide(cancion):
            caract_can = cancion.obtenerCaracteristicas()

            sonoras = caract_can.get("Caracteristicas Sonoras", {})
            sentimentales = caract_can.get("Caracteristicas Sentimentales", {})

            for clave, valor in sonoras.items():
                media = estadisticas_sesion.get("Media Sonora", 0)
                desv = estadisticas_sesion.get("Desviacion Sonora", 0)
                
                if abs(valor - media) > desv:
                    return False
            
            return True

        coincidentes = filter(coincide, canciones_ordenadas)

        try:
            return next(coincidentes)
        except StopIteration:
            return None

        
class Temporal(EstrategiaBusqueda):
    def buscar(self, catalogo: ServicioStreaming, sesion: Sesion):
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe pertenecer a la clase ServicioStreaming")
        
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe pertenecer a la clase Sesion")

        catalogo_completo = set(catalogo.getCanciones())
        
        for artista in catalogo.getArtistas():
            catalogo_completo.update(artista.__canciones)

        for lista in catalogo.getListasRepro():
            catalogo_completo.update(lista.__canciones)

        canciones_ordenadas = sorted(
            list(catalogo_completo), 
            key=lambda c: c._Cancion__fecha_creacion,
            reverse=True
        )

        estadisticas_sesion = sesion.obtenerCaracteristicas()

        def coincide(cancion):
            caract_can = cancion.obtenerCaracteristicas()
            sonoras = caract_can.get("Caracteristicas Sonoras", {})
            sentimentales = caract_can.get("Caracteristicas Sentimentales", {})

            for valor in sonoras.values():
                media = estadisticas_sesion.get("Media Sonora", 0)
                desv = estadisticas_sesion.get("Desviacion Sonora", 0)
                if abs(valor - media) > desv:
                    return False
            
            for valor in sentimentales.values():
                media = estadisticas_sesion.get("Media Sentimental", 0)
                desv = estadisticas_sesion.get("Desviacion Sentimental", 0)
                if abs(valor - media) > desv:
                    return False
            
            return True

        coincidentes = filter(coincide, canciones_ordenadas)

        try:
            return next(coincidentes)
        except StopIteration:
            return None

class Aleatorio:
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

class RecomArtista:
    pass

class RecomListaRepro:
    pass

class EstrategiaBusqueda:
    pass
