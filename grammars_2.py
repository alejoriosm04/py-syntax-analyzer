from prettytable import PrettyTable
from collections import deque
class grammar():
    def __init__(self, nonterminals, terminals, productions, start):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start = start

class Vertex:
    def __init__(self,i,item):
        self.id = i
        self.items = item
        self.collections = []
        self.neighbours = []
    def add_neigh(self,v):
        if v not in self.neighbours:
            self.neighbours.append(v)

class Graph:
    def __init__(self):
        self.vertexs = {}
    def add_vertex (self,v,items):
        if v not in self.vertexs:
            self.vertexs[v] = Vertex(v,items)
    def add_edge(self,a,b,weight):
        if a in self.vertexs and b in self.vertexs:
            self.vertexs[a].add_neigh((b,weight))

def read_grammar():
    nonterminals = input("Enter the nonterminals: ").split()
    terminals = input("Enter the terminals: ").split()
    productions = {}
    for i in range(len(nonterminals)):
        production = input("Enter a production:")
        productions[production.split('-')[0]] = production.split("->", 1)[1]
        productions[production.split('-')[0]] = productions[production.split('-')[0]].split("|")

    start = input("Enter the start symbol: ")
    
    return nonterminals, terminals, productions, start



def FIRST(G, symbol, P, FIRST_SET):
    position = 0
    lista=[]
    for i in range(len(P)):
        lista.append([])
    value = False # controlador para validar si una producción deriva en epsilon, así evitar eliminarlo del conjunto en caso de que pertenezca.
    for production in P: # para cada produccion en la lista de producciones:
        counter = 0 # permite saber si se recorrió toda la producción actual, para determinar que la misma deriva en epsilon.
        for element in production: #para cada letra de la produccion:
            if element == 'Ɛ':
                lista[position].append('Ɛ')
            if element in G.terminals: #si está en el conjunto de terminales, se agrega el terminal al first y se para de evaluar la produccion actual del no terminal.
                FIRST_SET[symbol].add(element)
                lista[position].append(element)
                break
            if element in G.nonterminals: # si está en el conjunto de no terminales, se ingresa al no terminal y se calcula el first al mismo (recursivamente).
                counter += 1
                if FIRST(G, element, G.productions[element], FIRST_SET)[0]: # si el llamado es true, significa que el no terminal tiene en su first epsilon y por lo tanto, se debe seguir evaluando la cadena.
                    FIRST_SET[symbol] = FIRST_SET[symbol].union(FIRST_SET[element])
                    for i in FIRST_SET[element]:
                        lista[position].append(i)
                else: # si el llamado es false, significa que el no terminal no tiene epsilon en su first, y por lo tanto, no se debe seguir evaluando la cadena.
                    FIRST_SET[symbol] = FIRST_SET[symbol].union(FIRST_SET[element])
                    for i in FIRST_SET[element]:
                        lista[position].append(i)
                    break
                if 'Ɛ' in FIRST_SET[symbol] and value == False: # se elimina el epsilon del first de el no terminal actual, ya que el mismo solo deriva en epsilon cuando en sus producciones tiene epsilon o se recorrio toda la produccion y cada letra deriva en epsilon (se evalua después).
                    FIRST_SET[symbol].remove('Ɛ')
                    lista[position].pop(lista[position].index("Ɛ"))
                if counter == len(production): # si el contador es igual al largo de la produccion, significa que se recorrio toda la cadena.
                    if 'Ɛ' in FIRST_SET[element]: # si en el first de mi ultimo elemento está epsilon, mi cadena puede derivar en epsilon, ya que si recorrimos toda la cadena es porque cada elemento de la misma deriva en epsilon.
                        FIRST_SET[symbol].add('Ɛ')
                        lista[position].append('Ɛ')
                        value = True # se cambia el valor del controlador para no eliminar el epsilon agregado en caso de que existan más producciones con el simbolo no terminal actual.
        position+=1
    if 'Ɛ' in P:
        FIRST_SET[symbol].add('Ɛ')
    if 'Ɛ'in FIRST_SET[symbol]: ## condición del llamado recursivo, con lo que se determina si el anterior llamado recursivo debe continuar evaluando la cadena o no.
        return True,lista
    else:
        return False,lista


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

