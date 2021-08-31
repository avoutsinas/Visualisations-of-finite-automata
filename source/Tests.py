import numpy as np
from Preliminaries import *
from FA import *
from Algorithms import *


def run_tests():
    fa_test1()

    nfa_to_dfa_test1()
    nfa_to_dfa_test2()
    nfa_to_dfa_test3()
    nfa_to_dfa_test4()
    nfa_to_dfa_test5()
    nfa_to_dfa_test6()
    nfa_to_dfa_test7()

    dfa_min_test1()
    dfa_min_test2()
    dfa_min_test3()
    dfa_min_test4()
    dfa_min_test5()
    dfa_min_test6()

    nfa_to_min_dfa_test()


def fa_test1():
    print("\n\n ----------------------------------- DFA EXAMPLE 1 ---------------------------------------\n")

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
    print("Is the DFA " + dfa1.name + " valid? : " + str(dfa1.is_valid()))


def nfa_to_dfa_test1():
    print("\n\n --------------------------------- NFA TO DFA Test 1 -----------------------------------\n")
    nfa = Nfa("M")
    nfa.add_state("A")
    nfa.add_state("B")
    nfa.add_state("C")
    nfa.add_state("D", True)

    A = nfa.Q[0]
    B = nfa.Q[1]
    C = nfa.Q[2]
    D = nfa.Q[3]

    info = [(A, "0", A), (A, "0", B), (A, "1", A), (B, "0", C), (B, "1", C), (C, "0", D), (C, "1", D)]

    for i in range(len(info)):
        nfa.add_transition(*info[i])

    print(nfa)

    output = Determinise().convert(nfa)
    print(output)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def nfa_to_dfa_test2():
    print("\n\n --------------------------------- NFA TO DFA Test 2 -----------------------------------\n")

    nfa = Nfa("N")

    nfa.add_state("A")
    nfa.add_state("B")
    nfa.add_state("C", True)

    A = nfa.Q[0]
    B = nfa.Q[1]
    C = nfa.Q[2]

    info = [(A, "0", B), (A, "0", C), (A, "1", A), (A, epsilon, B), (B, "1", B), (B, epsilon, C),
            (C, "0", C), (C, "1", C)]

    for i in range(len(info)):
        nfa.add_transition(*info[i])

    print(nfa)

    output = Determinise().convert(nfa)
    print(output)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def nfa_to_dfa_test3():
    print("\n\n --------------------------------- NFA TO DFA Test 3 -----------------------------------\n")

    nfa = Nfa("O")

    nfa.add_state("1", True)
    nfa.add_state("2")
    nfa.add_state("3")

    A = nfa.Q[0]
    B = nfa.Q[1]
    C = nfa.Q[2]

    info = [(A, epsilon, C), (B, "a", B), (A, "b", B), (B, "a", C), (B, "b", C), (C, "a", A)]

    for i in range(len(info)):
        nfa.add_transition(*info[i])

    print(nfa)

    output = Determinise().convert(nfa)
    print(output)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def nfa_to_dfa_test4():
    print("\n\n --------------------------------- NFA TO DFA Test 4 -----------------------------------\n")

    nfa = Nfa("P")

    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.add_state("q2", True)

    A = nfa.Q[0]
    B = nfa.Q[1]
    C = nfa.Q[2]

    info = [(A, "0", A), (A, "1", B), (B, "0", B), (B, "1", B), (B, "0", C), (C, "0", C), (C, "1", C), (C, "1", B)]

    for i in range(len(info)):
        nfa.add_transition(*info[i])

    print(nfa)

    output = Determinise().convert(nfa)
    print(output)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def nfa_to_dfa_test5():
    print("\n\n --------------------------------- NFA TO DFA Test 5 -----------------------------------\n")

    nfa = Nfa("Q")

    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.add_state("q2")
    nfa.add_state("q3")
    nfa.add_state("q4", True)

    A = nfa.Q[0]
    B = nfa.Q[1]
    C = nfa.Q[2]
    D = nfa.Q[3]
    E = nfa.Q[4]

    info = [(A, epsilon, B), (A, epsilon, C), (B, "0", D), (C, "1", D), (D, "1", E)]

    for i in range(len(info)):
        nfa.add_transition(*info[i])

    print(nfa)

    output = Determinise().convert(nfa)
    print(output)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def nfa_to_dfa_test6():
    print("\n\n --------------------------------- NFA TO DFA Test 6 -----------------------------------\n")

    nfa = Nfa("R")

    nfa.add_state("q0")
    nfa.add_state("q1", True)

    A = nfa.Q[0]
    B = nfa.Q[1]

    info = [(A, "0", A), (A, "0", B), (A, "1", B), (B, "1", B), (B, "1", A)]

    for i in range(len(info)):
        nfa.add_transition(*info[i])

    print(nfa)

    output = Determinise().convert(nfa)
    print(output)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def nfa_to_dfa_test7():
    print("\n\n --------------------------------- NFA TO DFA Test 7 -----------------------------------\n")

    nfa = Nfa("S")

    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.add_state("q2", True)

    A = nfa.Q[0]
    B = nfa.Q[1]
    C = nfa.Q[2]

    info = [(A, epsilon, B), (A, "0", A), (B, "1", B), (B, epsilon, C), (C, "2", C)]

    for i in range(len(info)):
        nfa.add_transition(*info[i])

    print(nfa)

    output = Determinise().convert(nfa)
    print(output)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def dfa_min_test1():
    print("\n\n --------------------------------- DFA TO minDFA Test 1 -----------------------------------\n")

    dfa = Dfa("D")
    dfa.add_state("1", False)
    dfa.add_state("2", False)
    dfa.add_state("3", True)
    dfa.add_state("4", False)

    # dfa2.print_Q()

    a1 = dfa.Q[0]
    b1 = dfa.Q[1]
    c1 = dfa.Q[2]
    d1 = dfa.Q[3]

    info = [(a1, "a", b1), (a1, "b", a1), (b1, "a", b1), (b1, "b", c1), (c1, "a", c1), (c1, "b", c1), (d1, "a", c1),
            (d1, "b", d1)]

    for i in range(len(info)):
        dfa.add_transition(*info[i])

    print(dfa)

    output = Minimise().convert(dfa)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def dfa_min_test2():
    print("\n\n --------------------------------- DFA TO minDFA Test 2 -----------------------------------\n")

    dfa = Dfa("e")
    dfa.add_state("q0", False)
    dfa.add_state("q1", True)
    dfa.add_state("q2", True)
    dfa.add_state("q3", False)
    dfa.add_state("q4", True)
    dfa.add_state("q5", False)

    # dfa3.print_Q()

    q0 = dfa.Q[0]
    q1 = dfa.Q[1]
    q2 = dfa.Q[2]
    q3 = dfa.Q[3]
    q4 = dfa.Q[4]
    q5 = dfa.Q[5]

    info = [(q0, "0", q3), (q0, "1", q1), (q1, "0", q2), (q1, "1", q5), (q2, "0", q2), (q2, "1", q5), (q3, "0", q0),
            (q3, "1", q4), (q4, "0", q2), (q4, "1", q5), (q5, "0", q5), (q5, "1", q5)]

    for i in range(len(info)):
        dfa.add_transition(*info[i])

    print(dfa)

    output = Minimise().convert(dfa)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def dfa_min_test3():
    print("\n\n --------------------------------- DFA TO minDFA Test 3 -----------------------------------\n")

    dfa = Dfa("E")
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.add_state("q2")
    dfa.add_state("q3")
    dfa.add_state("q4", True)

    q0 = dfa.Q[0]
    q1 = dfa.Q[1]
    q2 = dfa.Q[2]
    q3 = dfa.Q[3]
    q4 = dfa.Q[4]

    info = [(q0, "a", q1), (q0, "b", q2), (q1, "a", q1), (q1, "b", q3), (q2, "a", q1), (q2, "b", q2), (q3, "a", q1),
            (q3, "b", q4), (q4, "a", q1), (q4, "b", q2)]

    for i in range(len(info)):
        dfa.add_transition(*info[i])

    print(dfa)

    output = Minimise().convert(dfa)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def dfa_min_test4():
    print("\n\n --------------------------------- DFA TO minDFA Test 4 -----------------------------------\n")

    dfa = Dfa("F")
    dfa.add_state("q0")
    dfa.add_state("q1", True)
    dfa.add_state("q2", True)
    dfa.add_state("q3")

    q0 = dfa.Q[0]
    q1 = dfa.Q[1]
    q2 = dfa.Q[2]
    q3 = dfa.Q[3]

    info5 = [(q0, "a", q1), (q0, "b", q0), (q1, "a", q2), (q1, "b", q1), (q2, "a", q1),
             (q2, "b", q2), (q3, "a", q1), (q3, "b", q2)]

    for i in range(len(info5)):
        dfa.add_transition(*info5[i])

    print(dfa)

    output = Minimise().convert(dfa)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def dfa_min_test5():
    print("\n\n --------------------------------- DFA TO minDFA Test 5 -----------------------------------\n")

    dfa = Dfa("G")
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.add_state("q2")
    dfa.add_state("q3")
    dfa.add_state("q4", True)

    q0 = dfa.Q[0]
    q1 = dfa.Q[1]
    q2 = dfa.Q[2]
    q3 = dfa.Q[3]
    q4 = dfa.Q[4]

    info5 = [(q0, "0", q1), (q0, "1", q3), (q1, "0", q2), (q1, "1", q4), (q2, "0", q1), (q2, "1", q4), (q3, "0", q2),
             (q3, "1", q4), (q4, "0", q4), (q4, "1", q4)]

    for i in range(len(info5)):
        dfa.add_transition(*info5[i])

    print(dfa)

    output = Minimise().convert(dfa)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def dfa_min_test6():
    print("\n\n --------------------------------- DFA TO minDFA Test 6 -----------------------------------\n")

    dfa = Dfa("H")
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.add_state("q2")
    dfa.add_state("q3", True)
    dfa.add_state("q4", True)
    dfa.add_state("q5")

    q0 = dfa.Q[0]
    q1 = dfa.Q[1]
    q2 = dfa.Q[2]
    q3 = dfa.Q[3]
    q4 = dfa.Q[4]
    q5 = dfa.Q[5]

    info = [(q0, "0", q1), (q0, "1", q2), (q1, "0", q2), (q1, "1", q3), (q2, "0", q2), (q2, "1", q4), (q3, "0", q3),
            (q3, "1", q3), (q4, "0", q4), (q4, "1", q4), (q5, "0", q5), (q5, "1", q4)]

    for i in range(len(info)):
        dfa.add_transition(*info[i])

    print(dfa)

    output = Minimise().convert(dfa)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))


