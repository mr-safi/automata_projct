from fa import NFA, DFA
filename = 'input.txt'
file = open(filename, 'r')
lines = file.readlines()
file.close()
nfa = NFA()
dfa = DFA()

#..........section 1 ...........
print(".........................section 1 : nfa to dfa...............\n")
nfa.construct_nfa_from_file(lines)
dfa.convert_from_nfa(nfa)
dfa.print_dfa()

