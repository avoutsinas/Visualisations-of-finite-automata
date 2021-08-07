import numpy as np
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
from Preliminaries import *
from FA import *
from Algorithms import *


class Board:
    def __init__(self, main, width, height, bg, highlightthickness, highlightbackground, highlightcolor):
        self.radius = main.radius
        self.container = tk.Frame(main, width=width, height=height)
        self.canvas = tk.Canvas(self.container, width=width, height=height, bg=bg,
                                highlightthickness=highlightthickness,
                                highlightbackground=highlightbackground, highlightcolor=highlightcolor,
                                scrollregion=(0, 0, 1.4 * width, 2 * height))

        """
        self.y_scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview, jump=1,
                                        width=12, troughcolor="black")
        self.scrollable_y_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_y_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.pack(side="right", fill="y")

        self.x_scrollbar = tk.Scrollbar(self.container, orient="horizontal", command=self.canvas.xview, jump=1,
                                        width=12, troughcolor="black")
        self.scrollable_x_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_x_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.pack(side="bottom", fill="x")
        """

    def select_state(self, event):
        x, y = event.x, event.y
        event.widget.bind('<Motion>', self.move_state)
        event.widget.bind('<ButtonRelease-1>', self.deselect)

        tags = event.widget.gettags(tk.CURRENT)
        name_tag = tags[0]
        print(name_tag)
        print(event.x, event.y)
        print(event.widget)

        if "label" in tags:
            event.widget.addtag_withtag('selected_txt', tk.CURRENT)
            event.widget.addtag_closest('selected', x, y, halo=13, start=tk.CURRENT)
            event.widget.addtag_withtag("selected_final", name_tag + "final")
            event.widget.addtag_withtag("selected_self_transition", "self" + name_tag)
            event.widget.addtag_withtag("selected_self_transition_text", "self" + name_tag + "text")

            if "first" in event.widget.gettags(tk.CURRENT):
                event.widget.addtag_withtag('selected_arrow', "arrow")

    def deselect(self, event):
        event.widget.dtag('selected')  # removes the 'selected' tag
        event.widget.dtag('selected_txt')
        event.widget.dtag("selected_final")
        event.widget.dtag("selected_self_transition")
        event.widget.dtag("selected_self_transition_text")
        event.widget.unbind('<Motion>')

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

            if "1" in event.widget.gettags(item):
                if x >= x2:
                    exit_coords = (x - r, y + r / 2, midx1, midy1, x3, y3)
                    exit_coords_txt = (midx1, midy1)
                else:
                    exit_coords = (x + r, y - r / 2, midx2, midy2, x3, y3)
                    exit_coords_txt = (midx2, midy2)

            elif "2" in event.widget.gettags(item):
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
        self.radius = self.main.radius
        self.states = []
        self.transitions = []
        self.transition_states = []

    def create_state(self, event):
        new_state = None
        starting = False
        final = None
        font = tkFont.Font(family="calibri", size=13)

        state_name = simpledialog.askstring(title="State Creation", prompt="Enter the name of the State",
                                            parent=event.widget)

        if state_name is not None:
            final = simpledialog.askinteger(title="State Creation", prompt="Is this a final state?\n(0 for non-final "
                                                                           "or 1 for final)",
                                            parent=event.widget)

            while state_name == "" or state_name in [i.get_name() for i in self.states]:
                state_name = simpledialog.askstring(title="State Creation",
                                                    prompt="States must have non-empty and unique "
                                                           "names.\n\n" "Please select a unique "
                                                           "name for this state",
                                                    parent=event.widget)
            while final not in [0, 1, None]:
                final = simpledialog.askinteger(title="State Creation", prompt="Please enter 0 for non-final\nor 1 for "
                                                                               "final",
                                                parent=event.widget)

        if state_name is not None and final is not None:
            x, y, r, r2 = event.x, event.y, self.radius, self.radius - 3

            if not self.states:
                starting = True
                event.widget.create_line(x - r, y, x - 2.2 * r, y, arrow=tk.FIRST, tags=(state_name, "arrow"),
                                         fill="white", width=1.45)
                event.widget.create_oval(x - r, y - r, x + r, y + r, outline='white', fill='#3c3c3c',
                                         tags=(state_name, "circle", "first"), width=1.4)
                event.widget.create_text(x, y, text=state_name, fill="white",
                                         tags=(state_name, state_name + "label", "first", "label"),
                                         font=font)
            else:
                event.widget.create_oval(x - r, y - r, x + r, y + r, outline='white', fill='#3c3c3c',
                                         tags=(state_name, "circle"), width=1.4)
                event.widget.create_text(x, y, text=state_name, fill="white",
                                         tags=(state_name, state_name + "label", "label"), font=font)
            if final == 1:
                event.widget.create_oval(x - r2, y - r2, x + r2, y + r2, outline='white', fill='',
                                         tags=(state_name + "final", "circle"), width=1.4)

                new_state = State(state_name, starting, True)
            else:
                new_state = State(state_name, starting, False)

        if state_name not in ["", None] and final is not None:
            self.record_state(new_state)
        print(self.states)

    def create_transition(self, event):
        x, y, r = event.x, event.y, self.radius
        tags = event.widget.gettags(tk.CURRENT)
        name_tag = tags[0]
        print(name_tag)

        if len(self.transition_states) < 2:
            if self.transition_states == [] and name_tag in [s.get_name() for s in self.states]:
                if "label" in tags:
                    item = event.widget.find_withtag(name_tag + "label")
                    self.start_x, self.start_y = event.widget.coords(item)
                    self.transition_states.append(name_tag)

            elif len(self.transition_states) == 1 and name_tag in [s.get_name() for s in self.states]:
                if name_tag != self.transition_states[0] and "label" in tags:
                    item = event.widget.find_withtag(name_tag + "label")
                    self.end_x, self.end_y = event.widget.coords(item)
                    self.transition_states.append(name_tag)
                    self.draw_transition(event, r)
                    self.transition_states = []
                elif name_tag == self.transition_states[0] and "label" in tags:
                    item = event.widget.find_withtag(name_tag + "label")
                    self.end_x, self.end_y = event.widget.coords(item)
                    self.start_x, self.start_y = self.end_x, self.end_y
                    self.transition_states.append(name_tag)
                    self.draw_self_transition(event, r)
                    self.transition_states = []
            else:
                self.transition_states = []

    def draw_self_transition(self, event, r):
        state = None
        state_name = self.transition_states[0]
        tag_to_add = ("self" + state_name, "self_transition")
        tag_to_add_txt = ("self" + state_name + "text", "text")

        x1 = self.start_x - 0.9 * r
        y1 = y2 = self.start_y - 0.5 * r
        x2 = self.start_x + 0.9 * r

        midx = (x1 + x2) / 2
        midy = (y1 - 3 * r)

        points = ((x1, y1), (midx, midy), (x2, y2))

        if "s_t" not in event.widget.gettags(tk.CURRENT):
            transition_letters = simpledialog.askstring(title="Transition Creation",
                                                        prompt="Specify the letter or letters that are used in this "
                                                               "transition.\n\n Multiple letters should be seperated "
                                                               "by commas.",
                                                        parent=event.widget)
            if transition_letters not in ["", None]:
                event.widget.create_text(midx, midy + 15, text=transition_letters, fill="white", tags=tag_to_add_txt)

                event.widget.create_line(points, arrow='last', smooth=1, fill="white", tags=tag_to_add, width=1.45)
                event.widget.addtag_withtag("s_t", tk.CURRENT)
                self.record_transition(transition_letters, same=True)

    def draw_transition(self, event, r):
        existing_arrows = midx = y_txt = tag_to_add = tag_to_add_txt = points = None
        input_prompt = "Specify the letter or letters that are used in this transition.\n\n " \
                       "Multiple letters should be seperated by commas."

        if self.start_x <= self.end_x:
            tag_to_add = ("from_" + self.transition_states[0], "to_" + self.transition_states[1], "transition", "1")
            tag_to_add_txt = (str((*tag_to_add, "text")), "text")
            existing_arrows = event.widget.find_withtag(str((*tag_to_add, "text")))

            midx = (self.start_x + self.end_x) / 2
            midy = (self.start_y + self.end_y) / 2 - np.abs(self.start_x - self.end_x) / 6
            y_txt = midy - 1
            points = ((self.start_x + r, self.start_y - r / 2), (midx, midy), (self.end_x - r, self.end_y - r / 2))

        elif self.start_x > self.end_x:
            tag_to_add = ("from_" + self.transition_states[0], "to_" + self.transition_states[1], "transition", "2")
            tag_to_add_txt = (str((*tag_to_add, "text")), "text")
            existing_arrows = event.widget.find_withtag(str((*tag_to_add, "text")))

            midx = (self.start_x + self.end_x) / 2
            midy = (self.start_y + self.end_y) / 2 + np.abs(self.start_x - self.end_x) / 6
            y_txt = midy + 1
            points = ((self.start_x - r, self.start_y + r / 2), (midx, midy), (self.end_x + r, self.end_y + r / 2))

        if existing_arrows == ():
            transition_letters = simpledialog.askstring(title="Transition Creation", prompt=input_prompt,
                                                        parent=event.widget)
            if transition_letters not in ["", None]:
                event.widget.create_text(midx, y_txt, text=transition_letters, fill="white", tags=tag_to_add_txt)
                event.widget.create_line(points, arrow='last', smooth=1, fill="white", tags=tag_to_add, width=1.45)
                self.record_transition(transition_letters, same=False)

    def record_state(self, new_state):
        self.states.append(new_state)
        self.update_input_window()

    def record_transition(self, transition_letters, same):
        if same:
            state = None
            state_name = self.transition_states[0]
            for s in self.states:
                if s.get_name() == state_name:
                    state = s

            for letter in transition_letters:
                if letter not in [",", "", " "] and state is not None:
                    self.transitions.append((state, letter, state))
                    print(self.transitions)
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
                    self.transitions.append((state1, letter, state2))
                    print(self.transitions)
        self.update_input_window()

    def update_input_window(self):
        fa = self.main.create_automaton()
        self.main.input_window.update_output(str(fa))


