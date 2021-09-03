# Visualisations of Finite Automata and Algorithms


VoFA is an educational tool designed for beginners in the field of Computer Science.

## Background
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
1. State Creation: **Shift-LMB**

2. Toggle Final State: **RMB**

3. Transition Creation: **Ctrl-LMB**

   - Click a state while holding down Control
   - Select a second state with LMB
   - Enter transition symbol(s)
   - Separate multiple symbols with commas
   - For the empty arrow use the symbol "$"

4. Undo Action: **Ctrl-Z**

### Tutorial:

Lets suppose that we would like to convert the following NFA from the textbook "Introduction to the theory of computation" to an equivalent DFA. 

<p align="center">
  <img width="400" src="https://github.com/avoutsinas/Visualisations-of-finite-automata/blob/main/source/images/Tutorial/sipser_automaton.png">
</p>


For the sake of simplicity lets assume that we will first place all the states of the automatonon the input canvas and then draw all the transitions. To create a state we have to navigate with the cursor to the input canvas (top right panel) and use the key-bind "Shift + left mouse button". Using this key-bind will prompt an input box on the canvas, which requests a name to be entered for the state. We will name the new state "1". We proceedby selecting "OK" in the input box and a new state is placed on the drawing canvas. It is worth noting that the transition table is also updated with the name of the new state. Since state "1" is the first state to be placed, it is the starting state for the automaton.

<p align="middle">
  <img src="https://github.com/avoutsinas/Visualisations-of-finite-automata/blob/main/source/images/Tutorial/Construction1.PNG" width="480" />
  <img src="https://github.com/avoutsinas/Visualisations-of-finite-automata/blob/main/source/images/Tutorial/Construction2.PNG" width="480" /> 
</p>

By using the same command, we proceed to add states "2" and "3" on the canvas. According to the example NFA, state "1" should be a final state. By hovering over the state with the cursor and using the right mouse button, we can set this state to be a final state.If we use the same command on state "1" again, it will turn back into a non-final state. Since all states have been added, we will proceed to add transitions to the automaton. To create a transition we have to use the key-bind "Control and left mouse button", while hovering over a state. Upon doing so, a temporary arrow is rendered and it follows thecursor until we select a second state, or cancel the transition creation. Selecting a second state, triggers an input prompt which requires us to enter a single or multiple symbolsfor the transition. We separate multiple symbols with commas or space characters. For empty transitions we have to enter the special symbol "$". Upon providing a symbol, the transition is fully rendered. The transition table is also expanded, to reflect the change we made to the automaton.

<p align="middle">
  <img src="https://github.com/avoutsinas/Visualisations-of-finite-automata/blob/main/source/images/Tutorial/Construction4.PNG" width="480" />
  <img src="https://github.com/avoutsinas/Visualisations-of-finite-automata/blob/main/source/images/Tutorial/Construction5.PNG" width="480" /> 
</p>


Once the automaton is constructed, all we have to do to convert it to an equivalent DFA, is to click the "CONVERT" button. Once the convert button is clicked the equivalent DFA is rendered on the output canvas and its transition table is visible on the output window. Wecan reorient the states of the automaton on the output canvas in any desired configuration.

<p align="center">
  <img width="1000" src="https://github.com/avoutsinas/Visualisations-of-finite-automata/blob/main/source/images/Tutorial/Textbook_conversion.PNG">
</p>

By comparing the output with the solution provided in the textbook, we can verify that the automaton was successfully converted. We could also click the "MIN CONVERT" button to view the equivalent minimal DFA, but in this example the output automaton is already in minimal form.

<p align="middle">
  <img src="https://github.com/avoutsinas/Visualisations-of-finite-automata/blob/main/source/images/Tutorial/Construction7.PNG" width="480" />
  <img src="https://github.com/avoutsinas/Visualisations-of-finite-automata/blob/main/source/images/Tutorial/sipser_solution.png" width="480" /> 
</p>

Finally, we can click the "CLEAR" button to reset all panels of the application and begin designing a brand new automaton to convert. To create a DFA and convert it to minimalform, we would simply have to click the tab "DFA" and start designing the input DFA.

## Installation guide
This application is designed to operate on a Windows computer. In order to successfully install  and run the application perform the following steps:

1. Download the ["Visualisation of Finite Automata 1.0.zip"](https://github.com/avoutsinas/Visualisations-of-finite-automata/raw/main/Visualisations%20of%20Finite%20Automata%201.0.zip) file from the project repository

2. Locate the downloaded file on your computer and extract the files into a new folder

3. Open the folder and run the VoFA.exe file (if the provided shortcut does not work, the exe file can be located in the VoFA files folder)

You are all set!

