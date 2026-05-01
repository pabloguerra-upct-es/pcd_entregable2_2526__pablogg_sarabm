from abc import ABC, abstractmethod
from datetime import date
import random
from math import sqrt
import itertools

class DuplicatedError(Exception):
    pass

class SesionError(Exception):
    pass

class SingletonException(Exception):
    pass

class ElementoCatalogo(ABC):
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

    def obtenerCanciones(self):
        return self.__canciones

    def obtenerCaracteristicas(self) -> dict:
        solucion = {}
        for cancion in self.__canciones:            
            titulo = cancion.titulo 
            solucion[titulo] = cancion.obtenerCaracteristicas()
            
        return solucion
    
class ListaReproduccion:
    def __init__(self, canciones:list[Cancion], nombre:str, fecha_creacion:date):
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser canciones") 
        
        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser una cadena de texto")
        
        if not isinstance(fecha_creacion, date):
            raise TypeError("fecha_creacion debe ser una fecha")
        
        self.__canciones = canciones
        self.__nombre = nombre
        self.__fechs_creacion = fecha_creacion

    def obtenerCanciones(self):
        return self.__canciones

    def obtenerCaracteristicas(self) -> dict:
        solucion = {}
        for cancion in self.__canciones:            
            titulo = cancion.titulo 
            solucion[titulo] = cancion.obtenerCaracteristicas()
            
        return solucion

class Sesion:
    def __init__(self, canciones:list[Cancion]):
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser canciones")  
            
        self.__canciones = canciones
        self.__media_sonora = 0
        self.__media_sentimental = 0
        self.__desviacion_sonora = 0
        self.__desviacion_sentimental = 0

    def agregarCancion(self, c):
        if not isinstance(c, Cancion):
            raise TypeError("c debe pertenecer a la clase Cancion")
        
        for i in self.__canciones:
            if i == c:
                raise DuplicatedError("Esa cancion ya se encuentra en la lista de canciones")
            
        self.__canciones.append(c)

    def obtenerCanciones(self):
        return self.__canciones
    
    def obtenerCaracteristicas(self, m:"Manejador"): 
        if not isinstance(m, Manejador):
            raise TypeError("m debe pertenecer a la clase Manejador")
        
        m.procesar(self)
        return {
        "Media Sonora":self.__media_sonora,
        "Media Sentimental" : self.__media_sentimental,
        "Desviacion Sonora":self.__desviacion_sonora,
        "Desviacion Sentimental":self.__desviacion_sentimental
        }

class Manejador(ABC):
    def __init__(self, siguiente: "Manejador" = None):
        if siguiente is not None and not isinstance(siguiente, Manejador):
            raise TypeError("siguiente debe ser un Manejador")
        
        self._siguiente = siguiente

    def setSiguiente(self, m: "Manejador"):
        """Permite cambiar o establecer el siguiente manejador en la cadena."""
        if not isinstance(m, Manejador):
            raise TypeError("El nuevo manejador debe pertenecer a la clase Manejador")
        
        self._siguiente = m
        return m

    @abstractmethod
    def procesar(self, sesion:Sesion):

        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe pertenecer a la clase Sesion")

        if self._siguiente:
            return self._siguiente.procesar(sesion)
        
        return None

class ManejadorSonoro(Manejador):
    def procesar(self, s: Sesion):
        if not isinstance(s, Sesion):
            raise TypeError("s debe pertenecer a la clase Sesion")
        
        canciones_sesion = s.obtenerCanciones()

        if canciones_sesion:
            media = self._calcularMedia(canciones_sesion)
            desviacion = self._calcularDesviacion(canciones_sesion, media)
            
            s._Sesion__media_sonora = media
            s._Sesion__desviacion_sonora = desviacion
        
        return super().procesar(s)

    def _calcularMedia(self, lista_canciones:list) -> float:
        if not isinstance(lista_canciones, list):
            raise TypeError("lista_canciones debe ser una lista")
        
        suma = 0
        conteo = 0

        for cancion in lista_canciones:
            datos = cancion.obtenerCaracteristicas()
            sonoras = datos.get("Caracteristicas Sonoras", {})

            for valor in sonoras.values():
                suma += valor
                conteo += 1

        return suma / conteo if conteo > 0 else 0.0

    def _calcularDesviacion(self, lista_canciones: list, media: float) -> float:
        if not isinstance(lista_canciones, list):
            raise TypeError("lista_canciones debe ser una lista")
        
        if not isinstance(media, float):
            raise TypeError("media debe ser un numero decimal")
        
        if not lista_canciones:
            return 0.0
            
        suma_cuadrados = 0.0
        conteo = 0
        
        for cancion in lista_canciones:
            datos = cancion.obtenerCaracteristicas()
            sonoras = datos.get("Caracteristicas Sonoras", {})
            
            for valor in sonoras.values():
                suma_cuadrados += (valor - media) ** 2
                conteo += 1
            
        return sqrt(suma_cuadrados / conteo) if conteo > 0 else 0

