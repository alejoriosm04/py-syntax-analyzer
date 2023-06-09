from collections import deque


def read_string_top_down(string, G, table, positions_terminals, positions_nonterminals):
    queue = deque() # creamos la pila que inicialmente tendrá el simbolo pesos y el inicial, este ultimo en el top de la pila 
    queue.appendleft("$")
    queue.appendleft(G.start)

    for i in string: # si se ingresa un simbolo que no hace parte del lenguaje, retorna error.
        if i not in G.terminals:
            return errors(1)
        
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
                return errors(2) # si el top de la pila es un terminal y no coincide con el caracter a evaluar, retorna error.
        else:
            if table[positions_nonterminals[X]][positions_terminals[a]] == "∞": # si se trata acceder a una posicion de la tabla de "Error".
                return errors(2)
            else:
                value = queue.popleft() # elimino el no terminal de la pila (el que esta en el top).
                if table[positions_nonterminals[value]][positions_terminals[a]] != "Ɛ": # si la matriz en esa coordenadas es una produccion distinta a epsilon.
                    string_reversed = table[positions_nonterminals[value]][positions_terminals[a]][::-1] # invierto la cadena para hacer appendleft en la pila.
                    for caracter in string_reversed: # agregamos a la pila.
                        queue.appendleft(caracter)
        X = queue[0] # actualizamos el valor del top de la pila al actual.

    if string[0] != "$":
        return errors(2)
    
    return "String accepted"


def string_input_top_down(G, table, positions_terminals,positions_nonterminals):
    while True: # evaluar cadena.
        string = input("Enter a string (Enter 0 to finish):")
        if string == "0": # parar de evaluar cadenas.
            break
        else: # continuar evaluando cadenas.
            print(read_string_top_down(string, G, table, positions_terminals,positions_nonterminals))


def read_string_bottom_up(string, table, positions_rows, positions_columns, number_each_production,G):
    for i in string: # si se ingresa un simbolo que no hace parte del lenguaje, retorna error.
        if i not in G.terminals:
            return errors(1)
    string = string + "$" # a la cadena ingresada se le agrega $ que significa el final de la cadena
    current_char = string[0] # caracter que se está evaluando actualmente, primer simbolo
    queue = deque() # pila donde se actualizará la evaluación de la cadena
    queue.append(0) # se agrega el 0 a la pila (el estado inicial)
    dict_numbers = {} # diccionario donde se va almacenar como key la producción respectiva (enumeracion) y como value el no terminal de quien deriva esa producción y la longitud de la produccion (nos ayuda para saber la cantidad de veces que hacemos pop)
    for key in number_each_production: 
        for element in number_each_production[key]:
            if element[0]  == "Ɛ":
                dict_numbers[element[1]] = (key,0) # si es epsilon, la "longitud" de lo que debo popear es 0 (es lo que representa el simbolo en si mismo)
            else:
                dict_numbers[element[1]] = (key,len(element[0]))

    while True: # se ejecuta siempre hasta que lleguemos a un estado de aceptacion ó se intente acceder a una posición de error
        top_queue = queue[0] # actualizo el top de mi pila
        if table[positions_rows[top_queue]][positions_columns[current_char]][0] == "S": # si la tabla en la fila del top de mi pila y en la columna del caracter actual es un shift
            queue.appendleft(int(table[positions_rows[top_queue]][positions_columns[current_char]][1:])) # añado a la pila el numero del shift
            string = string[1:] # actualizo el string
            current_char = string[0] #establezco el nuevo caracter actual
        elif table[positions_rows[top_queue]][positions_columns[current_char]][0] == "r": # si la tabla en la fila del top de mi pila y en la columna del caracter actual es un reduce
            tuple_production = dict_numbers[int(table[positions_rows[top_queue]][positions_columns[current_char]][1:])] # accedemos a la tupla que contiene la produccion y la longitud, con el numero del reduce que estamos realizando
            for i in range(tuple_production[1]): #popea tantas veces como la longitud de dicha producción
                queue.popleft() 
            top_temp = queue[0] # una vez popeados los elementos nos queda un top temporal, el cual miramos en la tabla, en la fila de ese top temporal, y en la columna del no terminal el cual contenia la produccion, y añadimos a la pila el numero con el cual realizamos el GOTO
            value_to_append = table[positions_rows[top_temp]][positions_columns[tuple_production[0]]]
            queue.appendleft(int(value_to_append))
        elif table[positions_rows[top_queue]][positions_columns[current_char]][0] == "A": # si estamos en el estado de aceptación, el string fue procesado correctamente
            return "String Accepted"
        else:
            return errors(2)


def string_input_bottom_up(table, positions_rows, positions_columns, number_each_production,G):
    while True: # evaluar cadena.
        string = input("Enter a string (Enter 0 to finish):")
        if string == "0": # parar de evaluar cadenas.
            break
        else: # continuar evaluando cadenas.
            print(read_string_bottom_up(string, table, positions_rows, positions_columns, number_each_production,G))


def errors(id):
    if id == 1:
        return "Error syntax. Unknown symbol, not part of the language"
    if id == 2:
        return "Error syntax. Wrong string production"
