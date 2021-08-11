import numpy as np
from Preliminaries import *
from FA import *
from Algorithms import *
from UI import *


def run_tests():
    print("\n ----------------------------------- DFA EXAMPLE 1 ---------------------------------------\n")

    dfa1 = Dfa("M")
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

    print("\n --------------------------------- NFA TO DFA EXAMPLE 1 -----------------------------------\n")
    nfa1 = Nfa("N")
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

    Determinise().convert(nfa1)

    print("\n --------------------------------- NFA TO DFA EXAMPLE 2 -----------------------------------\n")

    nfa2 = Nfa("eNFA")

    nfa2.add_state("A")
    nfa2.add_state("B")
    nfa2.add_state("C", True)

    A2 = nfa2.Q[0]
    B2 = nfa2.Q[1]
    C2 = nfa2.Q[2]

    info3 = [(A2, "0", B2), (A2, "0", C2), (A2, "1", A2), (A2, epsilon, B2), (B2, "1", B2), (B2, epsilon, C2),
             (C2, "0", C2), (C2, "1", C2)]

    for i in range(len(info3)):
        nfa2.add_transition(*info3[i])

    print(nfa2)
    # nfa1.print_d()

    Determinise().convert(nfa2)

    print("\n --------------------------------- DFA TO minDFA EXAMPLE 1 -----------------------------------\n")

    dfa2 = Dfa("D")
    dfa2.add_state("1", False)
    dfa2.add_state("2", False)
    dfa2.add_state("3", True)
    dfa2.add_state("4", False)

    # dfa2.print_Q()

    a1 = dfa2.Q[0]
    b1 = dfa2.Q[1]
    c1 = dfa2.Q[2]
    d1 = dfa2.Q[3]

    info4 = [(a1, "a", b1), (a1, "b", a1), (b1, "a", b1), (b1, "b", c1), (c1, "a", c1), (c1, "b", c1), (d1, "a", c1),
             (d1, "b", d1)]

    for i in range(len(info4)):
        dfa2.add_transition(*info4[i])

    print(dfa2)

    Minimise().convert(dfa2)

    dfa3 = Dfa("F")
    dfa3.add_state("q0", False)
    dfa3.add_state("q1", True)
    dfa3.add_state("q2", True)
    dfa3.add_state("q3", False)
    dfa3.add_state("q4", True)
    dfa3.add_state("q5", False)

    # dfa3.print_Q()

    q0 = dfa3.Q[0]
    q1 = dfa3.Q[1]
    q2 = dfa3.Q[2]
    q3 = dfa3.Q[3]
    q4 = dfa3.Q[4]
    q5 = dfa3.Q[5]

    info5 = [(q0, "0", q3), (q0, "1", q1), (q1, "0", q2), (q1, "1", q5), (q2, "0", q2), (q2, "1", q5), (q3, "0", q0),
             (q3, "1", q4), (q4, "0", q2), (q4, "1", q5), (q5, "0", q5), (q5, "1", q5)]

    for i in range(len(info5)):
        dfa3.add_transition(*info5[i])

    print(dfa3)

    Minimise().convert(dfa3)


def main(test=False):
    if test:
        run_tests()
    app_startup(skip=False)


if __name__ == "__main__":
    main()
