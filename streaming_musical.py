from abc import ABC, abstractmethod
from datetime import date
import random
from math import sqrt
import itertools

class DuplicatedError(Exception):
    '''Creamos una excepcion para cuando se producca un duplicado de valores'''
    pass

class SesionError(Exception):
    '''Creamos una excepcion para cuando se intente utilizar el resto de funciones del SistemaRecomendador sin crear antes una instancia de esta'''
    pass

class ElementoCatalogo(ABC):
    """Clase abstracta que define el objeto minimo que puede formar parte del catalogo"""
    @abstractmethod
    def obtenerCaracteristicas(self):
        """Metodo abstracto cuya implementacion queda delegada a sus hijos"""
        pass

class Cancion(ElementoCatalogo):
    """Clase que modela las canciones de todo el sistema recomendador; las canciones de los artistas, de las listas de reproduccion,...
       Contiene su id, sus caracteristicas sonoras y sentimentales, el titulo de la cancion y la fecha de creacion"""
    
    def __init__(self, id:str, c_sonoras:dict, c_sentimentales:dict, titulo:str, fecha_creacion: date):
        """Comprobamos que id sea una cadena de texto"""
        if not isinstance(id, str):
            raise TypeError("id tiene que ser una cadena de texto")
        
        """Comprobamos que las caracteristicas sonoras vengan guardadas en un diccionario"""
        if not isinstance(c_sonoras, dict):
            raise TypeError("c_sonoras debe ser un diccionario")
        
        """Comprobamos que las caracteristicas sentimentales vengan guardadas en un diccionario"""
        if not isinstance(c_sentimentales, dict):
            raise TypeError("c_sentimentales debe ser un diccionario")
        
        """Comprobamos que el titulo sea una cadena de texto"""
        if not isinstance(titulo, str):
            raise TypeError("titulo debe ser una cadena de texto")
        
        """Comprobamos que la fecha de creacion sea una fecha"""
        if not isinstance(fecha_creacion, date):
            raise TypeError("fecha_creacion debe ser una fecha")
        
        self.__id = id
        self.__c_sonoras = c_sonoras
        self.__c_sentimentales = c_sentimentales
        self.__titulo = titulo
        self.__fecha_creacion = fecha_creacion       

    def obtenerCaracteristicas(self) -> dict:
        """Funcion que devuelve las caracteristicas sonoras y sentimentales en un unico diccionario"""
        
        solucion = {}
        solucion["Caracteristicas Sonoras"] = self.__c_sonoras
        solucion["Caracteristicas Sentimentales"] = self.__c_sentimentales
        return solucion
    
class Artista(ElementoCatalogo):
    '''Clase que modela a los cantantes existentes en una plataforma de servicio de streaming
       Contiene el nombre del artista, sus canciones y su fecha de nacimiento '''
    
    def __init__(self, nombre:str, canciones:list[Cancion], fecha_nacimiento:date):
        '''Comprobamos que nombre sea una cadena de texto'''
        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser una cadena de texto")
        
        '''Comprobamos que canciones sea una lista'''
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")
        
        '''Comprobamos que los elementos de la lista canciones sean objetos de la clase Cancion'''
        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben objetos de la clase Cancion")  
        
        '''Comprobamos que la fecha de nacimiento sea una fecha'''       
        if not isinstance(fecha_nacimiento, date):
            raise TypeError("fecha_nacimiento debe ser una fecha de nacimiento")

        self.__nombre = nombre
        self.__canciones = canciones
        self.__fecha_nacimiento = fecha_nacimiento

    def obtenerCanciones(self) -> list:
        '''Funcion que devuelve una lista de las canciones del artista'''
        return self.__canciones

    def obtenerCaracteristicas(self) -> dict:
        '''Funcion que devuelve las caracteristicas sonoras y sentimentales de las canciones del artista'''
        solucion = {}
        for cancion in self.__canciones:            
            titulo = cancion._Cancion__titulo 
            solucion[titulo] = cancion.obtenerCaracteristicas()
            
        return solucion
    
