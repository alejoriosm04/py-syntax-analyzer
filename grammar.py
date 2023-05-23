from prettytable import PrettyTable
from collections import deque
from string_parser import *
import random

class grammar():
    def __init__(self, nonterminals, terminals, productions, start):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start = start

    def give_positions_new_grammar(self): # establece a cada no terminal su A_i respectivo
        count_Asub = 0  # contador que permite saber el A_i en el que vamos
        dictionary_Asub = {} # diccionario que tendrá como key el no terminal, y como valor su A_i respectivo
        for i in self.nonterminals: # recorremos cada no terminal, y para cada uno de ellos le asignamos el A_i
            dictionary_Asub[i] = "ª" + str(count_Asub)
            count_Asub+=1
        return dictionary_Asub, count_Asub # se retorna el diccionario con las correspondencias y el contador para en el futuro crear los siguientes A_i

    def find_new_letter(self, alphabet_new_nonterminals, dictionary_Asub): # Encuentra una letra que no haya sido utilizada aún en los no terminales de la gramatica. 
        while(True): # Hasta que encuentre una letra que usar
            num = random.randint(0,len(alphabet_new_nonterminals)-1) # genera un numero, el cual permite ubicarnos en la lista en la posicion de una letra
            if alphabet_new_nonterminals[num] not in dictionary_Asub:# se verifica si la letra no se ha usado
                return alphabet_new_nonterminals[num] # retorna la letra

    def eliminate_left_recursion_immediately(self, new_grammar_replace, dictionary_Asub, A_i, alphabet_new_nonterminals, count_Asub): # elimina la recursión inmediata de la derivación o A_i actual
        not_recursion = [] # lista donde se guarda los elementos que no generan recursion izquierda
        recursion = [] # lista donde se guarda los elementos que generan recursion izquierda
        
        for r in new_grammar_replace["ª"+str(A_i)]: #recorremos cada una de las producciones de el A_i actual
            if len(r)>=2:
                if r[0] + r[1] == "ª"+str(A_i): # se verifica si en dicha producción, existe una recursión izquierda
                    recursion.append(r) # si existe la recursión izquierda, la añadimos a la lista de quienes generan recursion
                else:
                    not_recursion.append(r) # si no existe la recursion izquierda, la añadimos a la lista de quienes no generan recursion
            else:
                not_recursion.append(r) # si la produccion tiene un largo menor a 2, significa que no es de la forma A_i y por lo tanto no genera recursion
        
        if len(recursion)==0: # si no hay ninguna producción que genere recursion, se termina de evaluar, y se devuelve el contador con el mismo valor con el que venia
            return count_Asub
        else: # si existe alguna producción que genere recursión
            new_letter = self.find_new_letter(alphabet_new_nonterminals, dictionary_Asub) # encontramos la letra para esa nueva derivación que existirá en la gramatica
            self.nonterminals.append(new_letter) # la añadimos a los no terminales
            dictionary_Asub[new_letter] = "ª"+str(count_Asub) # le asignamos a dicho no terminal su A_i respectivo
            new_grammar_replace[dictionary_Asub[new_letter]] = [] # añadimos a la gramatica este nuevo no terminal, y posteriormente le llenamos el valor de sus producciones
            new_grammar_replace["ª"+str(A_i)] = [] # formateamos la derivación actual para establecerle los valores almacenados en lo que genera recursion y no
            
            for production in not_recursion: # para cada uno de las producciones que no generan recursión izquierda 
                if production != "Ɛ": 
                    production = production + dictionary_Asub[new_letter] # le añado la producción, y al final El A_i'
                    new_grammar_replace["ª"+str(A_i)].append(production) # se añade a las derivaciones de A_i actual
                else:
                    new_grammar_replace["ª"+str(A_i)].append(dictionary_Asub[new_letter]) # Si tiene epsilon, basta con añadir el A_i', ya que epsilon representa nada
            
            for production in recursion: # para cada una de las producciones que generan recursion izquierda
                production = production[2:] + dictionary_Asub[new_letter] # popeo lo que le genera recursion izquierda a la produccion y dejo lo demás, agregandole al final el nuevo no terminal de quien estoy derivando
                new_grammar_replace[dictionary_Asub[new_letter]].append(production) #Se añade a las derivaciones de A_i actual
            
            new_grammar_replace[dictionary_Asub[new_letter]].append('Ɛ') # a esta nueva derivación que se genero siempre se añade epsilon
            count_Asub+=1 # Como se creo un nuevo A_i, se le suma uno al contador para en el futuro crear nuevos A_i.
            return count_Asub # retorna el contador actual del A_i, para crear nuevos A_i y no repetirlos.

    def remove_left_recursion(self):
        alphabet_new_nonterminals = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","Ñ","O","P","Q","R","S","T","U","V","W","X","Y","Z"] # abecedario para nuevos no terminales que aparezcan
        dictionary_Asub, count_Asub = self.give_positions_new_grammar() # asigno a cada no terminal el Asub(contador) que le pertenece y retorno el contador, para nuevos terminales que aparezcan al eliminar recursion 
        dictionary_Asub_reversed = {} # se establece a que no terminal pertenece cada Asubtanto (reverse entre keys y values)
        new_grammar_replace = {} # nueva gramatica reemplazada con los Asubtantos
        
        for nonterminal_key in self.productions: # establezco las keys en el diccionario reemplazado
            new_grammar_replace[dictionary_Asub[nonterminal_key]] = [] 
        for nonterminal_key in self.productions: # asigno la producción a cada key, reemplazado sus no terminales con el Asubtanto correspondiente
            for production in self.productions[nonterminal_key]: # recorro cada una de las producciones correspondientes al no terminal
                for caracter in production: # por cada caracter de la produccion, si es un no terminal lo reemplaza por el Asubtanto correspondiente.
                    if caracter in dictionary_Asub:
                        production = production.replace(caracter,dictionary_Asub[caracter])
                new_grammar_replace[dictionary_Asub[nonterminal_key]].append(production) # añadimos la produccion al no terminal correspondiente
        for A_i in range(len(self.nonterminals)): #para cada i de la gramatica
            for A_j in range(A_i): # para cada i-1 de la gramatica
                control = 0 # variable de control para recorrer cada una de las producciones del no terminal actual
                while(control<len(new_grammar_replace["ª"+str(A_i)])): # mientras aun no hayamos recorrido todas las producciones del no terminal actual
                    if len(new_grammar_replace["ª"+str(A_i)][control])>2: # si el largo de la produccion actual es mayor a 2 (es decir, que puede ser de la forma "ªi")
                        if new_grammar_replace["ª"+str(A_i)][control][0]+new_grammar_replace["ª"+str(A_i)][control][1] == "ª"+str(A_j): # verifico si hay algo de la forma A_i->Aj_
                            to_add = new_grammar_replace["ª"+str(A_i)][control][2:] # almaceno el beta que se debe agregar a las nuevas producciones
                            new_grammar_replace["ª"+str(A_i)].pop(new_grammar_replace["ª"+str(A_i)].index(new_grammar_replace["ª"+str(A_i)][control])) # elimino la producción actual que es de la forma A_i->Aj_
                            new_production = [] # lista donde se almacenará el nuevo value de nuestro no terminal actual 
                            for production in new_grammar_replace["ª"+str(A_j)]: # a cada produccion de A_j le añado el to_add
                                new_production.append(production+to_add) 
                            new_grammar_replace["ª"+str(A_i)].extend(new_production) # añadimos a la lista de producciones de ese no terminal
                    control+=1 # aumento variable de control
            count_Asub = self.eliminate_left_recursion_immediately(new_grammar_replace,dictionary_Asub,A_i,alphabet_new_nonterminals,count_Asub) # eliminamos derivación izquierda, y almacenamos el Asub en el que se va
        for A_i in dictionary_Asub:
            dictionary_Asub_reversed[dictionary_Asub[A_i]] = A_i
        final_grammar = {} # gramatica con eliminación por izquierda
        for A_i in new_grammar_replace: # vuelvo a transformar la nueva gramatica que tenemos de A_i para ponerlo en los no terminales correspondientes
            final_grammar[dictionary_Asub_reversed[A_i]] = []
        for key in new_grammar_replace: # para cada key del diccionario de la gramatica de la forma A_i
            for production in new_grammar_replace[key]: # para cada produccion de ese A_i 
                control=0 # variable de control para recorrer cada caracter de la produccion
                while(control<len(production)): # recorremos la produccion
                    if production[control] == "ª" and production[control]+production[control+1] in dictionary_Asub_reversed: # si encuentra un A_i, lo modifica por su respectivo no terminal
                        production = production.replace(production[control]+production[control+1],dictionary_Asub_reversed[production[control]+production[control+1]]) 
                    control+=1
                final_grammar[dictionary_Asub_reversed[key]].append(production) # finalmente, añade la producción a su no terminal del quien deriva (con la transformación hecha).
        self.productions = final_grammar # asigna a la gramatica, su nueva gramatica con la eliminación de la derivación por izquierda.