class Window:
    def __init__(self, main, width, height, bg, highlightthickness, highlightbackground, highlightcolor):
        self.container = tk.Frame(main, width=width, height=height)
        self.canvas = tk.Canvas(self.container, width=width, height=height, bg=bg,
                                highlightthickness=highlightthickness,
                                highlightbackground=highlightbackground, highlightcolor=highlightcolor,
                                scrollregion=(0, 0, 0, 0))

        self.y_scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview, jump=1,
                                        width=12, troughcolor="black")
        self.scrollable_y_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_y_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)
        self.y_scrollbar.pack(side="right", fill="y")

        self.x_scrollbar = tk.Scrollbar(self.container, orient="horizontal", command=self.canvas.xview, jump=1,
                                        width=12, troughcolor="black")
        self.scrollable_x_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_x_frame, anchor="nw")
        self.canvas.configure(xscrollcommand=self.x_scrollbar.set)
        self.x_scrollbar.pack(side="bottom", fill="x")

        self.width = width
        self.height = height
        self.font = tkFont.Font(family="consolas", size=14)

    def show_pos(self, event):
        print(event.x, event.y)


class OutputWindow(Window):
    def __init__(self, main, width, height, bg, highlightthickness, highlightbackground, highlightcolor):
        super().__init__(main, width, height, bg, highlightthickness, highlightbackground, highlightcolor)

        self.starting_string = "\nTransition table" + "\n\n" + "    |  " + delta + "   "
        self.table_to_print = self.starting_string
        self.canvas.create_text(width / 50, height / 50, text=self.table_to_print, fill="black",
                                tags="output_table", font=self.font, anchor=NW)

    def update_output(self, string):
        self.table_to_print = string
        self.canvas.delete("output_table")
        self.canvas.create_text(self.width / 100, self.height / 100, text=self.table_to_print, fill="black",
                                tags="output_table", font=self.font, anchor=NW)
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def reset_output(self):
        reset_string = self.starting_string
        self.update_output(reset_string)