def nfa_to_min_dfa_test():
    print("\n\n --------------------------------- NFA TO minDFA Test -----------------------------------\n")
    nfa = Nfa("K")
    nfa.add_state("1")
    nfa.add_state("2")
    nfa.add_state("3")
    nfa.add_state("p", True)
    nfa.add_state("q")

    q1 = nfa.Q[0]
    q2 = nfa.Q[1]
    q3 = nfa.Q[2]
    p = nfa.Q[3]
    q = nfa.Q[4]

    info = [(q1, "a", q2), (q1, "b", q3), (q2, "a", q2), (q2, "b", q3), (q2, epsilon, p), (q3, "a", q1), (q3, "b", q3),
            (p, "a", q), (p, "b", p), (q, "a", p), (q, "b", q)]

    for i in range(len(info)):
        nfa.add_transition(*info[i])

    print(nfa)

    output = Determinise().convert(nfa)
    print(output)
    print("Is the DFA " + output.get_name() + " valid? : " + str(output.is_valid()))

    renamed_fa, renamed_states = Minimise().rename_fa_states(output)
    print(renamed_fa)
    mindfa = Minimise().convert(renamed_fa)
    print(renamed_states)
    print("\nIs the DFA " + mindfa.get_name() + " valid? : " + str(mindfa.is_valid()))
