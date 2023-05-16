from prettytable import PrettyTable
from collections import deque
from string_parser import *


class grammar():
    def __init__(self, nonterminals, terminals, productions, start):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start = start

    def remove_left_recursion(self):
        pass


class Vertex:
    def __init__(self, id, items, who_items):
        self.id = id
        self.items = items
        self.collections = []
        self.neighbours = []
        self.who_collections = []
        self.who_items = who_items

    def add_neigh(self, v):
        if v not in self.neighbours:
            self.neighbours.append(v)


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex (self, v, items, who_items):
        if v not in self.vertices:
            self.vertices[v] = Vertex(v, items, who_items)

    def add_edge(self, a, b, weight):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].add_neigh((b,weight))

## Top-Down Parsing Functions (Predictive Parsing)

def FIRST(G, symbol, P, FIRST_SET):
    position = 0
    list=[]

    for i in range(len(P)):
        list.append([])

    value = False # controlador para validar si una producción deriva en epsilon, así evitar eliminarlo del conjunto en caso de que pertenezca.
    
    for production in P: # para cada produccion en la lista de producciones:
        counter = 0 # permite saber si se recorrió toda la producción actual, para determinar que la misma deriva en epsilon.
        for element in production: #para cada letra de la produccion:
            if element == 'Ɛ':
                list[position].append('Ɛ')
            if element in G.terminals: #si está en el conjunto de terminales, se agrega el terminal al first y se para de evaluar la produccion actual del no terminal.
                FIRST_SET[symbol].add(element)
                list[position].append(element)
                break
            if element in G.nonterminals: # si está en el conjunto de no terminales, se ingresa al no terminal y se calcula el first al mismo (recursivamente).
                counter += 1
                if FIRST(G, element, G.productions[element], FIRST_SET)[0]: # si el llamado es true, significa que el no terminal tiene en su first epsilon y por lo tanto, se debe seguir evaluando la cadena.
                    FIRST_SET[symbol] = FIRST_SET[symbol].union(FIRST_SET[element])
                    for i in FIRST_SET[element]:
                        list[position].append(i)
                else: # si el llamado es false, significa que el no terminal no tiene epsilon en su first, y por lo tanto, no se debe seguir evaluando la cadena.
                    FIRST_SET[symbol] = FIRST_SET[symbol].union(FIRST_SET[element])
                    for i in FIRST_SET[element]:
                        list[position].append(i)
                    break
                if 'Ɛ' in FIRST_SET[symbol] and value == False: # se elimina el epsilon del first de el no terminal actual, ya que el mismo solo deriva en epsilon cuando en sus producciones tiene epsilon o se recorrio toda la produccion y cada letra deriva en epsilon (se evalua después).
                    FIRST_SET[symbol].remove('Ɛ')
                    list[position].pop(list[position].index("Ɛ"))
                if counter == len(production): # si el contador es igual al largo de la produccion, significa que se recorrio toda la cadena.
                    if 'Ɛ' in FIRST_SET[element]: # si en el first de mi ultimo elemento está epsilon, mi cadena puede derivar en epsilon, ya que si recorrimos toda la cadena es porque cada elemento de la misma deriva en epsilon.
                        FIRST_SET[symbol].add('Ɛ')
                        list[position].append('Ɛ')
                        value = True # se cambia el valor del controlador para no eliminar el epsilon agregado en caso de que existan más producciones con el simbolo no terminal actual.
        position+=1

    if 'Ɛ' in P:
        FIRST_SET[symbol].add('Ɛ')
    if 'Ɛ'in FIRST_SET[symbol]: ## condición del llamado recursivo, con lo que se determina si el anterior llamado recursivo debe continuar evaluando la cadena o no.
        return True, list
    else:
        return False, list
    

