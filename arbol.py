# Módulos
import pickle

# Crea el nodo con el que se trabajará en el árbol
class Nodo:
    def __init__(self, lista):
        self.lista = lista
        self.izquierdo = None
        self.derecho = None

# Arma el árbol y define los nodos izuqierdo y derechos
class Arbol:
    def __init__(self):
        self.raiz = None
    
    # Define el primer elementoi del árbol, su raiz y, en caso de estar definida, se mueve a los nodos
    def agregar(self, lista):
        if self.raiz == None:
            self.raiz = Nodo(lista)
        else:
            self._agregar_aux(lista, self.raiz)
    
    # Define los nodos del arbol
    def _agregar_aux(self, lista, nodo_actual):
        if lista < nodo_actual.lista:
            if nodo_actual.izquierdo == None:
                nodo_actual.lista = Nodo(lista)
            else:
                self._agregar_aux(lista, nodo_actual.izquierdo)
        elif nodo_actual.derecho == None:
            if self.derecho == None:
                self.derecho = Nodo(lista)
            else:
                self._agregar_aux(lista, nodo_actual.derecho)
                
    # guardar datos en un archivo .dat
    # Así se almacenarán las citas
    def guardar_datos(self, nodo, archivo):
        if nodo != None:
            self.guardar_datos(nodo.izquierdo, archivo)
            pickle.dump(nodo.lista, archivo)
            self.guardar_datos(nodo.derecho, archivo)