class ListaReproduccion:
    '''Clase que modela las listas de reproduccion que existen en una plataforma de servicio de streaming
       Contiene las canciones de la lista, su nombre y su fecha de creacion'''
    def __init__(self, canciones:list[Cancion], nombre:str, fecha_creacion:date):
        '''Comprobamos que canciones es una lista'''
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        '''Comprobamos que los elementos de la lista canciones sean objetos de la clase Cancion'''
        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben objetos de la clase cancion") 
        
        '''Comprobamos que nombre es una cadena de texto'''
        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser una cadena de texto")
        
        '''Comprobamos que fecha_creacion sea una fecha'''
        if not isinstance(fecha_creacion, date):
            raise TypeError("fecha_creacion debe ser una fecha")
        
        self.__canciones = canciones
        self.__nombre = nombre
        self.__fecha_creacion = fecha_creacion

    def obtenerCanciones(self) -> list:
        '''Funcion que devuelve las canciones de una lista de reproduccion'''
        return self.__canciones

    def obtenerCaracteristicas(self) -> dict:
        '''Funcion que devuelve las caracteristicas sonoras y sentimentales de las canciones de una lista de reproduccion'''
        solucion = {}
        for cancion in self.__canciones:            
            titulo = cancion._Cancion__titulo 
            solucion[titulo] = cancion.obtenerCaracteristicas()
            
        return solucion

class Sesion:
    '''Clase que modela una sesion iniciada de un usuario concreto del servicio de streaming
       Contiene una lista de las canciones escuchadas por el usuario'''
    
    def __init__(self, canciones:list[Cancion]):
        '''Comprobamos que canciones sea una lista'''
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        '''Comprobamos que los objetos de la lista canciones sean objetos de la clase Cancion'''
        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser objetos de la clase Cancion")  
            
        self.__canciones = canciones
        self.__media_sonora = 0
        self.__media_sentimental = 0
        self.__desviacion_sonora = 0
        self.__desviacion_sentimental = 0

    def agregarCancion(self, c):
        '''Funcion que toma una cancion y la añade a las canciones escuchadas de la sesion'''

        '''Comprobamos que c sea un objeto de la clase Cancion'''
        if not isinstance(c, Cancion):
            raise TypeError("c debe pertenecer a la clase Cancion")
        
        for i in self.__canciones:
            if i == c:
                raise DuplicatedError("Esa cancion ya se encuentra en la lista de canciones")
            
        self.__canciones.append(c)

    def obtenerCanciones(self) -> list:
        '''Funcion que devuelve una lista con las canciones escuchadas esa sesion'''
        return self.__canciones
    
    def obtenerCaracteristicas(self, m:"Manejador") -> dict: 
        '''Funcion que devuelve un diccionario con las caracteristicas sonoras y sentimentales de la sesion
           El manejador que pasamos como argumento se encargara de calcular las caracteristicas de la sesion'''
        
        '''Comprobamos que m sea un objeto de la clase Manejador'''
        if not isinstance(m, Manejador):
            raise TypeError("m debe pertenecer a la clase Manejador")
        
        '''Procesamo los atributos para realizar los calculos necesarios'''
        m.procesar(self) 
        return {
        "Media Sonora":self.__media_sonora,
        "Media Sentimental" : self.__media_sentimental,
        "Desviacion Sonora":self.__desviacion_sonora,
        "Desviacion Sentimental":self.__desviacion_sentimental
        }

class Manejador(ABC):
    '''Clase que modela el manejador principal que se encargara de gestionar a los manejadores concretos
       Contiene una referencia al manejador concreto al que se va a dirigir, para lo cual, inicializamos el atributo en None'''

    def __init__(self, siguiente: "Manejador" = None):
        '''Comprobamos que siguiente sea un objeto de la clase Manejador'''
        if siguiente is not None and not isinstance(siguiente, Manejador):
            raise TypeError("siguiente debe ser un objeto de la clase Manejador")
        
        self._siguiente = siguiente

    def setSiguiente(self, m: "Manejador") -> "Manejador":
        """Permite cambiar o establecer el siguiente manejador en la cadena."""
        if not isinstance(m, Manejador):
            raise TypeError("El nuevo manejador debe pertenecer a la clase Manejador")
        
        self._siguiente = m
        return m

    @abstractmethod
    def procesar(self, sesion:Sesion):
        '''Funcion que se encargara de realizar los calculos referentes a las caracteristicas sonoras y sentimentales
           Esta funcion se pasara a los hijos'''

        '''Comprobamos que sesion sea un objeto de la clase Sesion'''
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe pertenecer a la clase Sesion")

        if self._siguiente:
            return self._siguiente.procesar(sesion)
        
        return None

