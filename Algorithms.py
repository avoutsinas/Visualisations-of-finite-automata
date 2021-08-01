import numpy as np
from Preliminaries import *
from FA import *

"""******************************************* NFA TO DFA **********************************************************"""


class Determinise(object):

    @classmethod
    def find_powerset(cls, n):
        nfa_states = []
        for st in n.get_Q():
            nfa_states.append(st.get_name())

        powerset = [""]
        for i in nfa_states:
            for sub in powerset:
                if sub == "":
                    powerset = powerset + [str(sub) + str(i)]
                else:
                    powerset = powerset + [str(sub) + "," + str(i)]
        return powerset

    @classmethod
    def epsilon_closure(cls, all_states, nfa_transitions, powerset):
        q = all_states
        q0 = []
        d = nfa_transitions
        empty_d = []
        epsilon_closures = []

        for s in q:
            for t in d:
                flag_lst = [t.get_start_name(), "{}"]
                if t.get_start_name() in s.get_name() and t.letter == epsilon and t.get_end_name() not in flag_lst:
                    empty_d.append(t)
                    temp = t.get_start_state()
                    if temp not in q0:
                        q0.append(temp)

        for s0 in q0:
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
                            # print("caught")
                            final = True
                        if es.get_name() not in s0.get_name() and et.get_start_name() == s0.get_name():
                            # print("passed name check")
                            combined_name += "," + es.get_name()

            combined_state = State(combined_name, start, final)

            if combined_name in powerset:
                # print("found")
                for j in nfa_transitions:
                    if j.get_start_name() in combined_name and j.letter == epsilon \
                            and j.get_end_name() not in combined_name:
                        to_append = NfaTransition(combined_state, j.letter, [k for k in j.get_end_states()])
                        empty_d.append(to_append)
                        # print(NfaTransition(combined_state, j.letter, [k for k in j.get_end_states()]))

                    if combined_state not in q0:
                        q0.append(combined_state)

                        if s0 in epsilon_closures:
                            idx = epsilon_closures.index(s0)
                            epsilon_closures[idx] = combined_state
                        else:
                            epsilon_closures.append(combined_state)
                        # print("Combined state: " + str(combined_state))
                        # print("\n")

        return epsilon_closures

    @classmethod
    def merged_state(cls, same_letter_transitions, q):
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

    @classmethod
    def convert(cls, nfa):
        Q = []
        Q.append(nfa.get_Q()[0])
        transitions_to_add = []
        nfa_states = nfa.get_Q()
        sigma = nfa.get_sigma()
        delta = nfa.get_d()

        powerset = cls.find_powerset(nfa)
        print("POWERSET: " + str(powerset))

        if epsilon in sigma:
            sigma.remove(epsilon)

            empty_closures = cls.epsilon_closure(nfa_states, delta, powerset)

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

                new_state_name, starting, final = cls.merged_state(state_letter_transitions, Q)

                if new_state_name == "":
                    s_ = s0
                else:
                    s_ = State(new_state_name, starting, final)

                if s_.get_name() in powerset:
                    if s_ == s0:
                        transitions_to_add.append(DfaTransition(s0, letter, s0))
                    else:
                        transitions_to_add.append(DfaTransition(s0, letter, s_))
                        if s_ not in Q:
                            Q.append(s_)

                    # print("End State : " + new_state_name + " with letter " + letter)

        dfa_name = nfa.get_name() + ".to_DFA"
        output_dfa = Dfa(dfa_name)

        for i in range(len(Q)):
            output_dfa.add_state(Q[i].get_name(), Q[i].is_final)

        for j in transitions_to_add:
            output_dfa.add_transition(j.get_start_state(), j.letter, j.get_end_state())

        # print(output_dfa.get_table())
        print(output_dfa)


"""******************************************* DFA TO minDFA *******************************************************"""