def FOLLOW(FIRST_SET, G, symbol, FOLLOW_SET):
    for no_terminal in G.productions: # para cada no terminal en el conjunto de producciones (S, A, B, C..).
        counter = 0 #contador que permité identificar si todos los terminos derivan en epsilon hasta el final de la cadena, y por lo tanto, se debe calcular el follow de quien dicha cadena esta derivando.
        for production in G.productions[no_terminal]: # para cada produccion en la lista de producciones del no terminal (ABCDE, a, b, Ɛ).
            count = production.count(symbol) # contador que nos permite identificar cuantas veces esta ese no terminal en la cadena, para asi, calcularle el follow cada vez que aparezca.
            if count >= 1: # si el no terminal se encuentra en la cadena: 
                index = -1 # permite actualizar la posición en caso de que exista mas de una ocurrencia del no terminal en dicha cadena. (asi ignoramos el que ya se evaluo, y continuamos con la siguiente aparicion).
                for i in range(count): # para cada una de las apariciones:
                    index = production.find(symbol, index+1) # nos ubicamos en la aparicion, y actualizamos el valor del index para la siguiente ocurrencia en caso de existir.
                    if index != -1: # condición para que el index no se resetee una vez se encuentren las ocurrencias del no terminal.
                        for next in production[index+1:]: # para cada uno de los caracteres siguientes a ese no terminal en mi cadena:
                            if next in G.terminals: # si el siguiente es un terminal, lo añade al follow del no terminal actual y deja de evaluar los que siguen .
                                FOLLOW_SET[symbol].add(next)
                                break
                            if next in G.nonterminals: # si el siguiente es un no terminal:
                                FOLLOW_SET[symbol] = FOLLOW_SET[symbol].union(FIRST_SET[next]) # se añade a mi conjunto follow del no terminal actual, el first de mi no terminal siguiente.
                                if 'Ɛ' in FIRST_SET[next]: # si epsilon esta en el first de mi no terminal siguiente, seguimos evaluando el resto de elementos de la cadena, sumamos uno al contador y eliminamos del follow de mi no terminal actual el epsilon que habiamos agregado.
                                    counter += 1
                                    FOLLOW_SET[symbol].remove('Ɛ')
                                else: # paramos de evaluar esa cadena.
                                    break
                        if counter == len(production[index+1:]): # si el contador es igual a la cantidad de siguientes que habian a mi no terminal, significa que me encuentro en el final de la cadena, y debo utilizar la propiedad 3, uniendo el follow de mi no terminal actual con el de el no terminal de quien esta derivando la cadena.
                            if not len(FOLLOW_SET[no_terminal]): # evita la recursion infinita, si estoy buscando el follow de ese elemento y no existe, hago el llamado y agrego al follow de mi actual, el follow del que estoy derivando (que se encuentra en el llamado recursivo).
                                FOLLOW(FIRST_SET, G, no_terminal, FOLLOW_SET)
                                FOLLOW_SET[symbol] = FOLLOW_SET[symbol].union(FOLLOW_SET[no_terminal])
                            else: # si el follow del que estoy derivando ya tiene elementos, hago la union sin hacer el llamado recursivo.
                                FOLLOW_SET[symbol] = FOLLOW_SET[symbol].union(FOLLOW_SET[no_terminal])
                    else: #deje de buscar cuando no existan mas apariciones de el no terminal.
                        break


def give_positions(keys, true_false_terminal):
    dictionary = {} # diccionario donde se guardará como key el terminal o no terminal y como value el numero asignado (para manejar la tabla con posiciones numericas)
    count = 0 # valor asignado a cada terminal o no terminal 
    
    for i in keys: # se arma el diccionario con la key y el value correspondiente
        dictionary[i] = count
        count+=1
    
    if true_false_terminal: # si es para asignar posicion a terminales, se añade el simbolo $ que tambien hace parte de la tabla
        dictionary["$"] = count
    
    return dictionary #se devuelve el diccionario


def print_table(table, positions_terminals, positions_nonterminals): 
    pretty_table = PrettyTable() #tabla a imprimir
    pretty_table.field_names = [""] + list(positions_terminals.keys())# definicion de las columnas
    table_2 = table.copy()
    
    for i in range(len(table_2)): #definicion de filas, agrego el no terminal correspondiente
        table_2[i] = deque(table_2[i])
        table_2[i].appendleft(list(positions_nonterminals.keys())[i])
        table_2[i] = list(table_2[i])
    
    for i in range(len(table_2)): # agrego cada una de las filas a la tabla pretty_table
        row = table_2[i]
        pretty_table.add_row(row)
    
    print("Predictive Parsing Table:" + "\n")
    print(pretty_table) #imprimó la tabla