class ManejadorSonoro(Manejador):
    '''Clase hija de la clase Manejador que modela el manejador concreto que se encargara de las caracteristicas sonoras'''

    def procesar(self, s: Sesion):
        '''Funcion que se encarga de gestionar los calculos referentes a la caracteristica sonoras de una sesion concreta y devolverlos'''
        
        '''Comprobamos que s sea un objeto de la clase Sesion'''
        if not isinstance(s, Sesion):
            raise TypeError("s debe ser un objeto de la clase Sesion")
        
        canciones_sesion = s.obtenerCanciones()

        if canciones_sesion:
            media = self._calcularMedia(canciones_sesion)
            desviacion = self._calcularDesviacion(canciones_sesion, media)
            
            s._Sesion__media_sonora = media
            s._Sesion__desviacion_sonora = desviacion
        
        return super().procesar(s)

    def _calcularMedia(self, lista_canciones:list) -> float:
        '''Funcion que se encargara de calcular la media sonora de todas las canciones de una lista'''

        '''Comprobamos que lista_canciones sea una lista'''
        if not isinstance(lista_canciones, list):
            raise TypeError("lista_canciones debe ser una lista")
        
        '''Inicializamos la suma en 0 y creamos una variable para contar el numero de canciones'''
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
        '''Funcion que se encarga de calcular la desviacion sonora de una lista de cancion, tomando a su vez la media de esta'''

        '''Comprobamos que lista_canciones sea una lista'''
        if not isinstance(lista_canciones, list):
            raise TypeError("lista_canciones debe ser una lista")
        
        '''Comprobamos que media sea un valor decimal'''
        if not isinstance(media, float):
            raise TypeError("media debe ser un numero decimal")
        
        '''Inicializamos la suma de los cuadrados en 0 y creamos una variable para contar el numero de canciones'''    
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
    '''Clase hija de la clase Manejador que modela el manejador concreto que se encargara de las caracteristicas sentimentales'''

    def procesar(self, s: Sesion):
        '''Funcion que se encarga de gestionar los calculos referentes a la caracteristica sentimentales de una sesion concreta y devolverlos'''
        
        '''Comprobamos que s sea un objeto de la clase Sesion'''
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
        '''Funcion que se encargara de calcular la media senitmental de todas las canciones de una lista'''

        '''Comprobamos que lista_canciones sea una lista'''
        if not isinstance(lista_canciones, list):
            raise TypeError("lista_canciones debe ser una lista")
        
        '''Inicializamos la suma en 0 y creamos una variable para contar el numero de canciones'''
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
        '''Funcion que se encarga de calcular la desviacion sentimental de una lista de cancion, tomando a su vez la media de esta'''

        '''Comprobamos que lista_canciones sea una lista'''
        if not isinstance(lista_canciones, list):
            raise TypeError("lista_canciones debe ser una lista")
        
        '''Comprobamos que media sea un valor decimal'''
        if not isinstance(media, float):
            raise TypeError("media debe ser un numero decimal")
            
        '''Inicializamos la suma de los cuadrados en 0 y creamos una variable para contar el numero de canciones'''    
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
    '''Clase que modela los servicios que presta una plataforma de streaming
       Contiene las canciones, artistas y listas de reproduccion que hay en la plataforma'''
    
    def __init__(self, canciones:list[Cancion], artistas:list[Artista], listas_repro:list[ListaReproduccion]):
        '''Comprobamos que canciones sea una lista'''
        if not isinstance(canciones, list):
            raise TypeError("canciones debe ser una lista")

        '''Comprobamos que los objetos de la lista canciones sean objetos de la clase Cancion'''
        if not all(isinstance(c, Cancion) for c in canciones):
            raise TypeError("Todos los elementos deben ser objetos de la clase Cancion") 

        '''Comprobamos que artistas sea una lista'''
        if not isinstance(artistas, list):
            raise TypeError("artistas debe ser una lista")

        '''Comprobamos que los elementos de la lista artistas sean objetos de la clase Artista'''

        if not all(isinstance(a, Artista) for a in artistas):
            raise TypeError("Todos los elementos deben ser artistas") 

        '''Comprobamos que listas_repro sea una lista'''
        if not isinstance(listas_repro, list):
            raise TypeError("listas_repro debe ser una lista")

        '''Comprobamos que los elementos de listas_repro sean objetos de la clase ListaReproduccion'''
        if not all(isinstance(l, ListaReproduccion) for l in listas_repro):
            raise TypeError("Todos los elementos deben ser listas de reproduccion")
         
        self.__canciones = canciones
        self.__artistas = artistas
        self.__listas_repro = listas_repro

    def getCanciones(self) -> list:
        '''Funcion que devuelve una lista con las canciones existentes'''
        return self.__canciones
    
    def getArtistas(self) -> list:
        '''Funcion que devuelve una lista con los artistas existentes'''
        return self.__artistas
    
    def getListasRepro(self) -> list:
        '''Funcion que devuelve una lista con las listas de reproduccion existentes'''
        return self.__listas_repro

