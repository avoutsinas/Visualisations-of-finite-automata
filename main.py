import numpy as np
from Preliminaries import state, transition
from FA import dfa


def main():
    dfa1 = dfa()
    dfa1.add_state("1", False)
    dfa1.add_state("2", False)
    dfa1.add_state("3", True)

    # dfa1.print_states()

    a = dfa1.states[0]
    b = dfa1.states[1]
    c = dfa1.states[2]

    info = [(a, "a", b), (a, "b", a), (b, "a", b), (b, "b", c), (c, "a", c), (c, "b", c)]
    for i in range(len(info)):
        dfa1.add_transition(*info[i])

    print(dfa1)
    # print("Is the DFA " + dfa1.name + " valid? : " + str(dfa1.is_valid()))


if __name__ == "__main__":
    main()