class ManejadorSentimental(Manejador):
    def procesar(self, s: Sesion):
        if not isinstance(s, Sesion):
            raise TypeError("s debe pertenecer a la clase Sesion")
        
        canciones_sesion = s.obtenerCanciones()

        if canciones_sesion:        

            media = self._calcularMedia(canciones_sesion)
            desviacion = self._calcularDesviacion(canciones_sesion, media)
            
            s._Sesion__media_sentimental = media
            s._Sesion__desviacion_sentimental = desviacion
                
        return super().procesar(s)

    def _calcularMedia(self, lista_canciones: list) -> float:
        if not isinstance(lista_canciones, list):
            raise TypeError("lista_canciones debe ser una lista")
        
        if not lista_canciones:
            return 0.0
        
        suma = 0.0
        conteo = 0

        for cancion in lista_canciones:
            datos = cancion.obtenerCaracteristicas()
            sentimentales = datos.get("Caracteristicas Sentimentales", {})

            for valor in sentimentales.values():
                suma += valor
                conteo += 1

        return suma / conteo if conteo > 0 else 0

    def _calcularDesviacion(self, lista_canciones: list, media: float) -> float:
        if not isinstance(lista_canciones, list):
            raise TypeError("lista_canciones debe ser una lista")
        
        if not isinstance(media, float):
            raise TypeError("media debe ser un numero decimal")
        
        if not lista_canciones:
            return 0.0
            
        suma_cuadrados = 0.0
        conteo = 0
        
        for cancion in lista_canciones:
            datos = cancion.obtenerCaracteristicas()
            sentimentales = datos.get("Caracteristicas Sentimentales", {})
            
            for valor in sentimentales.values():
                suma_cuadrados += (valor - media) ** 2
                conteo += 1
            
        return sqrt(suma_cuadrados / conteo) if conteo > 0 else 0

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

