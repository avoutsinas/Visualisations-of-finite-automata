import numpy as np
from Preliminaries import *
from FA import *


def is_nfa(nfa):
    pass


def find_powerset(nfa):
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


def merge_state(same_letter_transitions, q):
    new_state_name = ""
    starting = False
    final = False

    for t in same_letter_transitions:
        # print(t)

        if len(t.get_end_states()) > 1:
            print("more than one end states")
            for s in t.get_end_states():
                if s.is_final:
                    final = True
                if new_state_name == "":
                    new_state_name += s.get_name()
                else:
                    new_state_name += "," + s.get_name()

        elif len(t.get_end_states()) == 1:
            print("one end state")
            end_s = t.get_end_states()[0]
            if end_s.is_final:
                final = True

            if end_s.get_name() != "{}":
                if new_state_name == "":
                    new_state_name += end_s.get_name()
                else:
                    new_state_name += "," + end_s.get_name()

    if new_state_name == q[0].get_name():
        starting = True

    return new_state_name, starting, final


def merge_end_state(letter, d_memory, transitions_to_add):
    new_state_name2 = ""
    starting2 = False
    final2 = False
    end_states = []

    for i in d_memory:
        # print("checking " + str(i.get_start_state().get_name()) + " for letter " + letter)

        if i in transitions_to_add and i.letter == letter:
            transitions_to_add.remove(i)

            end_s = i.get_end_state()

            if end_s not in end_states:
                if end_s.is_final:
                    final2 = True
                if new_state_name2 == "":
                    new_state_name2 += end_s.get_name()
                else:
                    new_state_name2 += "," + end_s.get_name()
                if end_s not in end_states:
                    end_states.append(end_s)

    return new_state_name2, starting2, final2


def dfa_conversion(nfa):
    Q = []
    sigma = nfa.sigma
    Q.append(nfa.Q[0])
    transitions_to_add = []
    powerset = find_powerset(nfa)
    # print(powerset)

    for s0 in Q:
        # print("For state " + str(s0))
        state_transitions = []
        for t in nfa.d:
            if t.get_start_name() in s0.get_name():
                state_transitions.append(t)

        for letter in nfa.sigma:
            state_letter_transitions = [i for i in state_transitions if i.letter == letter]
            d_memory = []

            new_state_name, starting, final = merge_state(state_letter_transitions, Q)

            s_ = state(new_state_name, starting, final)

            if s_.get_name() == "{}":
                s_ = s0

            if s_.get_name() in powerset:
                if s_ == s0:
                    transitions_to_add.append(transition(s0, letter, s0))
                    d_memory.append(transition(s0, letter, s0))
                else:
                    transitions_to_add.append(transition(s0, letter, s_))
                    d_memory.append(transition(s0, letter, s_))
                    if s_ not in Q:
                        Q.append(s_)

                print (d_memory[0])
                # print("End State : " + new_state_name)

            if len(d_memory) > 1:
                print("end states has 2 or more end states")
                new_state_name2 = ""
                starting2 = False
                final2 = False
                end_states = []

                for i in d_memory:
                    # print("checking " + str(i.get_start_state().get_name()) + " for letter " + letter)

                    if i in transitions_to_add and i.letter == letter:
                        transitions_to_add.remove(i)

                        end_s = i.get_end_state()

                        if end_s not in end_states:
                            if end_s.is_final:
                                final2 = True
                            if new_state_name2 == "":
                                new_state_name2 += end_s.get_name()
                            else:
                                new_state_name2 += "," + end_s.get_name()
                            if end_s not in end_states:
                                end_states.append(end_s)

                s__ = state(new_state_name2, starting2, final2)

                if s__.get_name() in powerset:
                    transitions_to_add.append(transition(s_, letter, s__))
                    if s__ not in Q:
                        Q.append(s__)

                # for q in Q:
                # print(q)
                # print("-------------------------------------------------------")
            else:
                pass

    dfa_name = "Converted " + nfa.name
    output_dfa = dfa(dfa_name, [])

    for i in range(len(Q)):
        output_dfa.add_state(Q[i].get_name(), Q[i].is_final)

    for j in transitions_to_add:
        output_dfa.add_transition(j.get_start_state(), j.letter, j.get_end_state())

    print(output_dfa)