class EstrategiaBusqueda(ABC):
    '''Clase que modela la estrategia de busqueda que se aplicara a la hora de realizar la recomendacion al usuario'''
    
    @abstractmethod
    def buscar(self, catalogo:ServicioStreaming, sesion:Sesion):
        '''Funcion que se encarga, dados un catalogo y una sesion, de buscar canciones que cumplan los requisitos impuestos por el usuario'''

        '''Comprobamos que catalogo sea un objeto de la clase ServicioStreaming'''
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un servicio de streaming")
        
        '''Comprobamos que sesion sea un objeto de la calse Sesion'''
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe ser una sesion")
        
        pass

class Alfabetico(EstrategiaBusqueda):
    '''Clase hija de la clase EstrategiaBusqueda que modela una busqueda en la que se ordenan los elementos por orden alfabetico'''
    def buscar(self, catalogo:ServicioStreaming, sesion:Sesion):
        '''Funcion que se encarga dados un catalogo y una sesion, de buscar los elementos que coinciden con las caracteristicas dadas'''
        
        '''Comprobamos que catalogo sea un objeto de la clase ServicioStreaming'''
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe pertenecer a la clase ServicioStreaming")
        
        '''Comprobamos que sesion sea un objeto de la clase Sesion'''
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe pertenecer a la clase Sesion")
        
        '''Creamos una variable que contenga todas las canciones de los artistas y de las listas'''
        items_catalogo = []
        items_catalogo.extend(catalogo.getCanciones())
        items_catalogo.extend(catalogo.getArtistas())
        items_catalogo.extend(catalogo.getListasRepro())

        '''Ordenamos las canciones alfabeticamente'''
        items_ordenados = sorted(
            items_catalogo,
            key=lambda x: (
                x._Cancion__titulo.lower() if isinstance(x, Cancion) else
                x._Artista__nombre.lower() if isinstance(x, Artista) else
                x._ListaReproduccion__nombre.lower() if isinstance(x, ListaReproduccion) else ""
            )
        )

        estadisticas_sesion = sesion.obtenerCaracteristicas(ManejadorSonoro(ManejadorSentimental()))
        canciones_escuchadas = sesion.obtenerCanciones()

        def coincide(item) -> bool:
            """
            Valida si un ítem cumple con los requisitos sonoros y sentimentales.
            Si el ítem es un Artista o Lista, se validan todas sus canciones.
            """
            if isinstance(item, Cancion):
                if item in canciones_escuchadas:
                    return False
                
                canciones_a_validar = [item]

            elif isinstance(item, (Artista, ListaReproduccion)):
                canciones_a_validar = item.obtenerCanciones()

            else:
                return False

            for cancion in canciones_a_validar:
                caract = cancion.obtenerCaracteristicas()
                sonoras = caract.get("Caracteristicas Sonoras", {})
                sentimentales = caract.get("Caracteristicas Sentimentales", {})

                for valor in sonoras.values():
                    media = estadisticas_sesion.get("Media Sonora", 0)
                    desv = estadisticas_sesion.get("Desviacion Sonora", 0) + 0.1
                    if abs(valor - media) > desv:
                        return False
                
                for valor in sentimentales.values():
                    media = estadisticas_sesion.get("Media Sentimental", 0)
                    desv = estadisticas_sesion.get("Desviacion Sentimental", 0) + 0.1
                    if abs(valor - media) > desv:
                        return False
            
            return True

        coincidentes = filter(coincide, items_ordenados)

        return next(coincidentes, None)
        
class Temporal(EstrategiaBusqueda):
    '''Clase hija de la clase EstrategiaBusqueda que modela una busqueda en la que se ordenan los elementos por orden temporal'''
    def buscar(self, catalogo: ServicioStreaming, sesion: Sesion):
        '''Funcion que se encarga dados un catalogo y una sesion, de buscar los elementos que coinciden con las caracteristicas dadas'''
        
        '''Comprobamos que catalogo sea un objeto de la clase ServicioStreaming'''
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe pertenecer a la clase ServicioStreaming")
        
        '''Comprobamos que sesion sea un objeto de la clase Sesion'''
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

        def coincide(item) -> bool:
            '''Funcion que se encarga de encontrar los elementos que coincidan con las caracteristicas '''

            if isinstance(item, Cancion):
                canciones_a_validar = [item]

            elif isinstance(item, Artista) or isinstance(item, ListaReproduccion):
                canciones_a_validar = item.obtenerCanciones()
            
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

        return None