class EstrategiaBusqueda(ABC):
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

        catalogo_completo = set(itertools.chain(
            catalogo.getCanciones(),
            *(artista.obtenerCanciones() for artista in catalogo.getArtistas()),
            *(lista.obtenerCanciones() for lista in catalogo.getListasRepro())
        ))

        canciones_ordenadas = sorted(
            list(catalogo_completo), 
            key=lambda c: c.__titulo.lower()
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
        return next(coincidentes, None)
        
class Temporal(EstrategiaBusqueda):
    def buscar(self, catalogo: ServicioStreaming, sesion: Sesion):
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe pertenecer a la clase ServicioStreaming")
        
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe pertenecer a la clase Sesion")

        items_catalogo = []
        items_catalogo.extend(catalogo.getCanciones())
        items_catalogo.extend(catalogo.getArtistas())
        items_catalogo.extend(catalogo.getListasRepro())

        items_ordenados = sorted(
            items_catalogo,
            key=lambda x: (
                x._Cancion__fecha_creacion if isinstance(x, Cancion) else
                x._ListaReproduccion__fecha_creacion if isinstance(x, ListaReproduccion) else
                x._Artista__fecha_nacimiento if isinstance(x, Artista) else date.min
            ),
            reverse=True
        )

        estadisticas_sesion = sesion.obtenerCaracteristicas(ManejadorSonoro(ManejadorSentimental()))

        def coincide(item):
            if isinstance(item, Cancion):
                canciones_a_validar = [item]

            elif isinstance(item, Artista):
                canciones_a_validar = item.__canciones
            elif isinstance(item, ListaReproduccion):
                canciones_a_validar = item.__canciones
            else:
                return False

            for cancion in canciones_a_validar:
                caract = cancion.obtenerCaracteristicas()
                sonoras = caract.get("Caracteristicas Sonoras", {})
                sentimentales = caract.get("Caracteristicas Sentimentales", {})

                for valor in sonoras.values():
                    if abs(valor - estadisticas_sesion.get("Media Sonora", 0)) > estadisticas_sesion.get("Desviacion Sonora", 0):
                        return False
                
                for valor in sentimentales.values():
                    if abs(valor - estadisticas_sesion.get("Media Sentimental", 0)) > estadisticas_sesion.get("Desviacion Sentimental", 0):
                        return False
            
            return True

        for item in items_ordenados:
            if coincide(item):
                return item

class Aleatorio(EstrategiaBusqueda):
    def buscar(self, catalogo: ServicioStreaming, sesion: Sesion):
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe pertenecer a la clase ServicioStreaming")
        
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe pertenecer a la clase Sesion")

        canciones_lista = list(set(itertools.chain(
            catalogo.getCanciones(),
            *(artista._Artista__canciones for artista in catalogo.getArtistas()),
            *(lista._ListaReproduccion__canciones for lista in catalogo.getListasRepro())
        )))
        
        random.shuffle(canciones_lista) 

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

        coincidentes = filter(coincide, canciones_lista)

        try:
            return next(coincidentes)
        except StopIteration:
            return None

class Recomendacion:
    def __init__(self, elemento:ElementoCatalogo):
        if not isinstance(elemento, ElementoCatalogo):
            raise TypeError("elemento debe ser un elemento del catalogo")
        
        self._elemento = elemento

    def obtenerResultado(self):
        return self._elemento

class DecoradorRecom(Recomendacion):
    def __init__(self, recomendacion:Recomendacion):
        super().__init__(recomendacion._elemento)

        if not isinstance(recomendacion, Recomendacion):
            raise TypeError("recomendacion debe ser un objeto de la clase Recomendacion")
        
        self.__recomendacion = recomendacion

    def obtenerResultado(self):
        return self.__recomendacion.obtenerResultado()

class RecomArtista(DecoradorRecom):
    def __init__(self, recomendacion:Recomendacion, catalogo:ServicioStreaming):
        if not isinstance(recomendacion, Recomendacion):
            raise TypeError("recomendacion tiene que ser un objeto de la clase Recomendacion")
        
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un objeto de la clase ServicioStreaming")
        
        super().__init__(recomendacion)
        self.__catalogo = catalogo

    def obtenerResultado(self):
        cancion = super().obtenerResultado()

        for artista in self.__catalogo.getArtistas():
            if cancion in artista._Artista__canciones:
                return artista
        
        return cancion

class RecomListaRepro(DecoradorRecom):
    def __init__(self, recomendacion:Recomendacion, catalogo:ServicioStreaming):
        if not isinstance(recomendacion, Recomendacion):
            raise TypeError("recomendacion tiene que ser un objeto de la clase Recomendacion")
        
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un objeto de la clase ServicioStreaming")
        
        super().__init__(recomendacion)
        self.__catalogo = catalogo

    def obtenerResultado(self):
        cancion = super().obtenerResultado()

        for lista in self.__catalogo.getListasRepro():
            if cancion in lista._ListaReproduccion__canciones:
                return lista
        
        return cancion

class SistemaRecomendacion:
    __instancia = None

    def __init__(self):
        if SistemaRecomendacion.__instancia is not None:
            raise SingletonException("Al ser un Singleton, debes usar primero getInstancia")       
        
        SistemaRecomendacion.__instancia = self
        self.__estrategia = None
        self.__manejador_inicial = None
        self.__sesion = None
        self.__tipo_recomendacion = None

    @classmethod
    def getInstancia(cls):
        if cls._SistemaRecomendacion__instancia is None:
            cls._SistemaRecomendacion__instancia = cls()
        
        return cls._SistemaRecomendacion__instancia
    
    def setEstrategia(self, e:EstrategiaBusqueda):
        if not isinstance(e, EstrategiaBusqueda):
            raise TypeError("e debe ser un objeto de la clase Estrategia Busqueda")
        
        self.__estrategia = e

    def setTipoRecomendacion(self, tipo:ElementoCatalogo):
        if not isinstance(tipo, ElementoCatalogo):
            raise TypeError("tipo debe ser un objeto de la clase ElementoCatalogo")
        
        self.__tipo_recomendacion = tipo

    def setSesion(self, s:Sesion):
        if not isinstance(s, Sesion):
            raise TypeError("s debe ser un objeto de la clase Sesion")
        
        self.__sesion = s

    def setManejador(self, m:Manejador):
        if not isinstance(m, Manejador):
            raise TypeError("m debe ser un objeto de la clase Manejador")
        
        self.__manejador_inicial = m

    async def procesarCancion(self, id:str, fecha_hora:date, catalogo:ServicioStreaming):
        if not isinstance(id, str):
            raise TypeError("id tiene que ser una cadena de texto")
        
        if not isinstance(fecha_hora, date):
            raise TypeError("fecha_hora debe ser una fecha")
        
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un objeto de la clase ServicioStreaming")
        
        if not self.__sesion:
            raise SesionError("NO hay ninguna sesion iniciada")
        
        cancion_encontrada = None
        for cancion in catalogo.getCanciones():
            if cancion._Cancion__id == id:
                cancion_encontrada = cancion

        if not cancion_encontrada:
            raise ValueError(f"No se encontro la cancion con ID: {id}")
        
        self.__sesion.agregarCancion(cancion_encontrada)

        if self.__manejador_inicial:
            self.__manejador_inicial.procesar(self.__sesion)

    def recomendar(self, catalogo:ServicioStreaming):
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un objeto de la clase ServicioStreaming")
        
        if not self.__estrategia or not self.__sesion:
            raise SesionError("Se deben inicializar los valores de estrategia y sesion")
        
        elemento_base = self.__estrategia.buscar(catalogo, self.__sesion)
        recomendacion = Recomendacion(elemento_base)

        if self.__tipo_recomendacion == Artista:
            recomendacion = RecomArtista(recomendacion, catalogo)
        
        elif self.__tipo_recomendacion == ListaReproduccion:
            recomendacion = RecomListaRepro(recomendacion, catalogo)

        return recomendacion.obtenerResultado()
