import numpy as np
from Preliminaries import *


class dfa:
    def __init__(self, name="M", alphabet=[]):
        self.name = name
        self.states = []
        self.transitions = []
        self.start_state = []
        self.final_states = []
        self.alphabet = alphabet

    def set_alphabet(self, new_letters):
        for i in range(new_letters):
            if new_letters[i] not in self.alphabet:
                self.alphabet.append(str(new_letters[i]))

    def add_state(self, state_name, final=False):
        if self.states == []:
            state_to_add = state(state_name, True, final)
            self.states.append(state_to_add)
            self.start_state.append(state_to_add)
        else:
            exists = False
            for s in self.states:
                if s.get_name() == str(state_name):
                    exists = True

            if exists == False:
                state_to_add = state(state_name, False, final)
                self.states.append(state_to_add)
            else:
                # raise ValueError ("The state already exists in the DFA")
                pass

        if final == True:
            self.final_states.append(self.states[-1])

    def add_transition(self, state1, letter, state2):

        letter_str = str(letter)

        if state1 in self.states and state2 in self.states:
            transition_to_add = transition(state1, letter_str, state2)
            self.transitions.append(transition_to_add)

            if letter_str not in self.alphabet:
                self.alphabet.append(letter_str)

    def is_valid(self):
        valid = True

        if self.start_state == [] or self.final_states == []:
            valid = False
            return valid

        for s in self.states:
            transition_letters = []
            for t in self.transitions:
                if t.get_start_name() == s.get_name():
                    transition_letters.append(t.letter)

            if sorted(transition_letters) != sorted(self.alphabet):
                valid = False
                return valid

        return valid

    def print_states(self):
        i = 1
        print("\n#|   Q   , s   ,  F")
        print("----------------------")
        for state in self.states:
            print(str(i) + "|", str(state))
            print("----------------------")
            i += 1
        print("\n")

    def __str__(self):

        if self.is_valid() or not self.is_valid():

            lst = ["", "\u03B4"]

            for i in self.alphabet:
                lst.append(i)
            dfa_table = [lst]

            for s in self.states:
                temp = []
                if s.is_start and not s.is_final:
                    slot1 = "s"
                elif s.is_final and not s.is_start:
                    slot1 = "F"
                elif s.is_start and s.is_final:
                    slot1 = "s,F"
                else:
                    slot1 = ""

                slot2 = s.get_name()

                temp = [slot1, slot2]
                for l in self.alphabet:
                    for t in self.transitions:
                        if t.letter == l and s.get_name() == t.get_start_name():
                            temp.append(t.get_end_name())
                dfa_table.append(temp)

            dfa_table = np.array(dfa_table)
            r = ""
            for line in dfa_table:
                k = "{:^7s}|" * len(lst)
                r += k.format(*line) + "\n"
                r += "-" * len(k.format(*line)) + "\n"

            return ("\nTransition table for DFA " + self.name) + "\n\n" + r

        else:
            return "Dfa is not valid"


class nfa:
    def __init__(self, name="N", alphabet=[]):
        self.name = name
        self.states = []
        self.transitions = []
        self.start_state = []
        self.final_states = []
        self.alphabet = alphabet

    def set_alphabet(self, new_letters):
        for i in range(new_letters):
            if new_letters[i] not in self.alphabet:
                self.alphabet.append(str(new_letters[i]))

    def add_state(self, state_name, final=False):
        if self.states == []:
            state_to_add = state(state_name, True, final)
            self.states.append(state_to_add)
            self.start_state.append(state_to_add)
        else:
            exists = False
            for s in self.states:
                if s.get_name() == str(state_name):
                    exists = True

            if exists == False:
                state_to_add = state(state_name, False, final)
                self.states.append(state_to_add)
            else:
                raise ValueError("The state already exists in the DFA")

        if final == True:
            self.final_states.append(self.states[-1])

    def add_transition(self, state1, letter, state2):
        letter_str = str(letter)
        flag = False

        if state1 in self.states and (state2 in self.states or state2.get_name() == "{}"):
            transition_to_add = nfa_transition(state1, letter_str, [state2])
            if self.transitions != []:
                for t in self.transitions:
                    if t.get_start_name() == state1.get_name() and t.letter == letter_str and t.get_end_name() != state2.get_name() and flag == False:
                        flag = True
                        t.add_end_state(state2)
            if flag == False:
                self.transitions.append(transition_to_add)

            if letter_str not in self.alphabet:
                self.alphabet.append(letter_str)

    def get_transitions(self):
        for s in self.states:
            remaining = self.alphabet
            transitions = self.get_state_transitions(s)
            if len(transitions) < len(self.alphabet):
                for t in transitions:
                    if t.letter in self.alphabet:
                        remaining.remove(t.letter)

                for letter in remaining:
                    self.add_transition(s, letter, state("{}"))
                    print(transition(s, letter, state("{}")))
        return self.transitions

    def get_state_transitions(self, state):
        to_return = []
        for t in self.transitions:
            if t.get_start_name() == state.get_name():
                to_return.append(t)

        return to_return

    def get_table(self):

        lst = ["", "\u0394"]

        for l in self.alphabet:
            lst.append(l)

        matrix = np.zeros((len(self.states) + 1, len(lst)), dtype=object)
        matrix[0] = lst

        for row in range(1, len(matrix)):
            temp_lst = []
            j = row - 1
            if self.states[j].is_start and not self.states[j].is_final:
                matrix[row][0] = "s"
            elif self.states[j].is_final and not self.states[j].is_start:
                matrix[row][0] = "F"
            elif self.states[j].is_start and self.states[j].is_final:
                matrix[row][0] = "s,F"
            else:
                matrix[row][0] = ""

            matrix[row][1] = self.states[j].get_name()

            for t in self.get_transitions():
                if t.get_start_name() == matrix[row][1]:
                    temp_lst.append(t)

            for col in range(2, len(matrix[0])):
                for elem in temp_lst:
                    if elem.letter == matrix[0][col]:
                        matrix[row][col] = elem.get_end_name()

        # matrix[matrix == 0] = "{}"
        return matrix

    def print_transitions(self):
        for i in self.get_transitions():
            print(i)

    def print_states(self):
        i = 1
        print("\n#|   Q   , s   ,  F")
        print("----------------------")
        for state in self.states:
            print(str(i) + "|", str(state))
            print("----------------------")
            i += 1
        print("\n")

    def __str__(self):

        table = self.get_table()

        r = ""
        for line in table:
            k = "{:^7s}|" * len(table[0])
            r += k.format(*line) + "\n"
            r += "-" * len(k.format(*line)) + "\n"

        return ("\nTransition table for NFA " + self.name) + "\n\n" + r
