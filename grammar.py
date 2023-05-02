from prettytable import PrettyTable


class grammar():
    def __init__(self, nonterminals, terminals, productions, start):
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.productions = productions
        self.start = start

    
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
    value = False # controlador para validar si una producción deriva en epsilon, así evitar eliminarlo del conjunto en caso de que pertenezca.
    for production in P: # para cada produccion en la lista de producciones:
        counter = 0 # permite saber si se recorrió toda la producción actual, para determinar que la misma deriva en epsilon.
        for element in production: #para cada letra de la produccion:
            if element in G.terminals: #si está en el conjunto de terminales, se agrega el terminal al first y se para de evaluar la produccion actual del no terminal.
                FIRST_SET[symbol].add(element)
                break
            if element in G.nonterminals: # si está en el conjunto de no terminales, se ingresa al no terminal y se calcula el first al mismo (recursivamente).
                counter += 1
                if FIRST(G, element, G.productions[element], FIRST_SET): # si el llamado es true, significa que el no terminal tiene en su first epsilon y por lo tanto, se debe seguir evaluando la cadena.
                    FIRST_SET[symbol] = FIRST_SET[symbol].union(FIRST_SET[element])
                else: # si el llamado es false, significa que el no terminal no tiene epsilon en su first, y por lo tanto, no se debe seguir evaluando la cadena.
                    FIRST_SET[symbol] = FIRST_SET[symbol].union(FIRST_SET[element])
                    break
                if 'Ɛ' in FIRST_SET[symbol] and value == False: # se elimina el epsilon del first de el no terminal actual, ya que el mismo solo deriva en epsilon cuando en sus producciones tiene epsilon o se recorrio toda la produccion y cada letra deriva en epsilon (se evalua después).
                    FIRST_SET[symbol].remove('Ɛ')
                if counter == len(production): # si el contador es igual al largo de la produccion, significa que se recorrio toda la cadena.
                    if 'Ɛ' in FIRST_SET[element]: # si en el first de mi ultimo elemento está epsilon, mi cadena puede derivar en epsilon, ya que si recorrimos toda la cadena es porque cada elemento de la misma deriva en epsilon.
                        FIRST_SET[symbol].add('Ɛ')
                        value = True # se cambia el valor del controlador para no eliminar el epsilon agregado en caso de que existan más producciones con el simbolo no terminal actual.
    if 'Ɛ' in P:
        FIRST_SET[symbol].add('Ɛ')
    if 'Ɛ'in FIRST_SET[symbol]: ## condición del llamado recursivo, con lo que se determina si el anterior llamado recursivo debe continuar evaluando la cadena o no.
        return True
    else:
        return False


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


def predictive_table(G, FIRST_SET, FOLLOW_SET):
    table = {}
    for no_terminal in G.productions:
        table[no_terminal] = {}
        for production in G.productions[no_terminal]:
            if production == 'Ɛ':
                for terminal in FOLLOW_SET[no_terminal]:
                    table[no_terminal][terminal] = production
            else:
                if production[0] in G.terminals:
                    table[no_terminal][production[0]] = production
                if production[0] in G.nonterminals:
                    for terminal in FIRST_SET[production[0]]:
                        table[no_terminal][terminal] = production

    columns = G.terminals
    columns.append('$') 
    
    for no_terminal in G.productions:
        for terminal in columns:
            if terminal not in table[no_terminal]:
                table[no_terminal][terminal] = '∞'

    print("Predictive table:")

    pretty_table = PrettyTable()
    pretty_table.field_names = [""] + list(table[list(table.keys())[0]].keys())

    for row_key, row_value in table.items():
        row = [row_key]
        for col_key in list(table[list(table.keys())[0]].keys()):
            if row_value[col_key] == '∞':
                row.append(row_value[col_key])
            else:
                row.append(row_key + "->" + row_value[col_key])
        pretty_table.add_row(row)

    print(pretty_table)


def main():
    nonterminals, terminals, productions, start = read_grammar()
    print(productions)
    G = grammar(nonterminals, terminals, productions, start)
    FIRST_SET = {}
    for i in nonterminals:
        FIRST_SET[i] = set()
    for i in FIRST_SET.keys():
        FIRST(G, i, productions[i], FIRST_SET)
    print(FIRST_SET)

    FOLLOW_SET = {}
    for i in nonterminals:
        FOLLOW_SET[i] = set()
        FOLLOW_SET[start].add('$')
    for i in FOLLOW_SET.keys():
        FOLLOW(FIRST_SET, G, i, FOLLOW_SET)
    print(FOLLOW_SET)

    predictive_table(G, FIRST_SET, FOLLOW_SET)


if __name__ == "__main__":
    main()
