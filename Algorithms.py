import numpy as np
from Preliminaries import *
from FA import *


def is_nfa(n):
    pass


def find_powerset(n):
    nfa_states = []
    for st in n.Q:
        nfa_states.append(st.get_name())

    powerset = [""]
    for i in nfa_states:
        for sub in powerset:
            if sub == "":
                powerset = powerset + [str(sub) + str(i)]
            else:
                powerset = powerset + [str(sub) + "," + str(i)]
    return powerset


def epsilon_closure(all_states, nfa_transitions, powerset):
    q = all_states
    d = nfa_transitions.copy()
    empty_d = []
    epsilon_closures = []

    for s in q:
        for t in d:
            if t.get_start_name() in s.get_name() and t.letter == epsilon and t.get_end_name() != "{}":
                empty_d.append(t)

    for s0 in q:
        combined_name = s0.get_name()
        start = s0.is_start
        final = s0.is_final

        # print("--------------------------------------")
        # print("For state " + str(s0))

        if empty_d != []:
            # print("caught")
            for et in empty_d:
                # print(t)
                for es in et.get_end_states():
                    if es.is_start:
                        start = True
                    if es.is_final:
                        final = True
                    if es.get_name() not in s0.get_name() and et.get_start_name() == s0.get_name():
                        # print("passed name check")
                        combined_name += "," + es.get_name()

        combined_state = state(combined_name, start, final)
        # print(combined_state)

        if combined_name in powerset:
            # print("found")
            for j in nfa_transitions:
                if j.get_start_name() in combined_name and j.letter == epsilon \
                        and j.get_end_name() not in combined_name:

                    to_append = nfa_transition(combined_state, j.letter, [k for k in j.get_end_states()])
                    empty_d.append(to_append)
                    # print(nfa_transition(combined_state, j.letter, [k for k in j.get_end_states()]))

                if combined_state not in q:
                    q.append(combined_state)

                    if s0 in epsilon_closures:
                        idx = epsilon_closures.index(s0)
                        epsilon_closures[idx] = combined_state
                    else:
                        epsilon_closures.append(combined_state)
                    # print("Combined state: " + str(combined_state))
                    # print("\n")
    return epsilon_closures


def merged_state(same_letter_transitions, q):
    new_state_name = ""
    starting = False
    final = False

    for t in same_letter_transitions:
        # print(t)

        if len(t.get_end_states()) > 1:
            # print("more than one end states")
            for s in t.get_end_states():
                if s.is_final:
                    final = True
                if new_state_name == "":
                    new_state_name += s.get_name()
                else:
                    new_state_name += "," + s.get_name()

        elif len(t.get_end_states()) == 1:
            # print("one end state")
            end_s = t.get_end_states()[0]

            if end_s.is_final:
                final = True
            if end_s.get_name() != "{}":
                if new_state_name == "":
                    new_state_name += end_s.get_name()
                elif end_s.get_name() not in new_state_name:
                    new_state_name += "," + end_s.get_name()

    if new_state_name == q[0].get_name():
        starting = True

    # print(new_state_name, starting, final)
    return new_state_name, starting, final


def dfa_conversion(nfa):
    Q = []
    Q.append(nfa.Q[0])
    transitions_to_add = []

    nfa_states = nfa.Q.copy()
    sigma = nfa.sigma.copy()
    delta = nfa.d.copy()

    powerset = find_powerset(nfa)
    print(powerset)

    if epsilon in sigma:
        sigma.remove(epsilon)

        empty_closures = epsilon_closure(nfa_states, delta, powerset)

        for i in empty_closures:
            if i.is_start:
                Q.pop(0)
                Q.append(i)
            else:
                Q.append(i)

    for s0 in Q:
        # print("For state " + str(s0))
        state_transitions = []

        for t in delta:
            if t.get_start_name() in s0.get_name():
                state_transitions.append(t)

        for letter in sigma:
            state_letter_transitions = [i for i in state_transitions if i.letter == letter]

            new_state_name, starting, final = merged_state(state_letter_transitions, Q)

            if new_state_name == "":
                s_ = s0
            else:
                s_ = state(new_state_name, starting, final)

            if s_.get_name() in powerset:
                if s_ == s0:
                    transitions_to_add.append(transition(s0, letter, s0))
                else:
                    transitions_to_add.append(transition(s0, letter, s_))
                    if s_ not in Q:
                        Q.append(s_)

                # print("End State : " + new_state_name + " with letter " + letter)

    dfa_name = "Converted " + nfa.name
    output_dfa = dfa(dfa_name)

    for i in range(len(Q)):
        output_dfa.add_state(Q[i].get_name(), Q[i].is_final)

    for j in transitions_to_add:
        output_dfa.add_transition(j.get_start_state(), j.letter, j.get_end_state())

    print(output_dfa)