def predictive_table(G, FIRST_SET_STRINGS, FOLLOW_SET):
    positions_nonterminals = give_positions(G.nonterminals, False) # definición del numero para cada no terminal.
    positions_terminals = give_positions(G.terminals, True) # definicion de la posicion de cada terminal.
    table = [] # tabla donde se van a almacenar los valores.
    
    for i in range(len(G.nonterminals)): # creo la tabla en un principio con todos sus valores en infinito (que en esa posicion x,y no tiene un dato relacionado).
        table.append(["∞"]*(len(G.terminals)+1))
    
    for i in G.nonterminals: # asigno los valores correspondientes en la posicion x,y, para cada uno de los no terminales (filas):
        for j in range(len(G.productions[i])): # para cada una de las producciones de ese no terminal:
            for k in FIRST_SET_STRINGS[i][j]: # me paro en la lista del first de esa cadena (producción).
                if k != "Ɛ": # si el elemento del first de la cadena es distinto de epsilon:
                    if table[positions_nonterminals[i]][positions_terminals[k]] == "∞":
                        table[positions_nonterminals[i]][positions_terminals[k]] = G.productions[i][j] # en la fila del no terminal, y en la columna del terminal, agrego la producción (cadena correspondiente al first).
                    else:
                        return False
                else:
                    for z in FOLLOW_SET[i]: #si es epsilon, para cada uno de los elementos del follow agrego la derivacion del epsilon.
                        if table[positions_nonterminals[i]][positions_terminals[z]] == "∞":
                            table[positions_nonterminals[i]][positions_terminals[z]] = "Ɛ"
                        else:
                            return False
    
    print_table(table, positions_terminals, positions_nonterminals) # llamo a la función para imprimir la tabla.
    string_input_top_down(G, table, positions_terminals,positions_nonterminals) # enviamos los datos para analizar cadenas.

## Bottom-Up Parsing Functions

def next_point(element): # hacer avanzar el punto de la produccion.
    position = element.find("•") # encuentro donde esta ubicado el punto.
    element = element[:position] + element[position+1:] #elimino el punto de la produccion.
    element = element[:position+1] + "•" + element[position+1:] # agrego un punto a la derecha de donde se encontraba originalmente.
    return element # retorno de la produccion con el punto movido a la derecha.

                    
def define_collections(G, Vertex):
    for item in Vertex.items:# para cada uno de los items.
        if item.find("•") != len(item)-1: # si el punto no está en la ultima posicion.
            position = item.find("•") + 1 # obtenemos la posicion del siguiente al punto.
            if item[position] in G.nonterminals: # si el siguiente al punto es un no terminal.
                Vertex.collections.extend(G.productions[item[position]]) # añadimos todo en lo que deriva ese no terminal a los colecciones del vertice actual.
                for j in range(len(Vertex.collections)): # le ponemos un punto al principio a cada una de las colecciones.
                    if Vertex.collections[j] == 'Ɛ':
                        Vertex.collections[j] = "•"
                        Vertex.who_collections.append(item[position])
                    elif Vertex.collections[j].find("•") == -1:
                        Vertex.collections[j] = "•" + Vertex.collections[j]
                        Vertex.who_collections.append(item[position]) 


    for collection in Vertex.collections: # se repite el mismo proceso pero ahora con cada una de las coleecciones, mirando si el siguiente al punto es un no terminal. 
        if collection.find("•") != len(collection)-1:
            position = collection.find("•") + 1
            if collection[position] in G.nonterminals:
                Vertex.collections.extend(G.productions[collection[position]])
                for j in range(len(Vertex.collections)):
                    if Vertex.collections[j] == 'Ɛ':
                        Vertex.collections[j] = "•"
                        Vertex.who_collections.append(collection[position])  
                    elif Vertex.collections[j].find("•") == -1:
                        Vertex.collections[j] = "•" + Vertex.collections[j]
                        Vertex.who_collections.append(collection[position]) 