class Aleatorio(EstrategiaBusqueda):
    '''Clase hija de la clase EstrategiaBusqueda que modela una busqueda en la que se ordenan los elementos aleatoriamente'''

    def buscar(self, catalogo: ServicioStreaming, sesion: Sesion):
        '''Funcion que se encarga dados un catalogo y una sesion, de buscar los elementos que coinciden con las caracteristicas dadas'''

        '''Comprobamos que catalogo sea un objeto de la clase ServicioStreaming'''
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe pertenecer a la clase ServicioStreaming")
        
        '''Comprobamos que sesion es un objeto de la clase Sesion'''
        if not isinstance(sesion, Sesion):
            raise TypeError("sesion debe pertenecer a la clase Sesion")

        canciones_lista = list(set(itertools.chain(
            catalogo.getCanciones(),
            *(artista.obtenerCanciones() for artista in catalogo.getArtistas()),
            *(lista.obtenerCanciones() for lista in catalogo.getListasRepro())
        )))
        
        random.shuffle(canciones_lista) 

        estadisticas_sesion = sesion.obtenerCaracteristicas(ManejadorSonoro(ManejadorSentimental()))

        def coincide(cancion) -> bool:
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
    '''Clase que modela una recomendacion de una plataforma de streaming a un usuario
       Contiene un elemento del catalogo, que puede ser una cancion, un artista o una lista de reproduccion'''
    
    def __init__(self, elemento:ElementoCatalogo):
        '''Comprobamos que elemento sea un objeto de la clase ElementoCatalogo'''
        if not isinstance(elemento, ElementoCatalogo):
            raise TypeError("elemento debe ser un elemento del catalogo")
        
        self._elemento = elemento

    def obtenerResultado(self) -> ElementoCatalogo:
        '''Funcion que devuelve el elemento del catalogo recomendado'''
        return self._elemento

class DecoradorRecom(Recomendacion):
    '''Clase hija de Recomendacion que se encarga de gestionar a los decoradores concretos del sistema de recomendacion
       Contiene una recomendacion del recomendador'''
    
    def __init__(self, recomendacion:Recomendacion):
        '''Comprobamos que recomendacion sea un objeto de la clase Recomendacion'''

        if not isinstance(recomendacion, Recomendacion):
            raise TypeError("recomendacion debe ser un objeto de la clase Recomendacion")
        
        super().__init__(recomendacion._elemento)
        
        self.__recomendacion = recomendacion

    def obtenerResultado(self) -> ElementoCatalogo:
        '''Funcion que nos devuelve el elemento del decorador'''
        return self.__recomendacion.obtenerResultado()

class RecomArtista(DecoradorRecom):
    '''Clase hija de DecoradorRecom que se encarga de modelar la recomendacion de un artista
       Contiene una recomendacion y el catalogo de elementos de la plataforma de streaming'''
    
    def __init__(self, recomendacion:Recomendacion, catalogo:ServicioStreaming):
        '''Comprobamos que recomendacion sea un objeto de la clase Recomendacion'''
        if not isinstance(recomendacion, Recomendacion):
            raise TypeError("recomendacion tiene que ser un objeto de la clase Recomendacion")
        
        '''Comprobamos que catalogo sea un objeto de la clase ServicioStreaming'''
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un objeto de la clase ServicioStreaming")
        
        super().__init__(recomendacion)
        self.__catalogo = catalogo

    def obtenerResultado(self):
        '''Funcion que devuelve el artista recomendado'''
        cancion = super().obtenerResultado()
        if not cancion:
            return None

        for artista in self.__catalogo.getArtistas():
            for c in artista.obtenerCanciones():
                if c._Cancion__id == cancion._Cancion__id:
                    return artista
        
        return cancion

class RecomListaRepro(DecoradorRecom):
    '''Clase hija de DecoradorRecom que se encarga de modelar la recomendacion de una lista de reproduccion
       Contiene una recomendacion y el catalogo de elementos de la plataforma de streaming'''
    
    def __init__(self, recomendacion:Recomendacion, catalogo:ServicioStreaming):
        '''Comprobamos que recomendacion es un objeto de la clase Recomendacion'''
        if not isinstance(recomendacion, Recomendacion):
            raise TypeError("recomendacion tiene que ser un objeto de la clase Recomendacion")
        
        '''Comprobamos que catalogo sea un objeto de la clase ServicioStreaming'''
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un objeto de la clase ServicioStreaming")
        
        super().__init__(recomendacion)
        self.__catalogo = catalogo

    def obtenerResultado(self):
        '''Funcion que devuelve la lista de reproduccion recomendada'''
        cancion = super().obtenerResultado()

        for lista in self.__catalogo.getListasRepro():
            if cancion in lista.obtenerCanciones():
                return lista
        
        return cancion