def give_positions(keys,true_false_terminal):
    dictionary = {} # diccionario donde se guardará como key el terminal o no terminal y como value el numero asignado (para manejar la tabla con posiciones numericas)
    count = 0 # valor asignado a cada terminal o no terminal 
    for i in keys: # se arma el diccionario con la key y el value correspondiente
        dictionary[i] = count
        count+=1
    if true_false_terminal: # si es para asignar posicion a terminales, se añade el simbolo $ que tambien hace parte de la tabla
        dictionary["$"] = count
    return dictionary #se devuelve el diccionario

def print_table(table,positions_terminals,positions_nonterminals): 
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
    print(pretty_table) #imprimó la tabla

def predictive_table(G,first_cadena,follow):
    positions_nonterminals = give_positions(G.nonterminals,False) # definición del numero para cada no terminal.
    positions_terminals = give_positions(G.terminals,True) # definicion de la posicion de cada terminal.
    table=[] # tabla donde se van a almacenar los valores.
    for i in range(len(G.nonterminals)): # creo la tabla en un principio con todos sus valores en infinito (que en esa posicion x,y no tiene un dato relacionado).
        table.append(["∞"]*(len(G.terminals)+1))
    for i in G.nonterminals: # asigno los valores correspondientes en la posicion x,y, para cada uno de los no terminales (filas):
        for j in range(len(G.productions[i])): # para cada una de las producciones de ese no terminal:
            for k in first_cadena[i][j]: # me paro en la lista del first de esa cadena (producción).
                if k != "Ɛ": # si el elemento del first de la cadena es distinto de epsilon:
                    if table[positions_nonterminals[i]][positions_terminals[k]] == "∞":
                        table[positions_nonterminals[i]][positions_terminals[k]] = G.productions[i][j] # en la fila del no terminal, y en la columna del terminal, agrego la producción (cadena correspondiente al first).
                    else:
                        return False
                else:
                    for z in follow[i]: #si es epsilon, para cada uno de los elementos del follow agrego la derivacion del epsilon.
                        if table[positions_nonterminals[i]][positions_terminals[z]] == "∞":
                            table[positions_nonterminals[i]][positions_terminals[z]] = "Ɛ"
                        else:
                            return False
    print_table(table,positions_terminals,positions_nonterminals) # llamo a la función para imprimir la tabla.
    while True: # evaluar cadena.
        string = input()
        if string == "0": # parar de evaluar cadenas.
            break
        else: # continuar evaluando cadenas.
            print(read_string(string,G,table,positions_terminals,positions_nonterminals))
    

def read_string(string, G, table, positions_terminals, positions_nonterminals):
    queue = deque() # creamos la pila que inicialmente tendrá el simbolo pesos y el inicial, este ultimo en el top de la pila 
    queue.appendleft("$")
    queue.appendleft(G.start)

    for i in string: # si se ingresa un simbolo que no hace parte del lenguaje, retorna error.
        if i not in G.terminals:
            return "Error syntax"
    string = string+"$" # añadimos el simbolo pesos al final de la cadena ingresada para saber que se recorrio la misma completamente.
    X = queue[0] # top de mi pila.
    a = string[0] # caracter a evaluar.
    while(X != "$"): # mientras que el top de la pila sea distinto de pesos (es decir, que existan producciones por aplicar).
        if X in G.terminals: # si el top de mi pila es un terminal.
            if X == a: # si el top de mi pila es igual al caracter que estoy evaluando (una coincidencia).
                queue.popleft() # elimino el caracter de la pila.
                string = string[1:] # actualizo el string, ya que se debe evaluar el siguiente caracter.
                a = string[0] # actualizo el caracter a evaluar (siguiente al anterior).
            else:
                return "Error syntax"
        else:
            if table[positions_nonterminals[X]][positions_terminals[a]] == "∞": # si se trata acceder a una posicion de la tabla de "Error".
                return "Error syntax"
            else:
                value = queue.popleft() # elimino el no terminal de la pila (el que esta en el top).
                if table[positions_nonterminals[value]][positions_terminals[a]] != "Ɛ": # si la matriz en esa coordenadas es una produccion distinta a epsilon.
                    string_reversed = table[positions_nonterminals[value]][positions_terminals[a]][::-1] # invierto la cadena para hacer appendleft en la pila.
                    for caracter in string_reversed: # agregamos a la pila.
                        queue.appendleft(caracter)
        X=queue[0] # actualizamos el valor del top de la pila al actual.
    return "String accepted"


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
                    if Vertex.collections[j].find("•") == -1:
                        Vertex.collections[j] = "•" + Vertex.collections[j]


    for collection in Vertex.collections: # se repite el mismo proceso pero ahora con cada una de las coleecciones, mirando si el siguiente al punto es un no terminal. 
        if collection.find("•") != len(collection)-1:
            position = collection.find("•") + 1
            if collection[position] in G.nonterminals:
                Vertex.collections.extend(G.productions[collection[position]])
                for j in range(len(Vertex.collections)):
                    if Vertex.collections[j].find("•") == -1:
                        Vertex.collections[j] = "•" + Vertex.collections[j]