class Vertex:
    def __init__(self, id, items, who_items):
        self.id = id
        self.items = items
        self.collections = []
        self.neighbours = []
        self.who_collections = []
        self.who_items = who_items
        self.relations = {}
        self.temp_items = {}
        self.temp_collections = {}
    def add_neigh(self, v):
        if v not in self.neighbours:
            self.neighbours.append(v)
    
    def who_derivate_general(self,who_items, items,who_collections,collections):
        who_items_2 = who_items.copy()
        who_collections_2 = who_collections.copy()
        for i in items:
            self.relations[i] = who_items_2[0]
            temp_val = who_items_2.pop(0)
            self.temp_items[i] = temp_val
        for i in collections:
            self.relations[i] = who_collections_2[0]
            temp_val = who_collections_2.pop(0)
            self.temp_collections[i] = temp_val


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
    
    print("\n" + "-----------------------------")
    print("Predictive Parsing Table:")
    print("-----------------------------" + "\n")
    print(pretty_table) #imprimó la tabla
    print("\n" + "-------------------------------")


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
    visited = [] # almacena las producciones por las cuales ya se pasó para no añadir el mismo elemtento
    for item in Vertex.items:# para cada uno de los items.
        if item.find("•") != len(item)-1: # si el punto no está en la ultima posicion.
            position = item.find("•") + 1 # obtenemos la posicion del siguiente al punto.
            if item[position] in G.nonterminals and item[position] not in visited: # si el siguiente al punto es un no terminal.
                Vertex.collections.extend(G.productions[item[position]])# añadimos todo en lo que deriva ese no terminal a los colecciones del vertice actual.
                visited.append(item[position])
                for j in range(len(Vertex.collections)): # le ponemos un punto al principio a cada una de las colecciones.
                    if Vertex.collections[j] == 'Ɛ': # si es epsilon,guarde un punto y no .epsilon
                        Vertex.collections[j] = "•"
                        Vertex.who_collections.append(item[position]) # guardo de quien deriva dicha producción (cual no terminal)
                    elif Vertex.collections[j].find("•") == -1: #le agrega el punto al principio a todos los elementos de la coleccion (clausura)
                        Vertex.collections[j] = "•" + Vertex.collections[j]
                        Vertex.who_collections.append(item[position]) 


    for collection in Vertex.collections: # se repite el mismo proceso pero ahora con cada una de las coleecciones, mirando si el siguiente al punto es un no terminal. 
        if collection.find("•") != len(collection)-1:
            position = collection.find("•") + 1
            if collection[position] in G.nonterminals and collection[position] not in visited:
                Vertex.collections.extend(G.productions[collection[position]])
                visited.append(collection[position])
                for j in range(len(Vertex.collections)):
                    if Vertex.collections[j] == 'Ɛ':
                        Vertex.collections[j] = "•"
                        Vertex.who_collections.append(collection[position])  
                    elif Vertex.collections[j].find("•") == -1:
                        Vertex.collections[j] = "•" + Vertex.collections[j]
                        Vertex.who_collections.append(collection[position])
    Vertex.who_derivate_general(Vertex.who_items, Vertex.items, Vertex.who_collections, Vertex.collections)