class SistemaRecomendacion:
    '''Clase principal del sistema que modela el sistema recomendador de una plataforma de streaming'''
    __instancia = None

    def __init__(self):
        if SistemaRecomendacion.__instancia is not None:
            raise SesionError("NO hay ninguna sesion iniciada")       
        
        self.__estrategia = None
        self.__manejador_inicial = None
        self.__sesion = None
        self.__tipo_recomendacion = None

    @classmethod
    def getInstancia(cls):
        '''Funcion que se encarga de inicializar la instancia de la clase'''
        if cls.__instancia is None:
            cls.__instancia = cls()
        
        return cls.__instancia
    
    def setEstrategia(self, e:EstrategiaBusqueda):
        '''Funcion que defiene la estrategia de busqueda que se va a seguir'''
        
        '''Comprobamos que e sea un objeto de la clase EstrategiaBusqueda'''
        if not isinstance(e, EstrategiaBusqueda):
            raise TypeError("e debe ser un objeto de la clase Estrategia Busqueda")
        
        self.__estrategia = e

    def setTipoRecomendacion(self, tipo:ElementoCatalogo):
        '''Funcion que define la recomendacio que se va a seguir'''
        
        '''Comprobamos que tipo sea un objeto de alguna de las subclases de ElementoCatalogo'''
        if not issubclass(tipo, ElementoCatalogo):
            raise TypeError("tipo debe ser un objeto de alguna subclase de ElementoCatalogo")
        
        self.__tipo_recomendacion = tipo

    def setSesion(self, s:Sesion):
        '''Funcion que define cual sera la sesion con la que vamos a trabajar'''
        
        '''Comprobamos que s sea un objeto de la clase Sesion'''
        if not isinstance(s, Sesion):
            raise TypeError("s debe ser un objeto de la clase Sesion")
        
        self.__sesion = s

    def setManejador(self, m:Manejador):
        '''Funcion que define el manejador que se va a emplear en la recomendacion'''
        
        '''Comprobamos que m sea un objeto de la clase Manejador'''
        if not isinstance(m, Manejador):
            raise TypeError("m debe ser un objeto de la clase Manejador")
        
        self.__manejador_inicial = m

    async def procesarCancion(self, id:str, fecha:date, catalogo:ServicioStreaming):
        '''Funcion que se encargara de, dadas unas ciertas caracteristicas, procesar la cancion de un catalogo que coincida con las caracteristicas
           Contiene un id, una fecha y un catalogo de elementos '''
        
        '''Comprobamos que id sea una cadena de texto'''
        if not isinstance(id, str):
            raise TypeError("id tiene que ser una cadena de texto")
        
        '''Comprobamos que fecha sea una fecha'''
        if not isinstance(fecha, date):
            raise TypeError("fecha debe ser una fecha")
        
        '''Comprobamos que catalogo sea un objeto de la clase ServicioStreaming'''
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un objeto de la clase ServicioStreaming")
        
        '''Comprobamos que sesion este inicializada'''
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
        '''Funcion que se encarga de recomendar un elemeto de un catalogo'''
        
        '''Comprobamos que catalogo sea un objeto de la clase ServicioStreaming'''
        if not isinstance(catalogo, ServicioStreaming):
            raise TypeError("catalogo debe ser un objeto de la clase ServicioStreaming")
        
        '''Comprobamos que las variables estrategia y sesion esten inicializadas'''
        if not self.__estrategia or not self.__sesion:
            raise SesionError("Se deben inicializar los valores de estrategia y sesion")
        
        elemento_base = self.__estrategia.buscar(catalogo, self.__sesion)

        if not elemento_base:
            return None
        
        recomendacion = Recomendacion(elemento_base)

        if self.__tipo_recomendacion == Artista:
            recomendacion = RecomArtista(recomendacion, catalogo)
        
        elif self.__tipo_recomendacion == ListaReproduccion:
            recomendacion = RecomListaRepro(recomendacion, catalogo)

        return recomendacion.obtenerResultado()