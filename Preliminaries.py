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

    def get_start_name(self):
        return self.start_state.get_name()

    def get_end_name(self):
        return self.end_state.get_name()

    def get_start_state(self):
        return self.start_state

    def get_end_state(self):
        return self.end_state

    # misc

    def __eq__(self, other):
        if self.start_state == other.start_state and self.end_state == other.end_state and self.letter == other.letter:
            return True
        else:
            return False

    def __str__(self):
        to_return = self.start_state.get_name() + " -> " + self.letter + " -> " + self.end_state.get_name()
        return to_return


class NfaTransition:
    def __init__(self, start_state, letter, end_states):
        self.start_state = start_state
        self.end_states = end_states
        self.letter = str(letter)
        self.matrix = [self.start_state, self.letter, self.end_states]

    # accessors

    def get_start_state(self):
        return self.start_state

    def get_end_states(self):
        return self.end_states

    def get_start_name(self):
        return self.start_state.get_name()

    def get_end_name(self):
        temp = ""
        for i in range(len(self.end_states)):
            if i == 0:
                temp += self.end_states[i].get_name()
            else:
                temp += "," + self.end_states[i].get_name()

        return temp

    # mutators

    def add_end_state(self, state):
        self.end_states.append(state)

    # misc

    def __str__(self):
        to_return = self.start_state.get_name() + " -> " + self.letter + " -> " + str(
            [n.get_name() for n in self.end_states])
        return to_return
