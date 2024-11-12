# Import necessary libraries
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

# Read grammar from file
grammar_file = input('***THIS IS A SIMPLE LL(1) PARSER***\nPlease, input the grammar file\t: ')
input_string = input('Please, input the string\t\t: ')

# Read the grammar from file
grammar = {}
with open(grammar_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line == '':
            continue
        # Handle both '→' and '->' as separators
        if '→' in line:
            lhs, rhs = line.split('→')
        elif '->' in line:
            lhs, rhs = line.split('->')
        else:
            print('Error: Invalid grammar line "{}" (no "→" or "->" found)'.format(line))
            continue
        lhs = lhs.strip()
        rhs = rhs.strip()
        productions = [prod.strip() for prod in rhs.split('|')]
        if lhs in grammar:
            grammar[lhs].extend(productions)
        else:
            grammar[lhs] = productions

# Terminals and non-terminals
non_terminals = list(grammar.keys())
terminals = set()
for prods in grammar.values():
    for prod in prods:
        for symbol in prod:
            if symbol.islower() or symbol in ('a', 'b', 'c', 'd', 'e'):
                terminals.add(symbol)
terminals = list(terminals)

# LL(1) Parsing Table
# As per the provided FIRST and FOLLOW sets, the parsing table is:

parsing_table = {
    'S': {
        'a': 'aSe',
        'b': 'B',
        'c': 'B',
        'd': 'B',
    },
    'B': {
        'b': 'bBe',
        'c': 'C',
        'd': 'C',
    },
    'C': {
        'c': 'cCe',
        'd': 'd',
    }
}

# Append $ to input string to signify end of input
input_string += '$'
input_ptr = 0  # Pointer to the input string

# Root of the parse tree
root = Node('S')

# Stack for parsing
stack = []
# Initialize the stack with the start symbol and $
# Each element in the stack is a tuple (symbol, node)
stack.append(('$', None))
stack.append(('S', root))

# Function to perform LL(1) parsing
def parse():
    global input_ptr
    current_symbol = input_string[input_ptr]
    while len(stack) > 0:
        top_symbol, node = stack.pop()
        if top_symbol == '$' and current_symbol == '$':
            print('Input string is accepted.')
            return root
        elif top_symbol in terminals or top_symbol == '$':
            if top_symbol == current_symbol:
                # Terminal matched, move input pointer
                input_ptr += 1
                current_symbol = input_string[input_ptr]
            else:
                print('Error: expected "{}" but found "{}"'.format(top_symbol, current_symbol))
                return None
        elif top_symbol in non_terminals:
            if current_symbol in parsing_table[top_symbol]:
                production = parsing_table[top_symbol][current_symbol]
                # Create child nodes for the production symbols
                children = []
                for symbol in production[::-1]:
                    child_node = Node(symbol)
                    children.insert(0, child_node)
                # Attach child nodes to the current node
                node.children = children
                # Push RHS of production onto the stack in reverse order
                for symbol, child_node in zip(production[::-1], children):
                    stack.append((symbol, child_node))
            else:
                print('Error: no rule for {} with input {}'.format(top_symbol, current_symbol))
                return None
        else:
            print('Error: invalid symbol on stack "{}"'.format(top_symbol))
            return None
    if current_symbol == '$':
        print('Input string is accepted.')
        return root
    else:
        print('Error: input not fully consumed.')
        return None

# Start parsing
parse_tree_root = parse()

# If parse tree is built, display it
if parse_tree_root:
    print('\nVisual of The Resulting Parse Tree:')
    for pre, fill, node in RenderTree(parse_tree_root):
        print("%s%s" % (pre, node.name))
    # Optionally, export the parse tree to a file
    # Uncomment the next line if you have Graphviz installed
    # DotExporter(parse_tree_root).to_picture("parse_tree.png")
else:
    print('Parsing failed due to errors.')