def automata_bottom_up(G, Vertex, automata, id_current_table):
    define_collections(G, Vertex) # creo lo que va en la parte de abajo de la tabla cuando ya tenemos los items. (clausure)
    elements = Vertex.items + Vertex.collections # juntamos en una variable aparte los items y las colecciones para hacer las aristas.
    who_two = Vertex.who_items + Vertex.who_collections
    id_next_table = id_current_table+1 # identificador de la proxima tabla.
    count_2 = 0
    for element in elements: # para cada uno de los items y las colecciones de la tabla (la produccion).
        count_differents = 0 # contador que me permite identificar si la tabla (o el vertice) ya existe en el grafo.
        if "•" != element[-1]: # si el punto esta distinto a la ultima posición.
            new_items = [] # guardo los items de mi proxima tabla (o vertice).
            value_next_point_string = next_point(element)
            new_items.append(value_next_point_string) # añado mi actual, con el punto corrido a la derecha.
            who_new_items = []
            temp_who_items = {}
            temp_who_items[value_next_point_string] = who_two[count_2]
            who_new_items.append(who_two[count_2])
            count_3=0
            for element2 in elements: # buscamos cada aparicion del mismo no terminal despues del punto para juntarlos en el item (con el punto corrido a la derecha).
                if element2 != element:
                    if "•" != element2[-1]:
                        if element2[element2.find("•")+1] == element[element.find("•")+1]: # si el no terminal siguiente al punto es igual del elemento con el cual vamos a avanzar de vertice.
                            value_next_point = next_point(element2)
                            new_items.append(value_next_point)
                            who_new_items.append(who_two[count_3])
                            temp_who_items[value_next_point] = who_two[count_3]
                count_3+=1
            for i in automata.vertices: #verifico si la tabla o vertice ya existe en el grafo o no.
                if sorted(automata.vertices[i].items) != sorted(new_items): 
                    count_differents+=1
                else:
                    if sorted(automata.vertices[i].temp_items.values())!= sorted(temp_who_items.values()):
                        count_differents+=1
                    else:
                        break 
            if count_differents == len(automata.vertices):# si esa tabla no existe, creo el vertice y la relacion, con su llamado recursivo con la nueva tabla.
                    automata.add_vertex(id_next_table,new_items,who_new_items) # añado vertice al grafo.
                    automata.add_edge(id_current_table,id_next_table,element[element.find("•")+1]) # añado relacion entre los vertices.
                    id_next_table = automata_bottom_up(G,automata.vertices[id_next_table],automata,id_next_table) # llamado recursivo, que me retorna el numero de tablas que creo, para seguir creando mas a partir de ese numero.
            else: # si la tabla existe, simplemente creo la relacion.
                automata.add_edge(id_current_table,automata.vertices[count_differents].id,element[element.find("•")+1]) #le mando el contador2 que contiene al relación con su tabla respectiva.
        count_2+=1
    return id_next_table #cuando finalice de evaluar la tabla, retorno en lo que va el contador para seguir creando tablas restantes en los anteriores llamados recursivos.


