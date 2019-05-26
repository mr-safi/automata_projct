import string


class NFA:
    def __init__(self):
        self.num_states = 0
        self.states = []
        self.symbols = []
        self.num_accepting_states = 0
        self.accepting_states = []
        self.start_state = 0
        self.transition_functions = []

    def init_states(self):
        self.states = list(range(self.num_states))

    def print_nfa(self):
        print(self.num_states)
        print(self.states)
        print(self.symbols)
        print(self.num_accepting_states)
        print(self.accepting_states)
        print(self.start_state)
        print(self.transition_functions)

    def construct_nfa_from_file(self, lines):
        self.num_states = int(lines[0])
        self.init_states()

        temp = lines[1].rstrip()
        self.symbols = list(temp.split(","))

        for index in range(2, len(lines)):
            temp = lines[index].rstrip()
            temp = temp.replace('q', '')
            transition_func_line = temp.split(",")

            if transition_func_line[0][0:2] == "->":
                transition_func_line[0] = transition_func_line[0][2:]
                self.start_state = int(transition_func_line[0])

            if transition_func_line[0][0] == "*":
                transition_func_line[0] = transition_func_line[0][1:]
                if not self.accepting_states.__contains__(int(transition_func_line[0])):
                    self.accepting_states.append(int(transition_func_line[0]))
                    # self.num_accepting_states += 1

            starting_state = int(transition_func_line[0])

            transition_symbol = transition_func_line[1]

            if transition_func_line[2][0] == "*":
                transition_func_line[2] = transition_func_line[2][1:]
                if not self.accepting_states.__contains__(int(transition_func_line[2])):
                    self.accepting_states.append(int(transition_func_line[2]))
                    # self.num_accepting_states += 1

            ending_state = int(transition_func_line[2])

            transition_function = (starting_state, transition_symbol, ending_state);

            self.transition_functions.append(transition_function)
            # print(self.accepting_states)


