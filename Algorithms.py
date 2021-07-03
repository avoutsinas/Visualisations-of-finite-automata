import numpy as np
from Preliminaries import *
from FA import *


def powerset(nfa):
    nfa_states = []
    for st in nfa.Q:
        nfa_states.append(st.get_name())

    powerset = [""]
    for i in nfa_states:
        for sub in powerset:
            if sub == "":
                powerset = powerset + [str(sub) + str(i)]
            else:
                powerset = powerset + [str(sub) + "," + str(i)]
    return powerset


def powerset_construction(nfa):
    Q = []
    sigma = nfa.sigma
    Q.append(nfa.Q[0])
    transitions_to_add = []
    pwrst = powerset(nfa)
    #print(pwrst)

    for s0 in Q:
        #print("For state " + str(s0))
        transitions = []
        for t in nfa.d:
            if t.get_start_name() in s0.get_name():
                transitions.append(t)

        for letter in nfa.sigma:
            temp_transitions = [tr for tr in transitions if tr.letter == letter]
            new_state_name = ""
            starting = False
            final = False
            end_states = []
            d_memory = []

            for t in temp_transitions:
                #print(t)

                if len(t.get_end_states()) > 1:
                    for s in t.get_end_states():
                        if s.is_final:
                            final = True
                        if new_state_name == "":
                            new_state_name += s.get_name()
                        else:
                            new_state_name += "," + s.get_name()
                        if s not in end_states:
                            end_states.append(s)

                elif len(t.get_end_states()) == 1:
                    end_s = t.get_end_states()[0]
                    if end_s.is_final:
                        final = True

                    if end_s.get_name() != "{}":
                        if new_state_name == "":
                            new_state_name += end_s.get_name()
                        else:
                            new_state_name += "," + end_s.get_name()

            if new_state_name == Q[0].get_name():
                starting = True

            s_ = state(new_state_name, starting, final)

            if s_.get_name() == "{}":
                s_ = s0

            if s_.get_name() in pwrst:
                if s_ == s0:
                    transitions_to_add.append(transition(s0, t.letter, s0))
                    d_memory.append(transition(s0, t.letter, s0))
                else:
                    transitions_to_add.append(transition(s0, t.letter, s_))
                    d_memory.append(transition(s0, t.letter, s_))
                    if s_ not in Q:
                        Q.append(s_)

                #print("End State : " + new_state_name)
            if len(d_memory) > 1:
                new_state_name2 = ""
                starting2 = False
                final2 = False
                end_states2 = []
                for i in d_memory:
                    #print("checking " + str(i.get_start_state().get_name()) + " for letter " + letter)

                    if i in transitions_to_add and i.letter == letter:
                        transitions_to_add.remove(i)

                        end = i.get_end_state()

                        if end not in end_states2:
                            if end.is_final:
                                final2 = True
                            if new_state_name2 == "":
                                new_state_name2 += end.get_name()
                            else:
                                new_state_name2 += "," + end.get_name()
                            if end not in end_states2:
                                end_states2.append(end)

                s__ = state(new_state_name2, starting2, final2)

                if s__.get_name() in pwrst:
                    transitions_to_add.append(transition(i.get_start_state(), i.letter, s__))
                    if s__ not in Q:
                        Q.append(s__)

                # for q in Q:
                # print(q)
                #print("-------------------------------------------------------")
            else:
                pass

    output_dfa = dfa("Converted", [])

    for i in range(len(Q)):
        output_dfa.add_state(Q[i].get_name(), Q[i].is_final)

    for j in transitions_to_add:
        output_dfa.add_transition(j.get_start_state(), j.letter, j.get_end_state())

    print(output_dfa)
