import numpy as np
from Preliminaries import *
from FA import *
from Algorithms import *


def main():
    dfa1 = dfa()
    dfa1.add_state("1", False)
    dfa1.add_state("2", False)
    dfa1.add_state("3", True)

    # dfa1.print_Q()

    a = dfa1.Q[0]
    b = dfa1.Q[1]
    c = dfa1.Q[2]

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

    A = nfa1.Q[0]
    B = nfa1.Q[1]
    C = nfa1.Q[2]
    D = nfa1.Q[3]

    info2 = [(A, "0", A), (A, "0", B), (A, "1", A), (B, "0", C), (B, "1", C), (C, "0", D), (C, "1", D)]

    for i in range(len(info2)):
        nfa1.add_transition(*info2[i])

    print(nfa1)
    # nfa1.print_d()

    info3 = (D, "1", D)
    nfa1.add_transition(*info3)

    print(nfa1)
    # nfa1.print_d()

    nfa1.remove_transition(*info3)
    print(nfa1)
    # nfa1.print_d()

    print("\n ----------------------------------------------------------------------\n")
    dfa_conversion(nfa1)

    nfa2 = nfa("eNFA")

    nfa2.add_state("A")
    nfa2.add_state("B")
    nfa2.add_state("C", True)

    A2 = nfa2.Q[0]
    B2 = nfa2.Q[1]
    C2 = nfa2.Q[2]

    info3 = [(A2, "0", B2), (A2, "0", C2), (A2, "1", A2), (A2, epsilon, B2),(B2, "1", B2),(B2, epsilon, C2),(C2, "0", C2), (C2, "1", C2) ]

    for i in range(len(info3)):
        nfa2.add_transition(*info3[i])

    print(nfa2)
    # nfa1.print_d()

    dfa_conversion(nfa2)


if __name__ == "__main__":
    main()
