import numpy as np
from Preliminaries import *


class Fa:
    def __init__(self, name):
        self.name = name
        self.Q = []
        self.d = []
        self.s = []
        self.F = []
        self.sigma = []
        self.table = []
        self.table_length = 0

    # accessors

    def get_Q(self):
        return self.Q.copy()

    def get_d(self):
        return self.d.copy()

    def get_s(self):
        return self.s.copy()

    def get_F(self):
        return self.F.copy()

    def get_sigma(self):
        return self.sigma.copy()

    def get_state_d(self, state):
        to_return = []
        for t in self.d:
            if t.get_start_name() == state.get_name():
                to_return.append(t)
        return to_return

    # mutators

    def set_sigma(self, new_letters):
        for i in range(len(new_letters)):
            if new_letters[i] not in self.sigma:
                self.sigma.append(str(new_letters[i]))

    def add_state(self, state_name, final=False):
        if self.Q == []:
            new_state = State(state_name, True, final)
            self.Q.append(new_state)
            self.s.append(new_state)
        else:
            exists = False
            new_state = State(state_name, False, final)
            for state in self.Q:
                if state == new_state:
                    exists = True

            if not exists:
                state_to_add = State(state_name, False, final)
                self.Q.append(state_to_add)
            else:
                print("state " + str(new_state) + " already exists in FA " + str(self.name))
                pass

        if final:
            self.F.append(new_state)

    # misc

    def print_Q(self):
        i = 1
        print("\n#|   Q   , s   ,  F")
        print("----------------------")
        for state in self.Q:
            print(str(i) + "|", str(state))
            print("----------------------")
            i += 1
        print("\n")

    def print_d(self):
        for i in self.d:
            print(i)


class Dfa(Fa):
    def __init__(self, name):
        super().__init__(name)

    # accessors

    def get_table(self):
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

        self.table = np.array(dfa_table, dtype=object)

        return self.table

    # mutators

    def add_transition(self, q1, letter, q2):
        letter_str = str(letter)

        if q1 in self.Q and q2 in self.Q:
            transition_to_add = DfaTransition(q1, letter_str, q2)
            self.d.append(transition_to_add)

            if letter_str not in self.sigma:
                self.sigma.append(letter_str)

    def remove_transition(self, q1, letter, q2):
        letter_str = str(letter)
        to_remove = DfaTransition(q1, letter_str, q2)

        if to_remove in self.d:
            self.d.remove(to_remove)

        else:
            print("transition not found")

    # misc

    @staticmethod
    def type():
        return "dfa"

    def find_table_size(self):
        name_size = max([len(x.get_end_name()) for x in self.d])
        if name_size > self.table_length:
            self.table_length = name_size
        return self.table_length

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

    def __str__(self):

        if self.is_valid():
            self.get_table()
            r = ""
            size = "{:^" + str(self.find_table_size() + 4) + "s}|"
            for line in self.table:
                k = size * len(self.table[0])
                r += k.format(*line) + "\n"
                r += "-" * len(k.format(*line)) + "\n"

            return ("\nTransition table for DFA " + self.name) + "\n\n" + r

        else:
            return "dfa is not valid"


class Nfa(Fa):
    def __init__(self, name):
        super().__init__(name)

    # accessors
    def get_table(self):

        lst = ["", "\u0394"]

        for l in self.sigma:
            lst.append(l)

        self.table = np.zeros((len(self.Q) + 1, len(lst)), dtype=object)
        self.table[0] = lst

        for row in range(1, len(self.table)):
            temp_lst = []
            j = row - 1
            if self.Q[j].is_start and not self.Q[j].is_final:
                self.table[row][0] = "s"
            elif self.Q[j].is_final and not self.Q[j].is_start:
                self.table[row][0] = "F"
            elif self.Q[j].is_start and self.Q[j].is_final:
                self.table[row][0] = "s,F"
            else:
                self.table[row][0] = ""

            self.table[row][1] = self.Q[j].get_name()

            for t in self.fill_d():
                if t.get_start_name() == self.table[row][1]:
                    temp_lst.append(t)

            for col in range(2, len(self.table[0])):
                for elem in temp_lst:
                    if elem.letter == self.table[0][col]:
                        self.table[row][col] = elem.get_end_name()

        return self.table

    # mutators

    def add_transition(self, q1, letter, q2):
        letter_str = str(letter)
        flag = False

        if q1 in self.Q and (q2 in self.Q or q2.get_name() == "{}"):
            transition_to_add = NfaTransition(q1, letter_str, [q2])
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

    # misc

    @staticmethod
    def type():
        return "nfa"

    def fill_d(self):
        for s in self.Q:
            remaining = self.get_sigma()
            s_d = self.get_state_d(s)
            if len(s_d) < len(self.sigma):
                for t in s_d:
                    if t.letter in self.sigma:
                        remaining.remove(t.letter)

                for letter in remaining:
                    self.add_transition(s, letter, State("{}"))
                    # print(DfaTransition(s, letter, State("{}")))
        return self.d

    def find_table_size(self):
        if self.get_d() != []:
            name_size = max([len(x.get_end_name()) for x in self.get_d()])
            if name_size > self.table_length:
                self.table_length = name_size
        else:
            self.table_length = 3
        return self.table_length

    def __str__(self):
        table = self.get_table()
        r = ""
        size = "{:^" + str(self.find_table_size() + 4) + "s}|"
        for line in table:
            k = size * len(table[0])
            r += k.format(*line) + "\n"
            r += "-" * len(k.format(*line)) + "\n"

        return ("\nTransition table for NFA " + self.name) + "\n\n" + r
