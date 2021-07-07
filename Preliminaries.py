import numpy as np

epsilon = '\u03B5'


class State:
    def __init__(self, state_name, is_start=False, is_final=False):
        self.name = str(state_name)
        self.is_start = is_start
        self.is_final = is_final
        self.state = [self.name, self.is_start, self.is_final]

    # accessors

    def get_name(self):
        return self.name

    def __eq__(self, other):
        if self.name == other.name and self.is_start == other.is_start and self.is_final == other.is_final:
            return True
        else:
            return False

    # misc

    def __str__(self):

        to_return = self.state[0], self.state[1], self.state[2]

        return str(to_return)


class Transition:
    def __init__(self, start_state, letter, end_state):
        self.start_state = start_state
        self.end_state = end_state
        self.letter = str(letter)
        self.matrix = [self.start_state, self.letter, self.end_state]

        # accessors

    def get_start_state(self):
        return self.start_state

    def get_start_name(self):
        return self.start_state.get_name()

    def __eq__(self, other):
        if self.start_state == other.start_state and self.end_state == other.end_state and self.letter == other.letter:
            return True
        else:
            return False


class DfaTransition(Transition):
    def __init__(self, start_state, letter, end_state):
        super().__init__(start_state, letter, end_state)

    # accessors

    def get_end_state(self):
        return self.end_state

    def get_end_name(self):
        return self.end_state.get_name()

    # misc

    def __eq__(self, other):
        if self.start_state == other.start_state and self.end_state == other.end_state and self.letter == other.letter:
            return True
        else:
            return False

    def __str__(self):
        to_return = self.start_state.get_name() + " -> " + self.letter + " -> " + self.end_state.get_name()
        return to_return


class NfaTransition(Transition):
    def __init__(self, start_state, letter, end_state):
        super().__init__(start_state, letter, end_state)

    # accessors

    def get_end_states(self):
        return self.end_state

    def get_end_name(self):
        name_lst = []
        temp = ""
        for e_s in self.get_end_states():
            name_lst.append(e_s.name)

        name_lst = sorted(name_lst)

        for i in range(len(name_lst)):
            if i == 0:
                temp += name_lst[i]
            else:
                temp += "," + name_lst[i]

        return temp

    # mutators

    def add_end_state(self, state):
        self.end_state.append(state)

    # misc

    def __eq__(self, other):
        if self.start_state == other.start_state and self.end_state == other.end_state and self.letter == other.letter:
            return True
        else:
            return False

    def __str__(self):
        to_return = self.start_state.get_name() + " -> " + self.letter + " -> " + str(
            sorted([n.get_name() for n in self.end_state]))
        return to_return
