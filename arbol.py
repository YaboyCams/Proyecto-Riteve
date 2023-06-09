# Módulos
import pickle


# Crea el nodo con el que se trabajará en el árbol
class Nodo:
    def __init__(self, lista):
        self.lista = lista
        self.izquierdo = None
        self.derecho = None
        self.cita = lista[1]
        self.placa = lista[4]

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
    def cambiar_estado(self, lista, argumento):
        return self.cambiar_estado_aux(self.raiz,lista,argumento)
    
    # Busca en los nados para cambiar
    def cambiar_estado_aux(self, nodo_actual, lista, argumento):
        if nodo_actual is None:
            return
        if lista == nodo_actual.lista:
            nodo_actual.lista[-1] = argumento
            # return nodo_actual.lista
        if lista < nodo_actual.lista:
            if nodo_actual.izquierdo is not None:
                return self.cambiar_estado_aux(nodo_actual.izquierdo, lista, argumento)
        elif nodo_actual.derecho is not None:
            return self.cambiar_estado_aux(nodo_actual.derecho, lista, argumento)
            
                
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
        
    # Buscar placa
    def buscar_placa(self, cita, placa_buscada):
        return self.buscar_placa_aux(cita, placa_buscada, self.raiz)
    
    # Busca bien en todo el árbol
    def buscar_placa_aux(self, cita, placa, nodo_actual):
        if nodo_actual is None:
            return
        if placa in nodo_actual.lista:
            return nodo_actual.cita
        elif cita < nodo_actual.cita:
            return self.buscar_nodos_aux(cita, nodo_actual.izquierdo)
        else:
            return self.buscar_nodos_aux(cita, nodo_actual.derecho)
    
    