def automata_bottom_up(G, Vertex, automata, id_current_table):
    define_collections(G, Vertex) # creo lo que va en la parte de abajo de la tabla cuando ya tenemos los items.
    elements = Vertex.items + Vertex.collections # juntamos en una variable aparte los items y las colecciones para hacer las aristas.
    id_next_table = id_current_table+1 # identificador de la proxima tabla.
    for element in elements: # para cada uno de los items y las colecciones de la tabla (la produccion).
        count_differents = 0 # contador que me permite identificar si la tabla (o el vertice) ya existe en el grafo.
        if element.find("•") != len(element)-1: # si el punto esta distinto a la ultima posición.
            new_items = [] # guardo los items de mi proxima tabla (o vertice).
            new_items.append(next_point(element)) # añado mi actual, con el punto corrido a la derecha.
            for element2 in elements: # buscamos cada aparicion del mismo no terminal despues del punto para juntarlos en el item (con el punto corrido a la derecha).
                if element2 != element:
                    if element2.find("•") != len(element)-1:
                        if element2[element2.find("•")+1] == element[element.find("•")+1]: # si el no terminal siguiente al punto es igual del elemento con el cual vamos a avanzar de vertice.
                            new_items.append(next_point(element2))
            for i in automata.vertexs: #verifico si la tabla o vertice ya existe en el grafo o no.
                if automata.vertexs[i].items != new_items: 
                    count_differents+=1
                else:
                    break 
            if count_differents == len(automata.vertexs):# si esa tabla no existe, creo el vertice y la relacion, con su llamado recursivo con la nueva tabla.
                    automata.add_vertex(id_next_table,new_items) # añado vertice al grafo.
                    automata.add_edge(id_current_table,id_next_table,element[element.find("•")+1]) # añado relacion entre los vertices.
                    id_next_table = automata_bottom_up(G,automata.vertexs[id_next_table],automata,id_next_table) # llamado recursivo, que me retorna el numero de tablas que creo, para seguir creando mas a partir de ese numero.
            else: # si la tabla existe, simplemente creo la relacion.
                automata.add_edge(id_current_table,automata.vertexs[count_differents].id,element[element.find("•")+1]) #le mando el contador2 que contiene al relación con su tabla respectiva.
    return id_next_table #cuando finalice de evaluar la tabla, retorno en lo que va el contador para seguir creando tablas restantes en los anteriores llamados recursivos.

def first_table_automata(automata,G):
    automata.add_vertex(0,["•"+G.start])
    automata_bottom_up(G,automata.vertexs[0],automata,0)

def main():
    nonterminals, terminals, productions, start = read_grammar()
    print(productions)
    G = grammar(nonterminals, terminals, productions, start)
    FIRST_SET = {}
    FIRST_SET_STRINGS = {}
    for i in nonterminals:
        FIRST_SET[i] = set()
        FIRST_SET_STRINGS[i] = None
    for i in FIRST_SET.keys():
        valor = FIRST(G, i, productions[i], FIRST_SET)[1]
        FIRST_SET_STRINGS[i] = valor
    FOLLOW_SET = {}
    for i in nonterminals:
        FOLLOW_SET[i] = set()
        FOLLOW_SET[start].add('$')
    for i in FOLLOW_SET.keys():
        FOLLOW(FIRST_SET, G, i, FOLLOW_SET)
    print(FOLLOW_SET)
    if predictive_table(G,FIRST_SET_STRINGS,FOLLOW_SET) == False:
        print("No es ll(1), se intentó ingresar dos valores en un posición de la matriz")
    automata = Graph()
    first_table_automata(automata,G)
    for i in automata.vertexs:
        print(i,automata.vertexs[i].items,automata.vertexs[i].collections, automata.vertexs[i].neighbours)

if __name__ == "__main__":
    main()
