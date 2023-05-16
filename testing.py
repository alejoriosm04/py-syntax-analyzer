from grammar import *


def test_user_grammar():
    nonterminals = input("Enter the nonterminals: ").split()
    terminals = input("Enter the terminals: ").split()
    productions = {}
    for i in range(len(nonterminals)):
        production = input("Enter a production:")
        productions[production.split('-')[0]] = production.split("->", 1)[1]
        productions[production.split('-')[0]] = productions[production.split('-')[0]].split("|")

    start = input("Enter the start symbol: ")
    
    G = grammar(nonterminals, terminals, productions, start)

    print("-----------------------------")
    print("Top-Down Parsing")
    print("-----------------------------")

    FIRST_SET = {}
    FIRST_SET_STRINGS = {}
    for i in nonterminals:
        FIRST_SET[i] = set()
        FIRST_SET_STRINGS[i] = None
    for i in FIRST_SET.keys():
        value = FIRST(G, i, productions[i], FIRST_SET)[1]
        FIRST_SET_STRINGS[i] = value

    FOLLOW_SET = {}
    for i in nonterminals:
        FOLLOW_SET[i] = set()
        FOLLOW_SET[start].add('$')
    for i in FOLLOW_SET.keys():
        FOLLOW(FIRST_SET, G, i, FOLLOW_SET)

    if predictive_table(G,FIRST_SET_STRINGS,FOLLOW_SET) is False:
        print("Error. Is not LL(1) Grammar, it was tried to input two productions in the same cell of the matrix")

    print("-----------------------------")
    print("Bottom-Up Parsing")
    print("-----------------------------")

    automata = Graph()
    first_table_automata(automata, G)
    for i in automata.vertices:
        print(i, automata.vertices[i].items,automata.vertices[i].collections, automata.vertices[i].neighbours)


def test_grammars():
    with open('grammars.txt', 'r') as file:
        lines = file.read().split('\n\n')  # Splitting grammars based on blank lines

        for grammar_str in lines:
            grammar_analyze = grammar_str.split('\n')
            print(grammar_analyze)
            nonterminals = grammar_analyze[0].split()
            print(nonterminals)
            terminals = grammar_analyze[1].split()
            print(terminals)
            productions = {}
            for i in range(len(nonterminals)):
                production = grammar_analyze[i + 2]
                productions[production.split('-')[0]] = production.split("->", 1)[1]
                productions[production.split('-')[0]] = productions[production.split('-')[0]].split("|")
            print(productions)
            start = grammar_analyze[-1]
            print(start)
            
            G = grammar(nonterminals, terminals, productions, start)

            print("-----------------------------")
            print("Top-Down Parsing")
            print("-----------------------------")

            FIRST_SET = {}
            FIRST_SET_STRINGS = {}
            for i in nonterminals:
                FIRST_SET[i] = set()
                FIRST_SET_STRINGS[i] = None
            for i in FIRST_SET.keys():
                value = FIRST(G, i, productions[i], FIRST_SET)[1]
                FIRST_SET_STRINGS[i] = value

            FOLLOW_SET = {}
            for i in nonterminals:
                FOLLOW_SET[i] = set()
                FOLLOW_SET[start].add('$')
            for i in FOLLOW_SET.keys():
                FOLLOW(FIRST_SET, G, i, FOLLOW_SET)

            if predictive_table(G,FIRST_SET_STRINGS,FOLLOW_SET) is False:
                print("Error. Is not LL(1) Grammar, it was tried to input two productions in the same cell of the matrix")

            print("-----------------------------")
            print("Bottom-Up Parsing")
            print("-----------------------------")

            automata = Graph()
            first_table_automata(automata, G)
            for i in automata.vertices:
                print(i, automata.vertices[i].who_items, automata.vertices[i].items, automata.vertices[i].who_collections, automata.vertices[i].collections, automata.vertices[i].neighbours)

            top_down_table(G, automata)
