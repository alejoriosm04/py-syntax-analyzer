from testing import *

def main():
    while True:
        print('-----------------------------')
        print('Final Project - Formal Languages and Compilers - ST0246')
        print('Alejandro Ríos Muñoz - Kristian Restrepo')
        print('-----------------------------')
        print('0. Exit.')
        print('1. Read testing grammars file.')
        print('2. Read user grammar.')

        option = input('Select an option: ')
        if option == '0':
            break
        elif option == '1':
            test_grammars()
        elif option == '2':
            test_user_grammar()


if __name__ == '__main__':
    main()
