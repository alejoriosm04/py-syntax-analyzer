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
    
    return "String accepted"


def string_input_top_down(G, table, positions_terminals,positions_nonterminals):
    while True: # evaluar cadena.
        string = input("Enter a string (Enter 0 to finish):")
        if string == "0": # parar de evaluar cadenas.
            break
        else: # continuar evaluando cadenas.
            print(read_string_top_down(string, G, table, positions_terminals,positions_nonterminals))


def errors(id):
    if id == 1:
        return "Error syntax. Unknown symbol, not part of the language"
    if id == 2:
        return "Error syntax. Wrong string production"
