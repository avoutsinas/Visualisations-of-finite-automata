import numpy as np
from Preliminaries import *
from FA import *

def to_dfa(nfa):
    Q = []
    Q.append(nfa.states[0])

    for state in Q:

