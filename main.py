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

#...........section 3.........
# dfa in section 1 convert to regex
# the longset string in last line is final regex
# this regex not optimize , just merge equation of  states

print("\n..........................section 3 : dfa to regex....................\n")
dfa.toRegex()
