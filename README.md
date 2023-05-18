<h1 align="center">
    <tt>> py-syntax-analyzer</tt>
</h1>

Project for the third-semester course "Formal Languages and Compilers" (ST0270) taught at EAFIT University by Sergio Ramirez.

## Getting Started

## Install and Usage

## Documentation

On this section, you will find the explanation for all the functions on this program. Please, take into account that those functions have
a very complex theory background, so it is recommended to have clearly understood the theory before reading this documentation.

### Grammar Definition

In the file `grammar.py` is defined the class `Grammar` which is used to represent a grammar. This class has the following attributes:
- `non_terminals`: A list of strings representing the non-terminals of the grammar.
- `terminals`: A list of strings representing the terminals of the grammar.
- `productions`: A dictionary where the keys are the non-terminals and the values are lists of strings representing the productions of the grammar.
- `start`: A string representing the start symbol of the grammar.

On this project, there are two ways to read and test and grammar. The first one is to read the grammar from a file. The second one is to read the user input. This works with the same funcionality in their respective functions.

The `non_terminals` and `terminals` attributes are read from the file or the user input and stored as lists. The `productions` attribute is read from the file or the user input and is stored in a dictionary where the keys are the non-terminals and the values are lists of strings representing the productions of the grammar. The `start` attribute is read from the file or the user input.

This data is sent to the Grammar class and created a new object. This object is sent to the respective functions to calculate all the necesary analysis data.

### FIRST

We defined a `FIRST`function in `grammar.py`, this function receives as parameters: the grammar, a symbol, a production and a dictionary of `FIRST` sets. This function returns the `FIRST` set of the symbol.

1. Initialize variables: 
- `position` is used to keep track of the current position in the list used to store the elements added to the FIRST set during the calculation.
- `list` is a list of lists used to store the elements added to the FIRST set for each production.
- `value` is a boolean variable used as a flag to avoid removing epsilon from the FIRST set if the current nonterminal symbol can derive ε.

2. Iterate over each production in the list of productions (`P`):

- Initialize a counter variable `counter` to keep track of the progress in the current production.

3. Iterate over each element in the current production:
- If the element is ε (epsilon), add it to the current list in the `list` variable.
- If the element is a terminal, add it to the FIRST set for the symbol and the current list, then break the loop to move to the next production.
- If the element is a nonterminal, recursively call the `FIRST` function to calculate the FIRST set for that nonterminal.
        
    - If the recursive call returns True, it means the nonterminal can derive ε, so add its FIRST set to the FIRST set of the current symbol and add the elements to the current list.
    - If the recursive call returns False, it means the nonterminal cannot derive ε, so add its FIRST set to the FIRST set of the current symbol, add the elements to the current list, and break the loop to move to the next production.
    - If ε (epsilon) is present in the FIRST set of the nonterminal and the value flag is False, remove ε from the FIRST set of the current symbol and remove it from the current list.
    - If the counter is equal to the length of the production, it means all elements in the production can derive ε.
    - If ε is present in the FIRST set of the last element, add it to the FIRST set of the current symbol, add it to the current list, and set the value flag to True.

4. Update the position variable to move to the next list in the list variable.

5. Check if ε (epsilon) is present in the list of productions (P):
If ε is present, add it to the FIRST set of the current symbol.

6. Check if ε (epsilon) is present in the FIRST set of the current symbol:
If ε is present, return True and the list variable.
Otherwise, return False and the list variable.

### FOLLOW

1. Iterate over each nonterminal in the set of productions (`G.productions`):
- Initialize a counter variable `counter` to keep track of whether all terms derive ε (epsilon) until the end of the production. If so, we need to calculate the FOLLOW set for the current nonterminal.

2. Iterate over each production in the list of productions for the current nonterminal:
Count the number of occurrences of the symbol in the production using the `count()` method.

