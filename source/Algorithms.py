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
    def assemble_dfa(cls, name, state_lst, d_lst, sigma):
        dfa_name = "Det(" + name + ")"
        output_dfa = Dfa(dfa_name)
        Q = []
        d = []

        if [garbage_state] in state_lst:
            state_lst.remove([garbage_state])
            state_lst.append([garbage_state])

        for state in state_lst:
            state_name = None
            start, final = False, False
            for simp_state in state:
                if state_name is None:
                    state_name = simp_state.get_name()
                else:
                    state_name += "," + simp_state.get_name()
                if simp_state.is_final:
                    final = True
                if state == state_lst[0]:
                    start = True
            s_to_append = State(state_name, start, final)
            Q.append(s_to_append)
        for t in d_lst:
            start_name, end_name = None, None
            letter = t[1]
            for s in t[0]:
                if start_name is None:
                    start_name = s.get_name()
                else:
                    start_name += "," + s.get_name()
            for s in t[2]:
                if end_name is None:
                    end_name = s.get_name()
                else:
                    end_name += "," + s.get_name()

            start_state = [s for s in Q if s.get_name() == start_name][0]
            end_state = [s for s in Q if s.get_name() == end_name][0]
            d_to_append = DfaTransition(start_state, letter, end_state)
            # print(to_append)
            d.append(d_to_append)

        for i in Q:
            output_dfa.add_state(i.get_name(), i.is_final)

        for j in d:
            output_dfa.add_transition(j.get_start_state(), j.letter, j.get_end_state())

        return output_dfa

    @classmethod
    def epsilon_closure(cls, q, d, first=False):

        if first == True:
            closure = [q]
            for t in d:
                if t.get_start_state() in closure and t.letter == epsilon:
                    temp = [s_ for s_ in t.get_end_states()]
                    for i in temp:
                        if i not in closure and i != empty_end_state:
                            closure.append(i)
            # print(closure)
        else:
            closure = q.copy()
            for t in d:
                for e_s in t.get_end_states():
                    # print(e_s)
                    if e_s not in closure and e_s != empty_end_state and t.letter == epsilon:
                        closure.append(e_s)

            closure = sorted(closure)

        return closure

    @classmethod
    def letter_closure(cls, e_closures, q, d):
        closure = []

        for t in d:
            for e_s in t.get_end_states():
                if e_s not in closure and e_s != empty_end_state:
                    closure.append(e_s)

        if closure == []:
            closure = [garbage_state]

        closure = sorted(closure)

        if len(closure) == 1:
            for e in e_closures:
                if e[0] == closure[0]:
                    closure = e
        elif len(closure) > 1:
            for e in e_closures:
                if e[0] == closure[0]:
                    for s_ in e:
                        if s_ not in closure:
                            closure.append(s_)

        closure = sorted(closure)

        return closure

    @classmethod
    def convert(cls, nfa, debug=False):
        powerset = cls.find_powerset(nfa)
        print("POWERSET: " + str(powerset))

        nfa_name = nfa.get_name()
        nfa_d = nfa.get_d()
        sigma = nfa.get_sigma()
        dfa_states = []
        dfa_transitions = []

        S = []

        nfa_start = nfa.Q[0]
        s0 = cls.epsilon_closure(nfa_start, nfa_d, first=True)
        dfa_states.append(s0)
        S.append(s0)

        if len(s0) > 1:
            e_closures = [s0]
        else:
            e_closures = []

        if epsilon in sigma:
            sigma.remove(epsilon)
            sigma.insert(0, epsilon)

        while S != []:
            cls.debug_text("\nS = " + str(S), debug)
            state = S.pop(0)

            for letter in sigma:
                state_letter_d = []
                cls.debug_text("\n\nfor state " + str(state) + " with letter " + letter, debug)
                all_transitions = [i for i in [t for t in [nfa.get_state_d(s) for s in state]]]

                for i in all_transitions:
                    for j in i:
                        if j.letter == letter:
                            state_letter_d.append(j)

                cls.debug_text("State-letter-Transitions: " + str(state_letter_d), debug)

                if letter == epsilon:
                    new_state = cls.epsilon_closure(state, state_letter_d, False)
                    cls.debug_text("e-closure " + str(new_state), debug)
                    if new_state not in dfa_states:
                        cls.debug_text("in e-branch", debug)
                        dfa_states.append(new_state)
                        e_closures.append(new_state)
                        S.append(new_state)

                        dfa_states.remove(state)
                        for t in dfa_transitions:
                            if t[2] == state:
                                t[2] = new_state
                        state = new_state
                else:
                    new_state = cls.letter_closure(e_closures, state, state_letter_d)
                    cls.debug_text("l-closure " + str(new_state), debug)
                    if new_state not in dfa_states:
                        dfa_states.append(new_state)
                        S.append(new_state)

                    d_to_append = [state, letter, new_state]
                    if d_to_append not in dfa_transitions:
                        dfa_transitions.append(d_to_append)

        to_return = cls.assemble_dfa(nfa_name, dfa_states, dfa_transitions, sigma)

        return to_return

    @classmethod
    def debug_text(cls, string, debug):
        if debug:
            print(string)


"""******************************************* DFA TO minDFA *******************************************************"""


class Minimise(object):

    @classmethod
    def rename_fa_states(cls, fa):
        count = -1
        name_prefix = "Q"
        name_index = "\n\n State Name Index:\n"
        for s in fa.get_Q():
            new_name = name_prefix + str(count + 1)
            for t in fa.get_d():
                if t.get_start_name() == s.get_name():
                    t.get_start_state().name = new_name
                if t.get_end_name() == s.get_name():
                    t.get_end_state().name = new_name

            if s.get_name() == "{" + void + "}":
                name_index += "\n " + new_name + " : " + s.get_name()
            else:
                name_index += "\n " + new_name + " : " + "{" + s.get_name() + "}"

            s.name = new_name

            count += 1
            if count >= 10:
                name_prefix = "S"
                count = -1
            elif count >= 20:
                name_prefix = "R"
                count = -1
            elif count >= 30:
                name_prefix = "T"
                count = -1

        return fa, name_index

    @classmethod
    def assemble_fa(cls, fa, name, r_s, r_t):
        tp = fa.type()
        output_fa = None
        r_s = sorted(r_s)

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
                                 for i in t.get_end_states() if i.get_name() != void and i not in temp]

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
        if p == []:
            p = [[s for s in input_dfa.get_Q() if s not in input_dfa.get_F()]]
        else:
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
    def convert(cls, dfa):
        r_s_dfa = cls.remove_unreachable_states(dfa)
        partitions = cls.hopcroft_algorithm(r_s_dfa)

        num_partitions = [len(set) for set in partitions]

        if max(num_partitions) > 1:
            new_Q = []
            new_d = []
            new_state = None

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
                elif len(p_set) == 1:
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
            name = "Min(" + dfa.get_name() + ")"
            output_dfa = cls.assemble_fa(r_s_dfa, name, new_Q, new_d)

            print(output_dfa)
            return output_dfa

        else:
            print("No non-distinguishable states found")
            return r_s_dfa
