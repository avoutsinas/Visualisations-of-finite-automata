import numpy as np
from Preliminaries import *

empty_end_state = State(state_name=void)
garbage_state = State(state_name="{"+void+"}")


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

    def get_name(self):
        name = self.name
        return name

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

    def get_table(self):
        if self.type() == "dfa":
            lst = ["", delta]
        elif self.type() == "nfa":
            lst = ["", Delta]
        else:
            raise ValueError("ERROR: FA has not type!")

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
        return "Not Implemented"

    def set_sigma(self, new_letters):
        for i in range(len(new_letters)):
            if new_letters[i] not in self.sigma:
                self.sigma.append(str(new_letters[i]))

    def add_state(self, state_name, final=False):
        added = False
        if self.Q == []:
            new_state = State(state_name, True, final)
            self.Q.append(new_state)
            self.s.append(new_state)
            added = True
        else:
            new_state = State(state_name, False, final)
            existing = [s.get_name() for s in self.Q]
            if state_name not in existing:
                self.Q.append(new_state)
                added = True
            else:
                print("A state with the name [" + str(state_name) + "] already exists in FA " + str(self.name))
                pass

        if added and final:
            self.F.append(new_state)

    def clear(self):
        self.Q = []
        self.d = []
        self.s = []
        self.F = []
        self.sigma = []
        self.table = []
        self.table_length = 0

    # misc
    @staticmethod
    def type():
        return "Not Implemented"

    def fill_d(self):
        for s in self.Q:
            remaining = self.get_sigma()
            s_d = self.get_state_d(s)
            if len(s_d) < len(self.sigma):
                for t in s_d:
                    if t.letter in self.sigma:
                        remaining.remove(t.letter)

                for letter in remaining:
                    self.add_transition(s, letter, empty_end_state)
                    #print(DfaTransition(s, letter, empty_end_state))
        return self.d

    def find_table_size(self):
        if self.get_d() != []:
            name_size = max([len(x.get_end_name()) for x in self.get_d()])
            if name_size > self.table_length:
                self.table_length = name_size
        else:
            self.table_length = 3
        return self.table_length

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

    # mutators

    def add_transition(self, q1, letter, q2):
        letter_str = str(letter)

        if q1 in self.Q and (q2 in self.Q or q2 == empty_end_state):
            transition_to_add = DfaTransition(q1, letter_str, q2)
            self.d.append(transition_to_add)

            if letter_str not in self.sigma:
                self.sigma.append(letter_str)

    # misc

    @staticmethod
    def type():
        return "dfa"

    def is_valid(self):
        valid = True
        end_states = [i.get_end_state() for i in self.d]

        if self.Q == [] or self.d == [] or empty_end_state in end_states or epsilon in self.sigma:
            valid = False
            return valid
        else:
            for s in self.Q:
                transition_letters = []
                for t in self.d:
                    if t.get_start_state() == s:
                        transition_letters.append(t.letter)

                if sorted(transition_letters) != sorted(self.sigma):
                    valid = False
                    return valid

        return valid

    def __str__(self):

        table = self.get_table()
        r = ""
        k = 0
        size = "{:^" + str(self.find_table_size() + 4) + "s}|"
        for line in table:
            try:
                k = size * len(table[0])
                r += k.format(*line) + "\n"
                r += "-" * len(k.format(*line)) + "\n"
            except ValueError:
                pass

        if self.is_valid():
            return ("\n DFA " + self.name) + "\n\n" + r
        else:
            error = "\n" + " " * 5 + "This DFA is not valid!"
            return ("\n DFA " + self.name) + "\n\n" + r + error


class Nfa(Fa):
    def __init__(self, name):
        super().__init__(name)

    # mutators

    def add_transition(self, q1, letter, q2):
        letter_str = str(letter)
        flag = False

        if q1 in self.Q and (q2 in self.Q or q2.get_name() == void):
            transition_to_add = NfaTransition(q1, letter_str, [q2])
            if self.d != []:
                for t in self.d:
                    if t.get_start_name() == q1.get_name() and t.letter == letter_str and \
                            t.get_end_name() != q2.get_name() and flag == False:

                        if void in t.get_end_name():
                            flag = True
                            t.change_end_state(q2)
                        else:
                            flag = True
                            t.add_end_state(q2)

            if flag == False:
                self.d.append(transition_to_add)

            if letter_str not in self.sigma:
                self.sigma.append(letter_str)

    # misc
    @staticmethod
    def is_valid():
        return False

    @staticmethod
    def type():
        return "nfa"

    def __str__(self):
        table = self.get_table()
        r = ""
        size = "{:^" + str(self.find_table_size() + 4) + "s}|"
        for line in table:
            k = size * len(table[0])
            r += k.format(*line) + "\n"
            r += "-" * len(k.format(*line)) + "\n"

        return ("\n NFA " + self.name) + "\n\n" + r