def first_table_automata(automata, G):
    automata.add_vertex(0, sorted(["•"+G.start]), ["δ"]) # nuestra primera tabla del automata siempre con id 0, un punto con el no terminal inicial por delante, y un simbolo random de quien deriva esta "nueva produccion".
    automata_bottom_up(G, automata.vertices[0], automata, 0) # llamamos a la funcion que crea el automata


def bottom_up_table(G, automata,follow):
    table = [] # creamos donde se almacenará la tabla
    numeration_rows = give_positions(list(automata.vertices.keys()), False) # a cada estado lo indexamos para poder utilizar coordenadas en la tabla, representan las filas
    columns_items = G.terminals + G.nonterminals  # las columnas son la suma de los no terminales y los terminales
    numeration_columns = give_positions(columns_items, True) # a cada terminal y no terminal le asignamos un numero (indexamos), para poder trabajar con coordenadas en la matriz

    for rows in range(len(automata.vertices)): # se crea la tabla con todos los valores en infinito (aun no se establecen valores)
        table.append(["∞"] * (len(G.terminals) + len(G.nonterminals) + 1))

    number_each_production = {} # diccionario que almacenará el no terminal como key y sus producciones con su respectiva enumeración para los reduce
    for i in G.productions:
        number_each_production[i] = []
    counter = 0
    for i in G.productions: # se almacena como value una tupla, que es la produccion, y la enumeración de la misma.
        for j in G.productions[i]:
            number_each_production[i].append((j, counter))
            counter+=1
    for vertex in automata.vertices: # para cada uno de los estados
        for tuple_neighbour in automata.vertices[vertex].neighbours: # accedemos a cada una de sus relaciones
            if tuple_neighbour[1] in G.nonterminals: # si va a otra tabla con un no terminal, tabla[id_tabla_actual][no_terminal_evaluado] = id de la tabla a la que se desplaza (GO TO)
                if table[numeration_rows[automata.vertices[vertex].id]][numeration_columns[tuple_neighbour[1]]] =="∞": # si se intenta establecer dos valores en una misma casilla retorna el error respectivo
                    table[numeration_rows[automata.vertices[vertex].id]][numeration_columns[tuple_neighbour[1]]] = tuple_neighbour[0] # 
                else:
                    return False
            if tuple_neighbour[1] in G.terminals: # si va a otra tabla con un terminal, tabla en la fila del estado y en la columna de ese terminal, hacemos Shift x, siendo x el id de la tabla a la que nos desplazamos
                if table[numeration_rows[automata.vertices[vertex].id]][numeration_columns[tuple_neighbour[1]]] == "∞":
                    table[numeration_rows[automata.vertices[vertex].id]][numeration_columns[tuple_neighbour[1]]] = "S"+str(tuple_neighbour[0])
                else:
                    return False
        union_items_collections = automata.vertices[vertex].items + automata.vertices[vertex].collections # una vez halladas todas las relaciones nos preguntamos si existe alguna produccion con un punto al final de la cadena, por lo tanto, evaluamos cada uno de los items y las colecciones del estado actual
        who_twoo = automata.vertices[vertex].who_items + automata.vertices[vertex].who_collections
        count2 = 0
        for item_or_collection in union_items_collections: # para cada uno de los items y las colecciones
            if "•" == item_or_collection[-1]: # si el punto está al final del item o la coleccion
                if who_twoo[count2] == "δ": # si dicho elemento deriva del simbolo inicial, es un estado de aceptación
                    if table[numeration_rows[automata.vertices[vertex].id]][numeration_columns["$"]] == "∞": 
                        table[numeration_rows[automata.vertices[vertex].id]][numeration_columns["$"]] = "A"
                    else:
                        return False
                else:
                    list_production = number_each_production[who_twoo[count2]] # lista que contiene cada una de las producciones del no terminal de quien deriva mi item o coleccion actual (colleccion = elementos de la clausura)
                    number = 0 # variable que almacena el numero con el que se realizará la reducción
                    for i in list_production: # recorremos la lista mencionada anteriormente hasta encontrar la producción actual y guardar su enumeración.
                        if item_or_collection == "•" and i[0] == "Ɛ": # si mi item o coleccion es un punto unicamente y mi produccion es epsilon, esa es la producción con la cual se realiza el reduce de mi item o coleccion actual
                            number = i[1]
                            break
                        if i[0] == item_or_collection[0:-1]: # si no es epsilon, buscamos la producción que sea igual a mi item sin el punto, para guardar su enumeración para realizar el reduce
                            number = i[1]
                            break
                    for i in follow[who_twoo[count2]]: # para cada uno de los elementos del follow del no terminal de quien deriva mi item o coleccion actual que tiene un punto al final
                        if table[numeration_rows[automata.vertices[vertex].id]][numeration_columns[i]] == "∞":
                            table[numeration_rows[automata.vertices[vertex].id]][numeration_columns[i]] = "r"+str(number) #se agrega el reduce con la enumeración respectiva
                        else:
                            return False
            count2+=1
                        
    print_table(table,numeration_columns,numeration_rows) # se imprime la tabla
    print("Productions were listed as follows: ") 
    print(number_each_production) # se imprime la enumeración que se le dio a cada producción
    print("-----------------------------")
    string_input_bottom_up(table, numeration_rows, numeration_columns, number_each_production, G) # se procesan las cadenas con el analizador
