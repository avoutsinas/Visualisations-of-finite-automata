import numpy as np


class state:
    def __init__(self, state_name, is_start=False, is_final=False):
        self.is_start = is_start
        self.is_final = is_final
        self.state = [str(state_name), self.is_start, self.is_final]

    def get_name(self):
        return self.state[0]

    def __eq__(self, other):
        if self.state[0] == other.state[0] and self.state[1] == other.state[1] and self.state[2] == other.state[2]:
            return True
        else:
            return False

    def __str__(self):

        to_return = self.state[0], self.state[1], self.state[2]

        return str(to_return)


class transition:
    def __init__(self, start_state, letter, end_state):
        self.start_state = start_state
        self.end_state = end_state
        self.letter = str(letter)
        self.matrix = [self.start_state, self.letter, self.end_state]

    def get_start_name(self):
        return self.start_state.get_name()

    def get_end_name(self):
        return self.end_state.get_name()

    def __str__(self):
        to_return = self.start_state.get_name() + " -> " + self.letter + " -> " + self.end_state.get_name()
        return to_return
