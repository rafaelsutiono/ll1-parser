from anytree import Node, RenderTree
from anytree.exporter import DotExporter


grammar_file = input('***THIS IS A SIMPLE LL(1) PARSER***\nPlease, input the grammar file\t: ')
input_string = input('Please, input the string\t\t: ')

# read grammar
grammar = {}
with open(grammar_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line == '':
            continue
        # both '→' and '->' can be separators
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


non_terminals = list(grammar.keys())
terminals = set()
for prods in grammar.values():
    for prod in prods:
        for symbol in prod:
            if symbol.islower() or symbol in ('a', 'b', 'c', 'd', 'e'):
                terminals.add(symbol)
terminals = list(terminals)


# parse table
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


input_string += '$'
input_ptr = 0  

# root of parse tree
root = Node('S')

# stack for parsing
stack = []
# initialize the stack with the start symbol and $
# each element in the stack is a tuple (symbol, node)
stack.append(('$', None))
stack.append(('S', root))

# function to perform LL(1) parsing
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
                # terminal matched, move input pointer
                input_ptr += 1
                current_symbol = input_string[input_ptr]
            else:
                print('Error: expected "{}" but found "{}"'.format(top_symbol, current_symbol))
                return None
        elif top_symbol in non_terminals:
            if current_symbol in parsing_table[top_symbol]:
                production = parsing_table[top_symbol][current_symbol]
                # create child nodes for the production symbols
                children = []
                for symbol in production[::-1]:
                    child_node = Node(symbol)
                    children.insert(0, child_node)
                # attach child nodes to the current node
                node.children = children
                # push RHS of production onto the stack in reverse order
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

# start parsing
parse_tree_root = parse()

# if parse tree is built, display it
if parse_tree_root:
    print('\nVisual of The Resulting Parse Tree:')
    for pre, fill, node in RenderTree(parse_tree_root):
        print("%s%s" % (pre, node.name))
else:
    print('Parsing failed due to errors.')