def automata_bottom_up(G, Vertex, automata, id_current_table):
    define_collections(G, Vertex) # creo lo que va en la parte de abajo de la tabla cuando ya tenemos los items.
    elements = Vertex.items + Vertex.collections # juntamos en una variable aparte los items y las colecciones para hacer las aristas.
    id_next_table = id_current_table+1 # identificador de la proxima tabla.
    who_items_collections = Vertex.who_items + Vertex.who_collections
    for element in elements: # para cada uno de los items y las colecciones de la tabla (la produccion).
        count_differents = 0 # contador que me permite identificar si la tabla (o el vertice) ya existe en el grafo.
        
        if "•" != element[-1]: # si el punto esta distinto a la ultima posición.
            new_items = [] # guardo los items de mi proxima tabla (o vertice).
            new_items.append(next_point(element)) # añado mi actual, con el punto corrido a la derecha.
            who_new_items = []
            who_new_items.append(who_items_collections[0])
            for element2 in elements: # buscamos cada aparicion del mismo no terminal despues del punto para juntarlos en el item (con el punto corrido a la derecha).
                if element2 != element:
                    if "•" != element2[-1]:
                        if element2[element2.find("•")+1] == element[element.find("•")+1]: # si el no terminal siguiente al punto es igual del elemento con el cual vamos a avanzar de vertice.
                            new_items.append(next_point(element2))
            for i in automata.vertices: #verifico si la tabla o vertice ya existe en el grafo o no.
                if automata.vertices[i].items != new_items: 
                    count_differents+=1
                else:
                    break 
            if count_differents == len(automata.vertices):# si esa tabla no existe, creo el vertice y la relacion, con su llamado recursivo con la nueva tabla.
                    automata.add_vertex(id_next_table,new_items,who_new_items) # añado vertice al grafo.
                    automata.add_edge(id_current_table,id_next_table,element[element.find("•")+1]) # añado relacion entre los vertices.
                    who_items_collections.pop(0)
                    id_next_table = automata_bottom_up(G,automata.vertices[id_next_table],automata,id_next_table) # llamado recursivo, que me retorna el numero de tablas que creo, para seguir creando mas a partir de ese numero.
            else: # si la tabla existe, simplemente creo la relacion.
                who_items_collections.pop(0)
                automata.add_edge(id_current_table,automata.vertices[count_differents].id,element[element.find("•")+1]) #le mando el contador2 que contiene al relación con su tabla respectiva.
    
    return id_next_table #cuando finalice de evaluar la tabla, retorno en lo que va el contador para seguir creando tablas restantes en los anteriores llamados recursivos.

def first_table_automata(automata, G):
    automata.add_vertex(0, ["•"+G.start],["δ"])
    automata_bottom_up(G, automata.vertices[0], automata, 0)


def bottom_up_table(G, automata):
    table = []
    numeration_rows = give_positions(list(automata.vertices.keys()),False)
    columns_items = G.terminals + G.nonterminals 
    numeration_columns = give_positions(columns_items,True)

    productions = []
    for value in G.productions.values():
        for production in value:
            productions.append(production)
    print(productions)
    numeration_productions = give_positions(productions, False)
    print(numeration_productions)

    for rows in range(len(automata.vertices)):
        table.append(["∞"] * (len(G.terminals) + len(G.nonterminals) + 1))

    for vertex in automata.vertices:
        for tuple_neighbour in vertex.neighbours:
            if tuple_neighbour[1] in G.nonterminals:
                table[numeration_rows[vertex.id]][numeration_columns[tuple_neighbour[1]]] = vertex.id
            if tuple_neighbour[1] in G.terminals:
                table[numeration_rows[vertex.id]][numeration_columns[tuple_neighbour[1]]] = "S"+vertex.id
        union_items_collections = vertex.items + vertex.collections

    for item in union_items_collections:
        if item.find("•") == len(item)-1:
            if item[:-1] == G.start:
                table[numeration_rows[vertex.id]][numeration_columns["$"]] = "A"
            else:
               production = G.productions[item[:-1]] 
        
