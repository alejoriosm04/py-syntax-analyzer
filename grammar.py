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

if __name__ == "__main__":
    main()
