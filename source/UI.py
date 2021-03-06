import numpy as np
import string
import webbrowser
import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
from tkinter import simpledialog
from PIL import Image, ImageTk
from Preliminaries import *
from FA import *
from Algorithms import *

tutorial_txt1 = "                  Welcome!" \
                "\n\n You can begin constructing an automaton!" \
                "\n\n                  Keybinds:" \
                "\n\n State Creation: Shift-LMB" \
                "\n\n Toggle Final State: RMB" \
                "\n\n Transition Creation: Ctrl-LMB" \
                "\n\n * Click a state while holding down Control" \
                "\n\n * Select a second state with LMB" \
                "\n\n * Enter transition symbol" \
                "\n\n * Separate multiple symbols with commas" \
                '\n\n * For the empty arrow use the symbol "$" ' \
                "\n\n Undo Action: Ctrl-Z " \
                "\n\n               Functionality:" \
                "\n\n Depending on your selected options you can: " \
                "\n\n a) Convert a NFA to its equivalent DFA" \
                "\n\n b) Convert a NFA to its equivalent min-DFA" \
                "\n\n c) Convert a DFA to its minimal form"


class Board:
    def __init__(self, main, width, height, bg, highlightthickness, highlightbackground, highlightcolor):
        self.main = main
        self.radius = main.radius
        self.font = tkFont.Font(family="consolas", size=13)
        self.font_small = tkFont.Font(family="consolas", size=10)
        self.font_extra_small = tkFont.Font(family="consolas", size=8)

        self.container = tk.Frame(self.main, width=width, height=height)
        self.canvas = tk.Canvas(self.container, width=width, height=height, bg=bg,
                                highlightthickness=highlightthickness,
                                highlightbackground=highlightbackground, highlightcolor=highlightcolor,
                                scrollregion=(0, 0, 1.4 * width, 2 * height))

        self.y_scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview, jump=1,
                                        width=12, troughcolor="black")
        self.scrollable_y_frame = tk.Frame(self.container)
        self.canvas.create_window((0, 0), window=self.scrollable_y_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.pack(side="right", fill="y")

        self.x_scrollbar = tk.Scrollbar(self.container, orient="horizontal", command=self.canvas.xview, jump=1,
                                        width=12, troughcolor="black")
        self.scrollable_x_frame = tk.Frame(self.container)
        self.canvas.create_window((0, 0), window=self.scrollable_x_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.pack(side="bottom", fill="x")

        self.canvas.create_image(0, 0, image=self.main.bg, anchor="nw", tag="background")
        self.canvas.pack()

    def select_state(self, event):
        x, y = event.x, event.y
        event.widget.bind('<B1-Motion>', self.move_state)
        event.widget.bind('<ButtonRelease-1>', self.deselect)

        tags = event.widget.gettags(tk.CURRENT)
        name_tag = tags[0]
        print(name_tag)

        if "label" in tags:
            event.widget.addtag_withtag('selected_txt', tk.CURRENT)
            event.widget.addtag_closest('selected', x, y, halo=13, start=tk.CURRENT)
            event.widget.addtag_withtag("selected_final", name_tag + "final")
            event.widget.addtag_withtag("selected_self_transition", "self" + name_tag)
            event.widget.addtag_withtag("selected_self_transition_text", "self" + name_tag + "text")

            if "first" in event.widget.gettags(tk.CURRENT):
                event.widget.addtag_withtag('selected_arrow', "arrow")

            event.widget.itemconfig('selected', fill="#696969")

    def deselect(self, event):
        event.widget.itemconfig('selected', fill="#3c3c3c")
        event.widget.dtag('selected')  # removes the 'selected' tag
        event.widget.dtag('selected_txt')
        event.widget.dtag("selected_final")
        event.widget.dtag("selected_self_transition")
        event.widget.dtag("selected_self_transition_text")
        event.widget.unbind('<B1-Motion>')

    def move_state(self, event):
        x, y, r, r2 = event.x, event.y, self.radius, self.radius - 3

        tags = event.widget.gettags(tk.CURRENT)
        name_tag = tags[0]

        if "label" in tags:
            event.widget.coords('selected', x - r, y - r, x + r, y + r)
            event.widget.coords('selected_txt', x, y)
            event.widget.coords("selected_final", x - r2, y - r2, x + r2, y + r2)

            # coords for self-transitions
            x1 = x - 0.9 * r
            y1 = y - 0.5 * r
            x2 = x + 0.9 * r
            midx = (x1 + x2) / 2
            midy = (y1 - 3 * r)

            event.widget.coords("selected_self_transition", x1, y1, midx, midy, x2, y1)
            event.widget.coords("selected_self_transition_text", midx, midy + 15)
            if "first" in tags:
                event.widget.coords("selected_arrow", x - r, y, x - 2.2 * r, y)

            self.move_state_transitions(event, name_tag, x, y, r)

    def move_state_transitions(self, event, name_tag, x, y, r):
        self.move_outbound_transitions(event, name_tag, x, y, r)
        self.move_inbound_transitions(event, name_tag, x, y, r)

    @staticmethod
    def move_outbound_transitions(event, name_tag, x, y, r):
        exit_arrows = event.widget.find_withtag("from_" + name_tag)

        for item in exit_arrows:
            item_tags = event.widget.gettags(item)
            text_tag = str((*item_tags, "text"))
            text = event.widget.find_withtag(text_tag)

            exiting = event.widget.coords(item)
            x1, y1, x2, y2, x3, y3 = exiting
            midx1 = (x - r + x3) / 2
            midx2 = (x + r + x3) / 2
            midy1 = (y + y3) / 2 + np.abs(x - x3) / 6
            midy2 = (y + y3) / 2 - np.abs(x - x3) / 6
            exit_coords, exit_coords_txt = None, None

            if "type1" in event.widget.gettags(item):
                if x >= x2:
                    exit_coords = (x - r, y + r / 2, midx1, midy1, x3, y3)
                    exit_coords_txt = (midx1, midy1)
                else:
                    exit_coords = (x + r, y - r / 2, midx2, midy2, x3, y3)
                    exit_coords_txt = (midx2, midy2)

            elif "type2" in event.widget.gettags(item):
                if x >= x2:
                    exit_coords = (x - r, y + r / 2, midx1, midy1, x3, y3)
                    exit_coords_txt = (midx1, midy1)
                else:
                    exit_coords = (x + r, y - r / 2, midx2, midy2, x3, y3)
                    exit_coords_txt = (midx2, midy2)

            event.widget.coords(item, *exit_coords)
            event.widget.coords(text, *exit_coords_txt)

    @staticmethod
    def move_inbound_transitions(event, name_tag, x, y, r):
        entry_arrows = event.widget.find_withtag("to_" + name_tag)

        for item in entry_arrows:
            entry = event.widget.coords(item)
            item_tags = event.widget.gettags(item)
            text_tag = str((*item_tags, "text"))
            text = event.widget.find_withtag(text_tag)

            x4, y4, x5, y5, x6, y6 = entry
            midx1 = (x4 + x - r) / 2
            midx2 = (x4 + x + r) / 2
            midy1 = (y + y4) / 2 - np.abs(x - x4) / 6
            midy2 = (y + y4) / 2 + np.abs(x - x4) / 6

            if x >= x4:
                entry_coords = (x4, y4, midx1, midy1, x - r, y - r / 2)
                entry_coords_txt = (midx1, midy1)
            else:
                entry_coords = (x4, y4, midx2, midy2, x + r, y + r / 2)
                entry_coords_txt = (midx2, midy2)

            event.widget.coords(item, *entry_coords)
            event.widget.coords(text, *entry_coords_txt)


class InputBoard(Board):
    def __init__(self, main, width, height, bg, highlightthickness, highlightbackground, highlightcolor):
        super().__init__(main, width, height, bg, highlightthickness, highlightbackground, highlightcolor)

        self.main = main
        self.start_x, self.start_y, self.end_x, self.end_y = 0, 0, 0, 0
        self.radius = main.radius
        self.states = []
        self.transitions = []
        self.transition_states = []
        self.tracer_drawn = False
        self.memory = []

        self.setup()

    def setup(self):
        self.canvas.bind('<1>', self.select_state)
        self.canvas.bind('<2>', self.set_final)
        self.canvas.bind('<3>', self.set_final)
        self.canvas.bind('<Shift-1>', self.create_state)
        self.canvas.bind('<Control-1>', self.create_transition)
        self.canvas.bind('<Control-z>', self.undo)

    def create_state(self, event):
        new_state = None
        starting = False
        final = False

        state_name = simpledialog.askstring(title="State Creation", prompt="Enter the name of the State",
                                            parent=event.widget)

        while state_name == "" or state_name in [i.get_name() for i in self.states]:
            state_name = simpledialog.askstring(title="State Creation",
                                                prompt="States must have non-empty and unique "
                                                       "names.\n\n" "Please select a unique "
                                                       "name for this state",
                                                parent=event.widget)
        if state_name is not None and final is not None:
            x, y, r, r2 = event.x, event.y, self.radius, self.radius - 3

            if not self.states:
                starting = True
                event.widget.create_line(x - r, y, x - 2.2 * r, y, arrow=tk.FIRST,
                                         tags=(state_name, "state" + state_name, "arrow"),
                                         fill="white", width=1.45)
                event.widget.create_oval(x - r, y - r, x + r, y + r, outline='white', fill='#3c3c3c',
                                         tags=(state_name, "state" + state_name, "circle", "first"), width=1.4)
                event.widget.create_text(x, y, text=state_name, fill="white",
                                         tags=(
                                             state_name, "state" + state_name, state_name + "label", "first", "label"),
                                         font=self.font)
            else:
                event.widget.create_oval(x - r, y - r, x + r, y + r, outline='white', fill='#3c3c3c',
                                         tags=(state_name, "state" + state_name, "circle"), width=1.4)
                event.widget.create_text(x, y, text=state_name, fill="white",
                                         tags=(state_name, "state" + state_name, state_name + "label", "label"),
                                         font=self.font)

            new_state = State(state_name, starting, final)

        if state_name not in ["", None] and final is not None:
            self.record_state(new_state)
        print(self.states)

    def set_final(self, event):
        r, r2 = self.radius, self.radius - 3
        tags = event.widget.gettags(tk.CURRENT)

        if "label" in tags or "circle" in tags:
            x, y = event.widget.coords(tags[0] + "label")
            state_name = tags[0]

            selected_state = [s for s in self.states if s.get_name() == state_name][0]
            final = selected_state.is_final

            if final:
                self.canvas.delete(state_name + "final")
                selected_state.is_final = False
            else:
                event.widget.create_oval(x - r2, y - r2, x + r2, y + r2, outline='white', fill='',
                                         tags=(state_name, "state" + state_name, state_name + "final", "circle"),
                                         width=1.4)
                selected_state.is_final = True

            self.main.update_input_window()

    def create_transition(self, event):
        x, y, r = event.x, event.y, self.radius
        tags = event.widget.gettags(tk.CURRENT)
        name_tag = tags[0]
        # print(name_tag)

        if len(self.transition_states) < 2:
            if self.transition_states == [] and name_tag in [s.get_name() for s in self.states]:
                if "label" in tags or "circle" in tags:
                    item = event.widget.find_withtag(name_tag + "label")
                    self.start_x, self.start_y = event.widget.coords(item)
                    self.transition_states.append(name_tag)
                    self.set_tracer(stop=False)

            elif len(self.transition_states) == 1 and name_tag in [s.get_name() for s in self.states]:
                if name_tag != self.transition_states[0] and ("label" in tags or "circle" in tags):
                    item = event.widget.find_withtag(name_tag + "label")
                    self.end_x, self.end_y = event.widget.coords(item)
                    self.transition_states.append(name_tag)
                    self.draw_transition(event, r)
                    self.transition_states = []
                    self.set_tracer(stop=True)
                    print(self.tracer_drawn)
                elif name_tag == self.transition_states[0] and ("label" in tags or "circle" in tags):
                    item = event.widget.find_withtag(name_tag + "label")
                    self.end_x, self.end_y = event.widget.coords(item)
                    self.start_x, self.start_y = self.end_x, self.end_y
                    self.transition_states.append(name_tag)
                    self.draw_self_transition(event, r)
                    self.transition_states = []
                    self.set_tracer(stop=True)
                    print(self.tracer_drawn)
            else:
                self.transition_states = []
                self.set_tracer(stop=True)
                print(self.tracer_drawn)

    def draw_self_transition(self, event, r):
        state_name = self.transition_states[0]
        tag_to_add = ("self" + state_name, "self_transition")
        tag_to_add_txt = ("self" + state_name + "text", "text")
        existing_arrows = event.widget.find_withtag("self" + state_name + "text")
        # print(existing_arrows)

        x1 = self.start_x - 0.9 * r
        y1 = y2 = self.start_y - 0.5 * r
        x2 = self.start_x + 0.9 * r

        midx = (x1 + x2) / 2
        midy = (y1 - 3 * r)

        points = ((x1, y1), (midx, midy), (x2, y2))

        if existing_arrows == ():
            transition_letters = simpledialog.askstring(title="Transition Creation",
                                                        prompt="Specify the letter or letters that are used in this "
                                                               "transition.\n\n Multiple letters should be seperated "
                                                               "by commas.",
                                                        parent=event.widget)
            transition_letters = self.find_empty_word(transition_letters, True)

            if transition_letters not in ["", None]:
                o1 = event.widget.create_text(midx, midy + 15, text=transition_letters, fill="white",
                                              tags=tag_to_add_txt,
                                              font=self.font_small)

                o2 = event.widget.create_line(points, arrow='last', smooth=1, fill="white", tags=tag_to_add, width=1.45)
                self.record_transition(transition_letters, o1, o2, same=True)

    def draw_transition(self, event, r):
        existing_arrows = midx = y_txt = points = None
        input_prompt = "Specify the letter or letters that are used in this transition.\n\n " \
                       "Multiple letters should be seperated by commas."
        tag_to_add = ["from_" + self.transition_states[0], "to_" + self.transition_states[1], "transition"]
        if self.start_x <= self.end_x:
            tag_to_add.append("type1")
            existing_arrows = event.widget.find_withtag(str((*tag_to_add, "text")))

            midx = (self.start_x + self.end_x) / 2
            midy = (self.start_y + self.end_y) / 2 - np.abs(self.start_x - self.end_x) / 6
            y_txt = midy - 1
            points = ((self.start_x + r, self.start_y - r / 2), (midx, midy), (self.end_x - r, self.end_y - r / 2))

        elif self.start_x > self.end_x:
            tag_to_add.append("type2")
            existing_arrows = event.widget.find_withtag(str((*tag_to_add, "text")))

            midx = (self.start_x + self.end_x) / 2
            midy = (self.start_y + self.end_y) / 2 + np.abs(self.start_x - self.end_x) / 6
            y_txt = midy + 1
            points = ((self.start_x - r, self.start_y + r / 2), (midx, midy), (self.end_x + r, self.end_y + r / 2))

        tag_to_add_txt = (str((*tag_to_add, "text")), "text")

        if existing_arrows == ():
            transition_letters = simpledialog.askstring(title="Transition Creation", prompt=input_prompt,
                                                        parent=event.widget)
            transition_letters = self.find_empty_word(transition_letters, False)

            if transition_letters not in ["", None]:
                o1 = event.widget.create_text(midx, y_txt, text=transition_letters, fill="white", tags=tag_to_add_txt,
                                              font=self.font_small)
                o2 = event.widget.create_line(points, arrow='last', smooth=1, fill="white", tags=tag_to_add, width=1.45)
                self.record_transition(transition_letters, o1, o2, same=False)

    def set_tracer(self, stop):
        if not stop:
            self.canvas.unbind('<1>')
            self.canvas.unbind('<2>')
            self.canvas.unbind('<3>')
            self.canvas.unbind('<Shift-1>')
            self.canvas.unbind('<Control-z>')
            self.canvas.unbind('<B1-Motion>')
            self.canvas.bind('<1>', self.create_transition)
            self.canvas.bind('<Motion>', self.draw_tracer_line)
        elif stop:
            self.canvas.unbind('<1>')
            self.tracer_drawn = False
            self.canvas.bind('<1>', self.select_state)
            self.canvas.bind('<2>', self.set_final)
            self.canvas.bind('<3>', self.set_final)
            self.canvas.bind('<Shift-1>', self.create_state)
            self.canvas.bind('<Control-z>', self.undo)
            self.canvas.delete("tracer")
            self.canvas.unbind('<Motion>')

    def draw_tracer_line(self, event):
        x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y

        if abs(x1 - x2) < self.radius and abs(y1 - y2) < self.radius:
            x1 = x1 - self.radius
            x2 = x1 + 2 * self.radius
            y2 = y1 = y1 - 9
            midx = (x1 + x2) / 2
            midy = (y1 - 3 * self.radius)
            points = (x1, y1, midx, midy, x2, y2)
        else:
            if x1 <= x2 and y1 <= y2:
                x1 = x1 + self.radius
                x2, y2 = x2 - 5, y2 - 3
            elif x1 < x2 and y1 > y2:
                x1 = x1 + self.radius
                x2, y2 = x2 - 5, y2 + 3
            elif x1 > x2 and y1 <= y2:
                x1 = x1 - self.radius
                x2, y2 = x2 + 5, y2 - 3
            elif x1 > x2 and y1 > y2:
                x1 = x1 - self.radius
                x2, y2 = x2 + 5, y2 + 3
            points = (x1, y1, x2, y2)

        if not self.tracer_drawn:
            self.canvas.create_line(*points, fill="white", width=1.45, arrow="last",
                                    smooth=1, tags="tracer")
            self.tracer_drawn = True
        else:
            self.canvas.coords("tracer", *points)

    def record_state(self, new_state):
        self.states.append(new_state)
        self.main.update_input_window()
        self.memory.append([new_state])

    def record_transition(self, transition_letters, obj1, obj2, same):
        self.memory.append([obj1, obj2])
        if same:
            state = None
            state_name = self.transition_states[0]
            for s in self.states:
                if s.get_name() == state_name:
                    state = s

            for letter in transition_letters:
                if letter not in [",", ".", "", " "] and state is not None:
                    to_add = (state, letter, state)
                    self.transitions.append(to_add)
                    self.memory[-1].append(to_add)
        else:
            state1 = state2 = None
            state_name1, state_name2 = self.transition_states[0], self.transition_states[1]

            for s in self.states:
                if state1 is not None and state2 is not None:
                    break
                else:
                    if s.get_name() == state_name1:
                        state1 = s
                    elif s.get_name() == state_name2:
                        state2 = s

            for letter in transition_letters:
                if letter not in [",", "", " "] and state1 is not None and state2 is not None:
                    to_add = (state1, letter, state2)
                    self.transitions.append(to_add)
                    self.memory[-1].append(to_add)

        print(self.transitions)
        self.main.update_input_window()

    def undo(self, event):
        if self.memory != []:
            current = self.memory.pop()
            if isinstance(current[0], State):
                print("found state")
                state_to_remove = current[0]
                self.states.remove(state_to_remove)
                print(state_to_remove.get_name())
                self.canvas.delete("state" + state_to_remove.get_name())
            elif type(current[0]) is int:
                self.canvas.delete(current[0])
                self.canvas.delete(current[1])
                for i in range(2, len(current)):
                    transition_to_remove = current[i]
                    self.transitions.remove(transition_to_remove)
            else:
                print("busted")

            self.main.update_input_window()

    def reset(self):
        self.canvas.delete("circle", "arrow", "label", "transition", "self_transition", "text", "tracer")
        self.states = []
        self.transitions = []
        self.transition_states = []
        self.memory = []

    @staticmethod
    def find_empty_word(txt, same):
        if same and txt is not None:
            to_return = txt.replace("$,", "")
            to_return = to_return.replace("$", "")
        elif not same and txt is not None:
            to_return = txt.replace("$", epsilon)
        else:
            to_return = txt

        to_return = [''.join(c for c in s if c not in string.punctuation) for s in to_return]

        temp = ""
        for i in range(len(sorted(to_return))):
            if to_return[i] not in [" ", ","] and to_return[i] not in temp:
                temp += to_return[i] + ","
        to_return = temp[:-1]

        return to_return


class OutputBoard(Board):
    def __init__(self, main, width, height, bg, highlightthickness, highlightbackground, highlightcolor):
        super().__init__(main, width, height, bg, highlightthickness, highlightbackground, highlightcolor)

        self.main = main
        self.flag = False
        self.initial_x = (width / 30) + 30
        self.initial_y = height / 2
        self.state_x_pos = self.initial_x
        self.state_y_pos = self.initial_y
        self.distance_factor = 10
        self.radius = self.main.radius
        self.same_state_transitions = []

        self.setup()

    def setup(self):
        self.canvas.bind('<1>', self.select_state)

    def get_same_state_transitions(self, fa):
        letters = None
        for t in fa.get_d():
            start = t.get_start_state()
            end = t.get_end_state()
            for t in fa.get_d():
                if t.get_start_state() == start and t.get_end_state() == end:
                    if letters is None:
                        letters = t.letter
                    elif letters is not None and t.letter not in letters:
                        letters += "," + t.letter
            combined_transition = DfaTransition(start, letters, end)
            if combined_transition not in self.same_state_transitions:
                self.same_state_transitions.append(combined_transition)
            letters = None

        # print(self.same_state_transitions)

    def render_automaton(self, fa):
        self.get_same_state_transitions(fa)

        if 0 <= len(fa.get_Q()) <= 5:
            self.distance_factor = 10
        elif 6 <= len(fa.get_Q()) <= 10:
            self.distance_factor = 5
        elif len(fa.get_Q()) > 10:
            self.distance_factor = 3

        for s in fa.get_Q():
            # print(s)
            self.create_state(s)
        for t in self.same_state_transitions:
            # print(t)
            self.create_transition(t)

    def create_state(self, s):
        state_name = s.get_name()
        starting = s.is_start
        final = s.is_final

        x, y = self.get_state_coordinates()
        r, r2 = self.radius, self.radius - 3

        if starting:
            self.canvas.create_line(x - r, y, x - 2.2 * r, y, arrow=tk.FIRST, tags=(state_name, "arrow"),
                                    fill="white", width=1.45)
            self.canvas.create_oval(x - r, y - r, x + r, y + r, outline='white', fill='#3c3c3c',
                                    tags=(state_name, "circle", "first"), width=1.4)
            self.canvas.create_text(x, y, text=state_name, fill="white",
                                    tags=(state_name, state_name + "label", "first", "label", (x, y)),
                                    font=self.font_extra_small)
        else:
            self.canvas.create_oval(x - r, y - r, x + r, y + r, outline='white', fill='#3c3c3c',
                                    tags=(state_name, "circle"), width=1.4)
            self.canvas.create_text(x, y, text=state_name, fill="white",
                                    tags=(state_name, state_name + "label", "label", (x, y)),
                                    font=self.font_extra_small)
        if final == 1:
            self.canvas.create_oval(x - r2, y - r2, x + r2, y + r2, outline='white', fill='',
                                    tags=(state_name, state_name + "final", "circle"), width=1.4)

    def create_transition(self, t):
        state1 = self.canvas.find_withtag(t.get_start_name() + "label")
        state2 = self.canvas.find_withtag(t.get_end_name() + "label")
        transition_letters = t.letter
        x1, y1 = self.canvas.coords(state1)
        x2, y2 = self.canvas.coords(state2)
        r = self.radius

        if t.get_start_name() == t.get_end_name():
            name = t.get_start_name()
            self.draw_self_transition(name, x1, y1, x2, y2, transition_letters, r)
            # print("self-drawn" + str(t))
        else:
            name1 = t.get_start_name()
            name2 = t.get_end_name()
            self.draw_transition(name1, name2, x1, y1, x2, y2, transition_letters, r)
            # print("drawn" + str(t))

    def draw_self_transition(self, name, x1, y1, x2, y2, transition_letters, r):
        state_name = name
        tag_to_add = ("self" + state_name, "self_transition")
        tag_to_add_txt = ("self" + state_name + "text", "text")

        x1 = x1 - 0.9 * r
        y1 = y1 - 0.5 * r
        x2 = x1 + 2 * 0.9 * r
        y2 = y1

        midx = (x1 + x2) / 2
        midy = (y1 - 3 * r)

        points = ((x1, y1), (midx, midy), (x2, y2))

        if transition_letters not in ["", None]:
            self.canvas.create_text(midx, midy + 15, text=transition_letters, fill="white",
                                    tags=tag_to_add_txt, font=self.font_small)

            self.canvas.create_line(points, arrow='last', smooth=1, fill="white", tags=tag_to_add, width=1.45)

    def draw_transition(self, name1, name2, x1, y1, x2, y2, transition_letters, r):
        midx = y_txt = points = None

        tag_to_add = ["from_" + name1, "to_" + name2, "transition"]
        if x1 <= x2:
            tag_to_add.append("type1")

            midx = (x1 + x2) / 2
            midy = (y1 + y2) / 2 - np.abs(x1 - x2) / 6
            y_txt = midy - 1
            points = ((x1 + r, y1 - r / 2), (midx, midy), (x2 - r, y2 - r / 2))

        elif x1 > x2:
            tag_to_add.append("type2")

            midx = (x1 + x2) / 2
            midy = (y1 + y2) / 2 + np.abs(x1 - x2) / 6
            y_txt = midy + 1
            points = ((x1 - r, y1 + r / 2), (midx, midy), (x2 + r, y2 + r / 2))

        tag_to_add_txt = (str((*tag_to_add, "text")), "text")

        if transition_letters not in ["", None]:
            self.canvas.create_text(midx, y_txt, text=transition_letters, fill="white", tags=tag_to_add_txt,
                                    font=self.font_small)
            self.canvas.create_line(points, arrow='last', smooth=1, fill="white", tags=tag_to_add, width=1.45)

    def get_state_coordinates(self, vertical=False):
        if self.state_x_pos == self.initial_x:
            to_return = self.state_x_pos, self.state_y_pos
            self.state_x_pos += self.distance_factor * self.radius
        elif self.state_x_pos == self.initial_x + self.distance_factor * self.radius:
            if vertical:
                self.state_y_pos = self.initial_y - 2 * self.radius
            to_return = self.state_x_pos, self.state_y_pos
            self.state_x_pos += self.distance_factor * self.radius
        else:
            if not self.flag and vertical:
                self.state_y_pos = self.initial_y + 2 * self.radius
                self.flag = True
            elif self.flag and vertical:
                self.state_y_pos = self.initial_y - 2 * self.radius
                self.flag = False
            to_return = self.state_x_pos, self.state_y_pos
            self.state_x_pos += self.distance_factor * self.radius
        return to_return

    def reset(self):
        self.same_state_transitions = []
        self.state_x_pos, self.state_y_pos = self.initial_x, self.initial_y
        self.flag = False
        self.canvas.delete("circle", "arrow", "label", "transition", "self_transition", "text")


class Window:
    def __init__(self, main, width, height, bg, highlightthickness, highlightbackground, highlightcolor):
        self.main = main
        self.width = width
        self.height = height
        self.font = tkFont.Font(family="consolas", size=14)
        self.font_small = tkFont.Font(family="consolas", size=11)

        self.container = tk.Frame(main, width=self.width, height=self.height)
        self.canvas = tk.Canvas(self.container, width=width, height=height, bg=bg,
                                highlightthickness=highlightthickness,
                                highlightbackground=highlightbackground, highlightcolor=highlightcolor,
                                scrollregion=(0, 0, width, height))

        self.y_scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview, jump=1,
                                        width=12, troughcolor="black")
        self.scrollable_y_frame = tk.Frame(self.container)

        self.x_scrollbar = tk.Scrollbar(self.container, orient="horizontal", command=self.canvas.xview, jump=1,
                                        width=12, troughcolor="black")
        self.scrollable_x_frame = tk.Frame(self.container)

        self.setup()

    def setup(self):
        self.canvas.create_window((0, 0), window=self.scrollable_y_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=self.scrollable_x_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.pack(side="bottom", fill="x")

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

        self.canvas.create_image(0, 0, image=self.main.bg, anchor="nw", tag="background")
        self.canvas.pack()

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def show_pos(self, event):
        print(event.x, event.y)


class OutputWindow(Window):
    def __init__(self, main, width, height, bg, highlightthickness, highlightbackground, highlightcolor, offset=50,
                 txt=""):
        super().__init__(main, width, height, bg, highlightthickness, highlightbackground, highlightcolor)

        self.offset = offset
        self.starting_string = txt
        self.table_to_print = self.starting_string

    def update_output(self, string, tutorial=False):
        width = (self.width / 100)
        if tutorial:
            font = self.font_small
            height = (self.height / self.offset) + 15
        else:
            font = self.font
            height = (self.height / self.offset)

        self.table_to_print = string
        self.canvas.delete("output_table")
        self.canvas.create_text(width, height, text=self.table_to_print, fill="white",
                                tags="output_table", font=font, anchor=NW)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def configure_txt(self, txt):
        self.starting_string = txt

    def reset_output(self):
        reset_string = self.starting_string
        if self.starting_string == tutorial_txt1:
            self.update_output(reset_string, True)
        else:
            self.update_output(reset_string, False)


class App(Frame):
    radius = 20

    def __init__(self):
        super().__init__()

        self.width = 1400
        self.height = 850
        self.font = tkFont.Font(family="consolas", size=14)
        self.font_small = tkFont.Font(family="consolas", size=10)
        self.font_tiny = tkFont.Font(family="consolas", size=8)

        self.fa = Nfa(name="InputNFA")

        self.pack(expand=Y, fill=BOTH)

        self.image0 = Image.open("source//images//logo.ico")
        self.image1 = Image.open("source//images//Window_Blackboard.jpg").resize((self.width, self.height),
                                                                                 Image.ANTIALIAS)
        self.main_logo = ImageTk.PhotoImage(self.image0)
        self.bg = ImageTk.PhotoImage(self.image1)

        self.main_canvas = Canvas(self, width=self.width + 17, height=self.height, bg="gray")
        # self.main_canvas.create_image(0,0,image=self.bg, anchor="nw")
        self.main_canvas.pack(expand=Y, fill=BOTH)

        self.input_board = InputBoard(self, width=self.width * 0.705, height=self.height * 0.435,
                                      bg='black', highlightthickness=5, highlightbackground="black",
                                      highlightcolor="black")

        self.output_board = OutputBoard(self, width=self.width * 0.705, height=self.height * 0.435,
                                        bg='black', highlightthickness=5, highlightbackground="black",
                                        highlightcolor="black")

        self.input_window = OutputWindow(self, width=self.width * 0.25, height=self.height * 0.435,
                                         bg='black', highlightthickness=5, highlightbackground="black",
                                         highlightcolor="black", offset=7, txt=str(self.fa))

        self.output_window = OutputWindow(self, width=self.width * 0.25, height=self.height * 0.435,
                                          bg='black', highlightthickness=5, highlightbackground="black",
                                          highlightcolor="black", txt=tutorial_txt1)

        self.clear_button = tk.Button(self, text="CLEAR", anchor="center", command=lambda: self.clear_input(),
                                      font=self.font_small)
        self.clear_button.configure(width=24, height=1, activebackground="gray", relief=RAISED)

        self.dfa_button = tk.Button(self, text="DFA", anchor="center", bg="gray",
                                    command=lambda: self.dfa_button_press(), font=self.font_small)
        self.dfa_button.configure(width=24, height=1, activebackground="black", activeforeground="white", relief=RAISED)

        self.nfa_button = tk.Button(self, text="NFA", anchor="center", bg="gray", fg="black",
                                    command=lambda: self.nfa_button_press(), font=self.font_small)
        self.nfa_button.configure(width=24, height=1, activebackground="black", activeforeground="white", relief=SUNKEN)

        self.convert_button = tk.Button(self, text="CONVERT", anchor="center", bg="gray", fg="black",
                                        command=lambda: self.convert_fa(), font=self.font_small)
        self.convert_button.configure(width=24, height=1, activebackground="black", activeforeground="white", bd=3.5,
                                      relief=RAISED)

        self.min_convert_button = tk.Button(self, text="MIN CONVERT", anchor="center", bg="gray", fg="black",
                                            command=lambda: self.min_convert_nfa(), font=self.font_small)
        self.min_convert_button.configure(width=22, height=1, activebackground="black", activeforeground="white",
                                          bd=3.5,
                                          relief=RAISED)

        self.info_button = tk.Button(self, text="About", anchor="center", fg="black",
                                     command=lambda: self.info_button_press(), font=self.font_tiny)
        self.info_button.configure(width=7, height=1, activebackground="black", activeforeground="white",
                                   relief=RAISED)

        self.setup()

    def setup(self):
        self.position_app()

        self.main_canvas.create_window(389, 20, anchor=NW, window=self.input_board.container)
        self.main_canvas.create_window(389, 413, anchor=NW, window=self.output_board.container)
        self.main_canvas.create_window(17, 20, anchor=NW, window=self.input_window.container)
        self.main_canvas.create_window(17, 413, anchor=NW, window=self.output_window.container)
        self.main_canvas.create_window((self.width + 17) / 2, self.height / 1.0425, anchor=NW, window=self.clear_button)
        self.main_canvas.create_window(22, 25, anchor=NW, window=self.nfa_button)
        self.main_canvas.create_window(194.3, 25, anchor=NW, window=self.dfa_button)
        self.main_canvas.create_window(204.3, 52, anchor=NW, window=self.min_convert_button)
        self.main_canvas.create_window(22, 52, anchor=NW, window=self.convert_button)
        self.main_canvas.create_window(self.width * 0.12, self.height / 1.04, anchor=NW,
                                       window=self.info_button)

        self.clear_input()

    def position_app(self):
        self.winfo_toplevel().title("VoFA")
        self.winfo_toplevel().iconbitmap(default="source//images//logo.ico")

        # get screen width and height
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight() - 100  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - ((self.width + 17) / 2)
        y = (hs / 2) - (self.height / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.winfo_toplevel().geometry('%dx%d+%d+%d' % ((self.width + 17), self.height, x, y))

    def create_automaton(self):
        if self.fa.Q != []:
            self.fa.clear()
        if self.input_board.states != []:
            for s in self.input_board.states:
                self.fa.add_state(s.get_name(), s.is_final)
        if self.input_board.transitions != []:
            for t in self.input_board.transitions:
                self.fa.add_transition(*t)
        return self.fa

    def convert_fa(self):
        self.output_board.reset()
        if self.fa.type() == "dfa":
            if self.fa.is_valid():
                min = Minimise()
                minimised_fa = min.convert(self.fa)
                self.output_window.update_output(str(minimised_fa))
                self.output_board.render_automaton(minimised_fa)
        elif self.fa.type() == "nfa":
            if self.fa.Q != [] and self.fa.d != []:
                det = Determinise()
                determinised_fa = det.convert(self.fa)
                self.output_window.update_output(str(determinised_fa))
                self.output_board.render_automaton(determinised_fa)

    def min_convert_nfa(self):
        self.output_board.reset()
        if self.fa.type() == "nfa":
            if self.fa.Q != [] and self.fa.d != []:
                det = Determinise()
                min = Minimise()
                determinised_fa = det.convert(self.fa)
                if determinised_fa.is_valid():
                    renamed_fa, name_index = min.rename_fa_states(determinised_fa)
                    min_det_fa = min.convert(renamed_fa)
                    self.output_window.update_output(str(min_det_fa) + name_index)
                    self.output_board.render_automaton(min_det_fa)

    def nfa_button_press(self):
        print("NFA Selected")
        self.nfa_button.config(relief=SUNKEN)
        self.dfa_button.config(relief=RAISED)
        self.convert_button.configure(text="CONVERT", width=24)
        self.min_convert_button.lift()
        self.fa = Nfa(name="InputNFA")
        self.input_window.configure_txt(str(self.fa))
        self.clear_input()

    def dfa_button_press(self):
        print("DFA Selected")
        self.dfa_button.config(relief=SUNKEN)
        self.nfa_button.config(relief=RAISED)
        self.convert_button.configure(text="MINIMISE", width=48)
        self.min_convert_button.lower()
        self.fa = Dfa(name="InputDFA")
        self.input_window.configure_txt(str(self.fa))
        self.clear_input()

    def info_button_press(self):
        webbrowser.open_new(r"https://github.com/avoutsinas/Visualisations-of-finite-automata/blob/main/README.md")

    def update_input_window(self):
        fa = self.create_automaton()
        self.input_window.update_output(str(fa))

    def clear_input(self):
        self.input_board.reset()
        self.output_board.reset()
        self.fa.clear()
        self.input_window.reset_output()
        self.output_window.reset_output()


def app_startup(skip=False):
    if not skip:
        splash_root = Tk()
        splash_root.overrideredirect(1)
        splash_root.title("VoFa")
        splash_root.winfo_toplevel().iconbitmap(default="source//images//logo.ico")

        splash_root_canvas = tk.Canvas(splash_root, width=700, height=500)
        splash_image = Image.open("source//images//logo.png").resize((700, 500), Image.ANTIALIAS)
        splash_logo = ImageTk.PhotoImage(splash_image)
        splash_root_canvas.create_image(0, 0, image=splash_logo, anchor="nw", tag="background")
        splash_root_canvas.pack()

        # get screen width and height
        ws = splash_root.winfo_screenwidth()  # width of the screen
        hs = splash_root.winfo_screenheight() - 100  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (700 / 2)
        y = (hs / 2) - (500 / 2)

        # set the dimensions of the screen
        # and where it is placed
        splash_root.winfo_toplevel().geometry('%dx%d+%d+%d' % (700, 500, x, y))

        splash_root.after(2000, splash_root.destroy)  # after(ms,func)
        splash_root.mainloop()
    App().mainloop()