class DFA:
    def __init__(self):
        self.num_states = 0
        self.symbols = []
        self.num_accepting_states = 0
        self.accepting_states = []
        self.start_state = 0
        self.transition_functions = []
        self.q = []

    def convert_from_nfa(self, nfa):
        self.symbols = nfa.symbols
        self.start_state = nfa.start_state

        nfa_transition_dict = {}
        dfa_transition_dict = {}

        # Combine NFA transitions
        for transition in nfa.transition_functions:
            # print(transition)
            starting_state = transition[0]
            transition_symbol = transition[1]
            ending_state = transition[2]

            if (starting_state, transition_symbol) in nfa_transition_dict:
                nfa_transition_dict[(starting_state, transition_symbol)].append(ending_state)
            else:
                nfa_transition_dict[(starting_state, transition_symbol)] = [ending_state]

        self.q.append((0,))

        for dfa_state in self.q:
            for symbol in nfa.symbols:
                # print(dfa_state,".........")
                if len(dfa_state) == 1 and (dfa_state[0], symbol) in nfa_transition_dict:
                    dfa_transition_dict[(dfa_state, symbol)] = nfa_transition_dict[(dfa_state[0], symbol)]

                    if tuple(dfa_transition_dict[(dfa_state, symbol)]) not in self.q:
                        self.q.append(tuple(dfa_transition_dict[(dfa_state, symbol)]))
                else:
                    destinations = []
                    final_destination = []

                    for nfa_state in dfa_state:
                        if (nfa_state, symbol) in nfa_transition_dict and nfa_transition_dict[
                            (nfa_state, symbol)] not in destinations:
                            destinations.append(nfa_transition_dict[(nfa_state, symbol)])

                    if not destinations:
                        final_destination.append(None)
                    else:
                        for destination in destinations:
                            for value in destination:
                                if value not in final_destination:
                                    final_destination.append(value)

                    dfa_transition_dict[(dfa_state, symbol)] = final_destination

                    if tuple(final_destination) not in self.q:
                        self.q.append(tuple(final_destination))

        # Convert NFA states to DFA states
        for key in dfa_transition_dict:
            self.transition_functions.append(
                (self.q.index(tuple(key[0])), key[1], self.q.index(tuple(dfa_transition_dict[key]))))

        for q_state in self.q:
            for nfa_accepting_state in nfa.accepting_states:
                if nfa_accepting_state in q_state:
                    self.accepting_states.append(self.q.index(q_state))
                    self.num_accepting_states += 1

    def print_dfa(self):
        print(len(self.q))
        print(",".join(self.symbols))

        for transition in sorted(self.transition_functions):

            temp1 = "q" + str(transition[0])
            temp2 = "q" + str(transition[2])
            if transition[0] == self.start_state:
                temp1 = "->" + temp1
            elif int(transition[0]) in self.accepting_states:
                temp1 = "*" + temp1

            if int(transition[2]) in self.accepting_states:
                temp2 = "*" + temp2

            temp3 = temp1 + "," + transition[1] + "," + temp2
            print(temp3)

    def toRegex(self):
        reg_dic = {}
        list2 = []
        complet_list = []

        for trans in sorted(self.transition_functions):

            t0 = trans[0]
            t1 = trans[1]
            t2 = trans[2]
            # reg_dic[t0].append(str(t1)+str(t2))
            if not reg_dic.__contains__(t0):
                list2.append(str(t1) + str(t2))
                reg_dic[t0] = list2
            else:
                list2.append(str(t1) + str(t2))
                reg_dic[t0] = list(list2)
                list2.clear()
        complet_list = list(reg_dic.keys())
        # for inedx in complet_list:
        counter = 0
        inedx = 0
        # print(reg_dic)
        while len(
                complet_list) != 0 and counter != 100:  # ...................................................while.......
            counter += 1

            if len(reg_dic.get(inedx)) < 5:
                k1 = reg_dic.get(inedx)[0]
                k2 = reg_dic.get(inedx)[1]
                # print(k1,k2 ,inedx)
                if k2[-1] == k1[-1]:
                    if k1[-1] != str(inedx):
                        reg_dic[inedx] = "(" + k1[0] + "+" + k2[0] + ")" + str(k1[-1])
                    else:
                        reg_dic[inedx] = "(" + k1[0] + "+" + k2[0] + ")" + "*"
                        complet_list.remove(inedx)

                else:
                    if (int(k1[-1]) not in complet_list) and (int(k2[-1]) not in complet_list):
                        tempk1 = reg_dic.get(int(k1[-1]))
                        tempk2 = reg_dic.get(int(k2[-1]))

                        reg_dic[inedx] = tempk1 + temp2;
                        complet_list.remove(inedx)
                    elif k1[-1] == str(inedx):
                        reg_dic[inedx] = k1[0] + "*" + "(" + k2 + ")"
                    elif k2[-1] == str(inedx):
                        reg_dic[inedx] = "(" + k1 + ")" + k2[0] + "*"

                    elif int(k1[-1]) not in complet_list:
                        tempk1 = reg_dic.get(int(k1[-1]))
                        reg_dic[inedx] = k1[0] + tempk1 + "(" + k2 + ")"
                        # print(reg_dic)

                    elif int(k2[-1]) not in complet_list:
                        tempk2 = reg_dic.get(int(k2[-1]))
                        reg_dic[inedx] = k1 + "(" + tempk2 + ")"
                        # print(reg_dic)

            else:
                # print(reg_dic)
                temp = reg_dic.get(inedx)
                for i in temp:
                    if i in string.digits:
                        if int(i) not in complet_list:
                            temp1 = reg_dic.get(int(i))
                            temp2 = temp.replace(i, temp1)
                            reg_dic[inedx] = temp2
                            complet_list.remove(inedx)

            inedx += 1
            if inedx == len(reg_dic):
                inedx = 0


        # print(max(reg_dic.values()))
        if counter == 100:
            print("erroe ! cant convert to regex")
        else:
            print(reg_dic)
            print()
            print(max(reg_dic.values()))
