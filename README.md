# Visualisations of Finite Automata and Algorithms


VoFA is an educational tool designed for beginners in the field of Computer Science.

Automata theory is a branch of computer science that deals with designing abstract self-propelled computing devices that follow a predetermined sequence of operations automatically. A finite automaton, or finite-state machine, is an abstract mathematical model of computation which has a finite number of states. A finite automaton can 
be in exactly one state at any given time and it can transition from one state to another by responding to an input. Any finite-state machine can be described both formally 
and graphically. Although finite automata have less computational power than other models of computations (i.e Turing machines), they are being utilised by many devices and applications of modern society which perform predetermined sequences of actions such as vending machines, traffic lights, CPU control units, and speech recognition software.

In undergraduate courses, finite automata are typically divided into two main classes: Deterministic Finite Automata (DFA) and Non-Deterministic Finite Automata (NFA). 
Through the implementation of the powerset construction algorithm (or NFA to DFA conversion algorithm) one can find the equivalent DFA of a given NFA. Additionally, through 
the DFA minimisation algorithm, a DFA can be converted to its most efficient form with the minimal number of states.

## Functionality and Features:

An automaton can be constructed by drawing it on a digital canvas, simulating the traditional pen and paper experience of adding states and transitions. Users are be able to 
apply the aforementioned powerset construction and minimisation algorithms (depending on the class of automaton) and view the output both as a transition table and a graphical representation. The tool has the following five core functionalities:

1. Construct DFA as graphs
2. Construct NFA as graphs
3. Convert a given NFA to its equivalent DFA
4. Convert a given DFA to its equivalent minimal DFA
5. Convert a given NFA to its equivalent minimal DFA by combining functionalities (3)and (4)

## How to use the Application

### Keybinds:
1. State Creation: Shift-LMB" 
2. Toggle Final State: RMB"
3. Transition Creation: Ctrl-LMB"
   - Click a state while holding down Control
   - Select a second state with LMB
   - Enter transition symbol
   - Separate multiple symbols with commas
   - For the empty arrow use the symbol "$"
4. Undo Action: Ctrl-Z

### Tutorial:



<p align="center">
  <img width="641" height="422" src="https://github.com/avoutsinas/Moon-Base-Delta/blob/main/images/picture3.jpg">
</p>

<p align="center">
  <img width="200" height="267" src="https://github.com/avoutsinas/Moon-Base-Delta/blob/main/Custom_graphics/Animation_Preview_Front.gif">
</p>

## Installation guide
This application is designed to operate on a Windows computer. In order to successfully install the application perform the followin steps:

1. Download the "Visualisation of Finite Automata 1.0.zip" file from the project repository
2. Locate the downloaded file on your computer and extract the files into a new folder
3. Open the folder and run the VoFA.exe file (if the provided shortcut does not work, the exe file can be located in the VoFA files folder)

You are all set!