class Minimise(object):

    @classmethod
    def remove_unreachable_states(cls, input_fa):
        fa_type = input_fa.type()

        d = input_fa.get_d()
        reachable_states = [input_fa.get_Q()[0]]
        new_states = [input_fa.get_Q()[0]]

        while new_states != []:
            temp = []
            for q in new_states:
                for l in input_fa.get_sigma():
                    if fa_type == "dfa":
                        temp += [t.get_end_state() for t in input_fa.get_d() if
                                 t.get_start_state() == q and t.letter == l and t.get_end_state() not in temp]
                    elif fa_type == "nfa":
                        temp += [i for t in input_fa.get_d() if t.get_start_state() == q and t.letter == l \
                                 for i in t.get_end_states() if i.get_name() != "{}" and i not in temp]

            new_states = [i for i in temp if i not in reachable_states]
            reachable_states += new_states

        unreachable_states = [s for s in input_fa.get_Q() if s not in reachable_states]
        reachable_transitions = [t for t in d if t.get_start_state() in reachable_states]

        if unreachable_states == []:
            print("no unreachable states found")
            return input_fa
        else:
            name = "rs_" + input_fa.get_name()
            output_fa = cls.assemble_fa(input_fa, name, reachable_states, reachable_transitions)
            print(output_fa)
            return output_fa

    @classmethod
    def hopcroft_algorithm(cls, input_dfa):
        p = input_dfa.get_F()
        p = [p, [s for s in input_dfa.get_Q() if s not in input_dfa.get_F()]]
        w = p.copy()

        while w != []:
            # print("W = " + str(w))
            current_set = w.pop(0)
            # print("Current set: " + str(current_set))
            for l in input_dfa.get_sigma():
                # print("For letter " + l)
                x = []
                x = [t.get_start_state() for t in input_dfa.get_d() if t.get_end_state() in current_set \
                     and t.letter == l and t.get_start_state() not in x]
                # print(x)
                for y in p:
                    intersection = [st1 for st1 in y if st1 in x]
                    diff = [st2 for st2 in y if st2 not in x]

                    if intersection != [] and diff != []:
                        # print("Intersection = " + str(intersection))
                        # print("Difference = " + str(diff))
                        p.remove(y)
                        p.append(intersection)
                        p.append(diff)
                        if y in w:
                            w.remove(y)
                            w.append(intersection)
                            w.append(diff)
                        else:
                            if len(intersection) <= len(diff):
                                w.append(intersection)
                            else:
                                w.append(diff)
        print("Partitions = " + str(p))
        return p

    @classmethod
    def assemble_fa(cls, fa, name, r_s, r_t):
        tp = fa.type()
        output_fa = None

        if tp == "dfa":
            output_fa = Dfa(name)

            for i in range(len(r_s)):
                output_fa.add_state(r_s[i].get_name(), r_s[i].is_final)

            for j in r_t:
                output_fa.add_transition(j.get_start_state(), j.letter, j.get_end_state())

        elif tp == "nfa":
            output_fa = Nfa("min_" + fa.get_name())

            for i in range(len(r_s)):
                output_fa.add_state(r_s[i].get_name(), r_s[i].is_final)

            for j in r_t:
                for e_s in j.get_end_states():
                    output_fa.add_transition(j.get_start_state(), j.letter, e_s)

        return output_fa

    @classmethod
    def convert(cls, dfa):
        r_s_dfa = cls.remove_unreachable_states(dfa)
        partitions = cls.hopcroft_algorithm(r_s_dfa)

        num_partitions = [len(set) for set in partitions]

        if max(num_partitions) > 1:
            new_Q = []
            new_d = []

            for p_set in partitions:
                new_state_name = ""
                start = False
                final = False
                if len(p_set) > 1:
                    for s in p_set:
                        if s.is_start:
                            start = True
                        if s.is_final:
                            final = True
                        if new_state_name == "":
                            new_state_name += s.get_name()
                        elif s.get_name() not in new_state_name:
                            new_state_name += "," + s.get_name()
                    new_state = State(new_state_name, start, final)
                else:
                    new_state = p_set[0]

                if new_state not in new_Q:
                    new_Q.append(new_state)

            start_state = [s for s in new_Q if s.is_start]
            start_state = start_state[0]
            new_Q.remove(start_state)
            new_Q.insert(0, start_state)
            # print(new_Q)

            for letter in dfa.get_sigma():
                new_transition = ""
                for s in new_Q:
                    for t in dfa.get_d():
                        if t.get_start_name() in s.get_name() and letter == t.letter:
                            end_state = []
                            end_state = [i for i in new_Q if t.get_end_name() in i.get_name() and i not in end_state]
                            new_transition = DfaTransition(s, letter, end_state[0])
                    new_d.append(new_transition)

            # print(new_d)
            name = "min_" + dfa.get_name()
            output_dfa = cls.assemble_fa(r_s_dfa, name, new_Q, new_d)

            print(output_dfa)
            return output_dfa

        else:
            print("No non-distinguishable states found")
            return r_s_dfa
