import numpy as np
from Preliminaries import *


class dfa:
    def __init__(self, name="M", sigma=[]):
        self.name = name
        self.Q = []
        self.d = []
        self.s = []
        self.F = []
        self.sigma = sigma

    def set_sigma(self, new_letters):
        for i in range(len(new_letters)):
            if new_letters[i] not in self.sigma:
                self.sigma.append(str(new_letters[i]))

    def add_state(self, state_name, final=False):
        if self.Q == []:
            state_to_add = state(state_name, True, final)
            self.Q.append(state_to_add)
            self.s.append(state_to_add)
        else:
            exists = False
            for s in self.Q:
                if s.get_name() == str(state_name):
                    exists = True

            if exists == False:
                state_to_add = state(state_name, False, final)
                self.Q.append(state_to_add)
            else:
                # raise ValueError ("The state already exists in the dFA")
                pass

        if final == True:
            self.F.append(self.Q[-1])

    def add_transition(self, q1, letter, q2):

        letter_str = str(letter)

        if q1 in self.Q and q2 in self.Q:
            transition_to_add = transition(q1, letter_str, q2)
            self.d.append(transition_to_add)

            if letter_str not in self.sigma:
                self.sigma.append(letter_str)

    def remove_transition(self, q1, letter, q2):
        letter_str = str(letter)
        to_remove = transition(q1, letter_str, q2)

        if to_remove in self.d:
            self.d.remove(to_remove)

        else:
            print("transition not found")

    def is_valid(self):
        valid = True

        if self.s == [] or self.F == []:
            valid = False
            return valid

        for s in self.Q:
            transition_letters = []
            for t in self.d:
                if t.get_start_name() == s.get_name():
                    transition_letters.append(t.letter)

            if sorted(transition_letters) != sorted(self.sigma):
                valid = False
                return valid

        return valid

    def print_Q(self):
        i = 1
        print("\n#|   Q   , s   ,  F")
        print("----------------------")
        for state in self.Q:
            print(str(i) + "|", str(state))
            print("----------------------")
            i += 1
        print("\n")

    def __str__(self):

        if self.is_valid() or not self.is_valid():

            lst = ["", "\u03B4"]

            for i in self.sigma:
                lst.append(i)
            dfa_table = [lst]

            for s in self.Q:
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
                for l in self.sigma:
                    for t in self.d:
                        if t.letter == l and s.get_name() == t.get_start_name():
                            temp.append(t.get_end_name())
                dfa_table.append(temp)

            dfa_table = np.array(dfa_table)
            r = ""
            for line in dfa_table:
                k = "{:^11s}|" * len(lst)
                r += k.format(*line) + "\n"
                r += "-" * len(k.format(*line)) + "\n"

            return ("\nTransition table for dFA " + self.name) + "\n\n" + r

        else:
            return "dfa is not valid"


class nfa:
    def __init__(self, name="N", sigma=[]):
        self.name = name
        self.Q = []
        self.d = []
        self.s = []
        self.F = []
        self.sigma = sigma
        self.matrix = []

    def set_sigma(self, new_letters):
        for i in range(new_letters):
            if new_letters[i] not in self.sigma:
                self.sigma.append(str(new_letters[i]))

    def add_state(self, state_name, final=False):
        if self.Q == []:
            state_to_add = state(state_name, True, final)
            self.Q.append(state_to_add)
            self.s.append(state_to_add)
        else:
            exists = False
            for s in self.Q:
                if s.get_name() == str(state_name):
                    exists = True

            if exists == False:
                state_to_add = state(state_name, False, final)
                self.Q.append(state_to_add)
            else:
                raise ValueError("The state already exists in the dFA")

        if final == True:
            self.F.append(self.Q[-1])

    def add_transition(self, q1, letter, q2):
        letter_str = str(letter)
        flag = False

        if q1 in self.Q and (q2 in self.Q or q2.get_name() == "{}"):
            transition_to_add = nfa_transition(q1, letter_str, [q2])
            if self.d != []:
                for t in self.d:
                    if t.get_start_name() == q1.get_name() and t.letter == letter_str and \
                            t.get_end_name() != q2.get_name() and flag == False:

                        if "{}" in t.get_end_name():
                            flag = True
                            t.change_end_state(q2)
                        else:
                            flag = True
                            t.add_end_state(q2)

            if flag == False:
                self.d.append(transition_to_add)

            if letter_str not in self.sigma:
                self.sigma.append(letter_str)

    def remove_transition(self, q1, letter, q2):
        letter_str = str(letter)
        for t in self.d:
            if t.get_start_name() == q1.get_name() and t.letter == letter_str and t.get_end_name() == q2.get_name():
                self.d.remove(t)
                break

        else:
            print("transition not found")

    def get_d(self):
        for s in self.Q:
            remaining = self.sigma.copy()
            d = self.get_state_d(s)
            if len(d) < len(self.sigma):
                for t in d:
                    if t.letter in self.sigma:
                        remaining.remove(t.letter)

                for letter in remaining:
                    self.add_transition(s, letter, state("{}"))
                    # print(transition(s, letter, state("{}")))
        return self.d

    def get_state_d(self, state):
        to_return = []
        for t in self.d:
            if t.get_start_name() == state.get_name():
                to_return.append(t)

        return to_return

    def get_table(self):

        lst = ["", "\u0394"]

        for l in self.sigma:
            lst.append(l)

        self.matrix = np.zeros((len(self.Q) + 1, len(lst)), dtype=object)
        self.matrix[0] = lst

        for row in range(1, len(self.matrix)):
            temp_lst = []
            j = row - 1
            if self.Q[j].is_start and not self.Q[j].is_final:
                self.matrix[row][0] = "s"
            elif self.Q[j].is_final and not self.Q[j].is_start:
                self.matrix[row][0] = "F"
            elif self.Q[j].is_start and self.Q[j].is_final:
                self.matrix[row][0] = "s,F"
            else:
                self.matrix[row][0] = ""

            self.matrix[row][1] = self.Q[j].get_name()

            for t in self.get_d():
                if t.get_start_name() == self.matrix[row][1]:
                    temp_lst.append(t)

            for col in range(2, len(self.matrix[0])):
                for elem in temp_lst:
                    if elem.letter == self.matrix[0][col]:
                        self.matrix[row][col] = elem.get_end_name()

        return self.matrix

    def print_d(self):
        for i in self.get_d():
            print(i)

    def print_Q(self):
        i = 1
        print("\n#|   Q   , s   ,  F")
        print("----------------------")
        for state in self.Q:
            print(str(i) + "|", str(state))
            print("----------------------")
            i += 1
        print("\n")

    def __str__(self):

        table = self.get_table()

        r = ""
        for line in table:
            k = "{:^11s}|" * len(table[0])
            r += k.format(*line) + "\n"
            r += "-" * len(k.format(*line)) + "\n"

        return ("\nTransition table for NFA " + self.name) + "\n\n" + r