class App(Frame):
    radius = 20

    def __init__(self):
        super().__init__()

        self.width = 1400
        self.height = 850

        self.fa = Dfa(name="InputGraphFA")

        self.pack(expand=Y, fill=BOTH)

        self.image1 = Image.open("images//Blackboard.jpg").resize((self.width, self.height), Image.ANTIALIAS)
        self.image2 = Image.open("images//Blackboard2.jpg").resize((self.width, self.height), Image.ANTIALIAS)
        self.bg1 = ImageTk.PhotoImage(self.image1)
        self.bg2 = ImageTk.PhotoImage(self.image2)

        self.main_canvas = Canvas(self, width=self.width, height=self.height, bg="gray")
        # self.main_canvas.create_image(0,0,image=self.bg, anchor="nw")
        self.main_canvas.pack(expand=Y, fill=BOTH)

        self.input_board = InputBoard(self, width=self.width * 0.705, height=self.height * 0.435,
                                      bg='white', highlightthickness=5, highlightbackground="black",
                                      highlightcolor="black")
        self.input_board.canvas.create_image(0, 0, image=self.bg1, anchor="nw")
        self.input_board.canvas.pack()

        self.output_board = tk.Canvas(self.main_canvas, width=self.width * 0.705, height=self.height * 0.435,
                                      bg='white', highlightthickness=5, highlightbackground="black",
                                      highlightcolor="black")
        self.output_board.create_image(0, 0, image=self.bg2, anchor="nw")
        self.output_board.pack()

        self.input_window = OutputWindow(self.main_canvas, width=self.width * 0.25, height=self.height * 0.435,
                                         bg='white', highlightthickness=5, highlightbackground="black",
                                         highlightcolor="black")
        self.input_window.canvas.pack()

        self.output_window = OutputWindow(self.main_canvas, width=self.width * 0.25, height=self.height * 0.435,
                                          bg='white', highlightthickness=5, highlightbackground="black",
                                          highlightcolor="black")
        self.output_window.canvas.pack()

        self.setup()

    def setup(self):
        self.winfo_toplevel().title("VoFA")
        label = Entry(self)
        # label.pack(side="top", fill="x")

        self.main_canvas.create_window(389, 31, anchor=NW, window=self.input_board.container)
        self.main_canvas.create_window(389, 424, anchor=NW, window=self.output_board)
        self.main_canvas.create_window(17, 31, anchor=NW, window=self.input_window.container)
        self.main_canvas.create_window(17, 424, anchor=NW, window=self.output_window.container)

        self.input_board.canvas.bind('<1>', self.input_board.select_state)
        self.input_board.canvas.bind('<Shift-1>', self.input_board.create_state)
        self.input_board.canvas.bind('<BackSpace>', self.clear_input)
        self.input_board.canvas.bind('<Control-1>', self.input_board.create_transition)
        self.input_board.canvas.bind('r', self.create_automaton)
        self.input_board.canvas.bind('t', self.minimize_dfa)
        self.output_window.canvas.bind('<1>', self.output_window.show_pos)

    def create_automaton(self):
        if self.fa.Q != []:
            self.fa.clear()
        if self.input_board.states != []:
            for s in self.input_board.states:
                self.fa.add_state(s.get_name(), s.is_final)
        if self.input_board.transitions != []:
            for t in self.input_board.transitions:
                self.fa.add_transition(*t)
        print(self.fa)
        return self.fa

    def minimize_dfa(self, event):

        if self.fa.Q != [] and self.fa.is_valid():
            min = Minimise()
            minimised_fa = min.convert(self.fa)
            self.output_window.update_output(str(minimised_fa))
            print(minimised_fa)

    def clear_input(self, event):
        self.input_board.canvas.delete("circle", "arrow", "label", "transition", "self_transition", "text")
        self.input_board.states = []
        self.input_board.transitions = []
        self.input_board.transition_states = []
        self.fa.clear()
        self.input_window.reset_output()
        self.output_window.reset_output()
