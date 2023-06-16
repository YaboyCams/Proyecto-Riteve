# Módulos
import pickle

# Crea el nodo con el que se trabajará en el árbol
class Nodo:
    def __init__(self, lista):
        self.lista = lista
        self.izquierdo = None
        self.derecho = None
        self.cita = lista[1]

# Arma el árbol y define los nodos izquierdo y derecho
class Arbol:
    def __init__(self):
        self.raiz = None
    
    # Define el primer elemento del árbol, su raíz y, en caso de estar definida, se mueve a los nodos
    def agregar(self, lista):
        if self.raiz is None:
            self.raiz = Nodo(lista)
        else:
            self.agregar_aux(lista, self.raiz)
    
    # Define los nodos del árbol
    def agregar_aux(self, lista, nodo_actual):
        if lista < nodo_actual.lista:
            if nodo_actual.izquierdo is None:
                nodo_actual.izquierdo = Nodo(lista)
            else:
                self.agregar_aux(lista, nodo_actual.izquierdo)
        else:
            if nodo_actual.derecho is None:
                nodo_actual.derecho = Nodo(lista)
            else:
                self.agregar_aux(lista, nodo_actual.derecho)
                
    # Guardar datos en un archivo .dat
    # Así se almacenarán las citas
    def guardar_datos(self, archivo):
        return self.guardar_datos_aux(self.raiz, archivo)
    
    def guardar_datos_aux(self, nodo, archivo):
        if nodo is not None:
            self.guardar_datos_aux(nodo.izquierdo, archivo)
            pickle.dump(nodo.lista, archivo)
            self.guardar_datos_aux(nodo.derecho, archivo)
            
    # Cambiar datos
    def cambiar_nodo(self, lista, argumento):
        if self.raiz is not None and self.raiz.cita == lista[1]:
            self.raiz.lista[-1] == argumento
        else:
            self.cambiar_aux(lista, self.raiz)
    
    # Busca en los nados para cambiar
    def cambiar_aux(self, lista, nodo_actual, argumento):
        if nodo_actual is None:
            return
        if nodo_actual.izquierdo is not None and self.nodo_actual.izquierdo.cita == lista[1]:
            nodo_actual.izquierdo.lista[-1] = argumento
        elif self.nodo_actual.derecho.cita == lista[1]:
            nodo_actual.derecho.lista[-1] = argumento
        elif lista < nodo_actual.lista:
            self.cambiar_aux(lista, nodo_actual.izquierdo, argumento)
        else:
            self.cambiar_aux(lista, nodo_actual.derecho, argumento)
            
                
    # Buscar nodos
    def buscar_nodos(self, buscado):
        return self.buscar_nodos_aux(buscado, self.raiz)
    
    # Busca bien en todo el árbol
    def buscar_nodos_aux(self, cita, nodo_actual):
        if nodo_actual is None:
            return
        if nodo_actual.cita == cita:
            return nodo_actual.lista
        elif cita < nodo_actual.cita:
            return self.buscar_nodos_aux(cita, nodo_actual.izquierdo)
        else:
            return self.buscar_nodos_aux(cita, nodo_actual.derecho)