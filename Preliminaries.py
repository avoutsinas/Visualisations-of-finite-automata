import numpy as np

epsilon = '\u03B5'


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


class nfa_transition:
    def __init__(self, start_state, letter, end_states):
        self.start_state = start_state
        self.end_states = end_states
        self.letter = str(letter)
        self.matrix = [self.start_state, self.letter, self.end_states]

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

    def add_end_state(self, state):
        self.end_states.append(state)

    def is_start_final(self):
        to_return = False

        if self.start_state.is_final == True:
            to_return = True

        return to_return

    def is_end_final(self):
        to_return = False
        for state in self.end_states:
            if state.is_final == True:
                to_return = True

        return to_return

    def __str__(self):
        to_return = self.start_state.get_name() + " -> " + self.letter + " -> " + str(
            [n.get_name() for n in self.end_states])
        return to_return
