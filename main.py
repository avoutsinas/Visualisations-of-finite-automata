import numpy as np
from Preliminaries import *
from FA import dfa, nfa


def main():
    dfa1 = dfa()
    dfa1.add_state("1", False)
    dfa1.add_state("2", False)
    dfa1.add_state("3", True)

    dfa1.print_states()

    a = dfa1.states[0]
    b = dfa1.states[1]
    c = dfa1.states[2]

    info = [(a, "a", b), (a, "b", a), (b, "a", b), (b, "b", c), (c, "a", c), (c, "b", c)]
    for i in range(len(info)):
        dfa1.add_transition(*info[i])

    print(dfa1)
    # print("Is the DFA " + dfa1.name + " valid? : " + str(dfa1.is_valid()))

    nfa1 = nfa()
    nfa1.add_state("A")
    nfa1.add_state("B")
    nfa1.add_state("C")
    nfa1.add_state("D", True)

    A = nfa1.states[0]
    B = nfa1.states[1]
    C = nfa1.states[2]
    D = nfa1.states[3]

    info2 = [(A, "0", A), (A, "0", B), (A, "1", A), (B, "0", C), (B, "1", C), (C, "0", D), (C, "1", D)]

    for i in range(len(info2)):
        nfa1.add_transition(*info2[i])

    nfa1.print_transitions()


if __name__ == "__main__":
    main()