3. If the symbol is present in the production:
- Initialize the index variable to -1, which allows updating the position in case there is more than one occurrence of the symbol in the production. This ensures that we ignore the previously evaluated occurrences and continue with the next one.
- Iterate over each occurrence of the symbol in the production:
    - Find the index of the occurrence and update the index variable to point to the next occurrence (if any).
    - If the index is not -1 (i.e., there is a valid index):
        - Iterate over each character next following the symbol in the production:
            - If `next` is a terminal, add it to the FOLLOW set of the current symbol and break the loop to stop evaluating the remaining characters.
            - If `next` is a nonterminal:
                - Add the FIRST set of the next nonterminal to the FOLLOW set of the current symbol.
                - If ε (epsilon) is present in the FIRST set of the next nonterminal, continue evaluating the remaining elements in the production, increment the counter by 1, and remove ε from the FOLLOW set of the current symbol that was added previously.
                - Otherwise, stop evaluating that production.
        - If the `counter` is equal to the length of the remaining characters in the production after the symbol, it means we are at the end of the production, and we need to use property 3. We add the FOLLOW set of the nonterminal from which the production is derived to the FOLLOW set of the current symbol.
            - If the FOLLOW set of the nonterminal is empty, we recursively call the `FOLLOW` function to calculate its FOLLOW set and add it to the current symbol's FOLLOW set.
            - Otherwise, we directly add the FOLLOW set of the nonterminal to the current symbol's FOLLOW set.

4. Check if there are no more occurrences of the symbol in the production:
Break the loop as there are no more occurrences to process.

5. Print the final `FOLLOW_SET` dictionary for debugging purposes.

Note: The code doesn't return any value, but it updates the FOLLOW_SET dictionary as a side effect.

### LL1() Parsing Table

First of all, we created a function called `give_positions`. This function is responsible for assigning positions (numeric values) to terminals and nonterminals. It creates a dictionary where the keys are the terminals or nonterminals, and the values are the assigned numbers.

Then, we created another function called `predictive_table`. This function is responsible for constructing the predictive parsing table using the given grammar, FIRST sets, and FOLLOW sets.


1. Create two dictionaries:
    - `positions_nonterminals` using the give_positions function to assign positions to the nonterminals.
    - `positions_terminals` using the give_positions function to assign positions to the terminals.
2. Create an empty list called `table` to store the values of the predictive parsing table.
3. Create a 2D table with `len(G.nonterminals)` rows and `len(G.terminals)+1` columns (including the column for nonterminals).
    - Initialize each cell of the table with the string "∞" to indicate that there is no data related to that position initially.
4. Iterate over each nonterminal `i` in the grammar:
    - Iterate over each production `j` of that nonterminal:
    - Iterate over each element `k` in the FIRST set of that production:
        - If k is not "Ɛ" (epsilon):
            - Check if the table cell at the position `[positions_nonterminals[i]][positions_terminals[k]]` is "∞":
                - If it is "∞", assign the corresponding production G.productions[i][j] to that table cell.
                - Otherwise, return False indicating a conflict in the parsing table.
        - If `k` is "Ɛ" (epsilon):
            - Iterate over each element `z` in the FOLLOW set of `i`:
                - Check if the table cell at the position `[positions_nonterminals[i]][positions_terminals[z]]` is "∞":
                - If it is "∞", assign "Ɛ" to that table cell.
                - Otherwise, return `False` indicating a conflict in the parsing table.
5. Call the `print_table` function to print the constructed parsing table.
6. Call the `string_input_top_down` function to analyze strings using the constructed parsing table.

Finally:
1. Create an instance of the PrettyTable class called `pretty_table`.
2. Set the field names of the table using the list of terminal positions as column headers, preceded by an empty string as the column for nonterminals.
3. Create a copy of the `table` list to avoid modifying the original list.
4. For each row in the `table`:
    - Convert the row to a deque to manipulate it easily.
    - Add the corresponding nonterminal to the beginning of the deque.
    - Convert the deque back to a list.
5. Add each row to the `pretty_table`.
6. Print the table title and the `pretty_table`.


### String Analysis - (Top-Down)

1. This function receives the string that the user enters and the G object that contains the grammar.
2. The deque library is used to create a stack that will be used to evaluate the string.
3. The stack is initialized with the non-terminal symbol and the initial symbol of the grammar. The latter is at the top of the stack.
4. The function checks that the string entered by the user is in the language of the grammar. If not, it returns an error.
5. The string is concatenated with the symbol $ to know that the string was fully traversed.
6. Then, X is assigned the value of the top of the stack and a is assigned the value of the first character in the string.
7. While the top of the stack is different from $, the function performs the following steps:
    - If X is a terminal, the function checks if it is equal to a. If so, it removes X from the stack and updates the string and a.
    - If X is a non-terminal, the function checks if the value in the table at the position of X and a is equal to "∞". If so, it returns an error.
    - If not, the function removes X from the stack and reverses the string in the table at the position of X and a. Then, the function adds each character of the string to the stack.
8. If the top of the stack is equal to $, the function returns that the string is accepted.


## Authors

This program was developed by [Alejandro Ríos](https://github.com/alejoriosm04) and [Kristian Restrepo](https://github.com/kristianrpo).