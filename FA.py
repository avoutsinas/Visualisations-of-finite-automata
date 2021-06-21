import numpy as np
from Preliminaries import state, transition


class dfa:
    def __init__(self, name="A", alphabet=[]):
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

    def add_state(self, state_name, final):
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

        if self.is_valid():

            lst = ["", "d"]

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

            return "\n" + r

        else:
            return "Dfa is not valid"
