# Módulos
import pickle

# Crea el nodo con el que se trabajará en el árbol
class Nodo:
    def __init__(self, lista):
        self.lista = lista
        self.izquierdo = None
        self.derecho = None

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
    def guardar_datos(self, nodo, archivo):
        if nodo is not None:
            self.guardar_datos(nodo.izquierdo, archivo)
            pickle.dump(nodo.lista, archivo)
            self.guardar_datos(nodo.derecho, archivo)
