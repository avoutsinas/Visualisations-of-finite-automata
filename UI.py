import numpy as np
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from tkinter import simpledialog
from PIL import Image, ImageTk
from Preliminaries import *
from FA import *
from Algorithms import *


class App(Frame):
    radius = 20

    def __init__(self):
        super().__init__()
        self.pack(expand=Y, fill=BOTH)
        self.width = 1400
        self.height = 850

        self.image = Image.open("images//Blackboard.jpg").resize((self.width, self.height), Image.ANTIALIAS)
        self.bg = ImageTk.PhotoImage(self.image)

        self.main_canvas = Canvas(self, width=self.width, height=self.height, bg="gray")
        # self.main_canvas.create_image(0,0,image=self.bg, anchor="nw")
        self.main_canvas.pack(expand=Y, fill=BOTH)

        self.input_canvas = tk.Canvas(self.main_canvas, width=self.width * 0.705, height=self.height * 0.435,
                                      bg='white')
        self.input_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.input_canvas.pack()

        self.output_canvas = tk.Canvas(self.main_canvas, width=self.width * 0.705, height=self.height * 0.435,
                                       bg='white')
        self.output_canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.output_canvas.pack()

        self.input_window = tk.Canvas(self.main_canvas, width=self.width * 0.25, height=self.height * 0.435, bg='white')
        self.input_window.pack()

        self.output_window = tk.Canvas(self.main_canvas, width=self.width * 0.25, height=self.height * 0.435,
                                       bg='white')
        self.output_window.pack()

        self.setup()

        self.selected = None
        self.start_x, self.start_y, self.end_x, self.end_y = 0, 0, 0, 0

        self.states = []
        self.transitions = []
        self.transition_states = []

    def setup(self):
        self.main_canvas.create_window(390, 35, anchor=NW, window=self.input_canvas)
        self.main_canvas.create_window(390, 420, anchor=NW, window=self.output_canvas)
        self.main_canvas.create_window(25, 35, anchor=NW, window=self.input_window)
        self.main_canvas.create_window(25, 420, anchor=NW, window=self.output_window)

        self.input_canvas.bind('<1>', self.select_state)
        self.input_canvas.bind('<Shift-1>', self.create_state)
        self.input_canvas.bind('<BackSpace>', self.clear_input)
        self.input_canvas.bind('<Control-1>', self.create_transition)

    def create_state(self, event):
        new_state = None
        final = None
        font = tkFont.Font(family="calibri", size=12)

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
                event.widget.create_line(x - r, y, x - 2.2 * r, y, arrow=tk.FIRST, tags=(state_name, "arrow"),
                                         fill="white", width=1.45)
                event.widget.create_oval(x - r, y - r, x + r, y + r, outline='black', fill='beige',
                                         tags=(state_name, "circle", "first"), width=1.4)
                event.widget.create_text(x, y, text=state_name, fill="black", tags=(state_name, "first", "label"),
                                         font=font)
            else:
                event.widget.create_oval(x - r, y - r, x + r, y + r, outline='black', fill='beige',
                                         tags=(state_name, "circle"), width=1.4)
                event.widget.create_text(x, y, text=state_name, fill="black", tags=(state_name, "label"), font=font)
            if final == 1:
                event.widget.create_oval(x - r2, y - r2, x + r2, y + r2, outline='black', fill='',
                                         tags=(state_name + "final", "circle"), width=1.4)

                new_state = State(state_name, False, True)
            else:
                new_state = State(state_name, False, False)

        if state_name not in ["", None] and final is not None:
            self.states.append(new_state)
        print(self.states)

    def create_transition(self, event):
        x, y, r = event.x, event.y, self.radius
        tags = event.widget.gettags(tk.CURRENT)
        name_tag = tags[0]
        print(name_tag)

        if len(self.transition_states) < 2:
            if self.transition_states == [] and name_tag in [i.get_name() for i in self.states]:
                if "label" in tags:
                    event.widget.addtag_withtag('start_point', tk.CURRENT)
                    self.start_x = x
                    self.start_y = y
                    self.transition_states.append(name_tag)
                    print("found starting point")
                    print(tags)
                    print(self.transition_states)

            elif len(self.transition_states) == 1 and name_tag in [i.get_name() for i in self.states]:
                if name_tag != self.transition_states[0]:
                    if "label" in tags or "circle" in tags:
                        event.widget.addtag_withtag('end_point', tk.CURRENT)
                        self.end_x = x
                        self.end_y = y
                        self.transition_states.append(name_tag)
                        print("found end point")
                        print(tags)
                        print(self.transition_states)

                        self.draw_arrow(event, r)
                        self.transition_states = []
                elif name_tag == self.transition_states[0]:
                    tag_to_add = ("from" + self.transition_states[0], "transition", "3")
                    # event.widget.create_line()
            else:
                self.transition_states = []

    def draw_arrow(self, event, r):
        if self.start_x < self.end_x:
            tag_to_add = ("from" + self.transition_states[0], "to" + self.transition_states[1], "transition", "1")

            midx = (self.start_x + self.end_x) / 2
            midy = (self.start_y + self.end_y) / 2 - np.abs(self.start_x - self.end_x) / 6

            points = ((self.start_x + r, self.start_y - r / 2), (midx, midy), (self.end_x - r, self.end_y - r / 2))

            transition_letters = simpledialog.askstring(title="Transition Creation",
                                                        prompt="Specify the letter or letters that are used in this "
                                                               "transition.\n\n Multiple letters should be seperated "
                                                               "by commas.",
                                                        parent=event.widget)

            if transition_letters not in ["", None]:
                event.widget.create_text(midx, midy - 1, text=transition_letters, fill="white", tags=(
                    transition_letters, "text", "text_from" + self.transition_states[0],
                    "text_to" + self.transition_states[1], "1"))

                event.widget.create_line(points, arrow='last', smooth=1, fill="white", tags=tag_to_add, width=1.45)
            else:
                self.transition_states = []

        elif self.start_x > self.end_x:
            tag_to_add = ("from" + self.transition_states[0], "to" + self.transition_states[1], "transition", "2")

            midx = (self.start_x + self.end_x) / 2
            midy = (self.start_y + self.end_y) / 2 + np.abs(self.start_x - self.end_x) / 6

            points = ((self.start_x - r, self.start_y + r / 2), (midx, midy), (self.end_x + r, self.end_y + r / 2))

            transition_letters = simpledialog.askstring(title="Transition Creation",
                                                        prompt="Specify the letter or letters that are used in this "
                                                               "transition.\n\n Multiple letters should be seperated "
                                                               "by commas.",
                                                        parent=event.widget)

            if transition_letters not in ["", None]:
                event.widget.create_text(midx, midy + 1, text=transition_letters, fill="white", tags=(
                    transition_letters, "text", "text_from" + self.transition_states[0],
                    "text_to" + self.transition_states[1], "2"))

                event.widget.create_line(points, arrow='last', smooth=1, fill="white", tags=tag_to_add, width=1.45)
            else:
                self.transition_states = []

    def select_state(self, event):
        x, y = event.x, event.y
        event.widget.bind('<Motion>', self.move_state)
        event.widget.bind('<ButtonRelease-1>', self.deselect)

        tags = event.widget.gettags(tk.CURRENT)
        name_tag = tags[0]
        print(name_tag)

        if "label" in tags:
            event.widget.addtag_withtag('selected_txt', tk.CURRENT)
            event.widget.addtag_closest('selected', x, y, halo=13, start=tk.CURRENT)
            event.widget.addtag_withtag("selected_final", name_tag + "final")
            event.widget.addtag_withtag("selected_exit_transition", "from" + name_tag)
            event.widget.addtag_withtag("selected_entry_transition", "to" + name_tag)
            # print(event.widget.gettags(tk.CURRENT))

            if "first" in event.widget.gettags(tk.CURRENT):
                event.widget.addtag_withtag('selected_arrow', "arrow")

    def deselect(self, event):
        event.widget.dtag('selected')  # removes the 'selected' tag
        event.widget.dtag('selected_txt')
        event.widget.dtag("selected_final")
        event.widget.dtag("selected_exit_transition")
        event.widget.dtag("selected_entry_transition")
        event.widget.unbind('<Motion>')
        event.widget.bind('<Shift-1>', self.create_state)

    def move_state(self, event):
        x, y, r, r2 = event.x, event.y, self.radius, self.radius - 3

        tags = event.widget.gettags(tk.CURRENT)
        name_tag = tags[0]

        if "label" in tags:
            event.widget.coords('selected', x - r, y - r, x + r, y + r)
            event.widget.coords('selected_txt', x, y)
            event.widget.coords("selected_final", x - r2, y - r2, x + r2, y + r2)
            if "first" in tags:
                event.widget.coords("selected_arrow", x - r, y, x - 2.2 * r, y)

            self.move_state_transitions(event, name_tag, x, y, r)

    def move_state_transitions(self, event, name_tag, x, y, r):
        self.move_outbound_transitions(event, name_tag, x, y, r)
        self.move_inbound_transitions(event, name_tag, x, y, r)

    @staticmethod
    def move_outbound_transitions(event, name_tag, x, y, r):
        exit_arrows = event.widget.find_withtag("from" + name_tag)
        exit_arrow_text = event.widget.find_withtag("text_from" + name_tag)

        for item in exit_arrows:
            exiting = event.widget.coords(item)

            x1, y1, x2, y2, x3, y3 = exiting
            midx = (x + x3) / 2
            midy1 = (y + y3) / 2 + np.abs(x - x3) / 6
            midy2 = (y + y3) / 2 - np.abs(x - x3) / 6
            exit_coords = None

            if "1" in event.widget.gettags(item):
                if x >= x2:
                    exit_coords = (x - r, y + r / 2, midx, midy1, x3, y3)
                    for text in exit_arrow_text:
                        if "1" in event.widget.gettags(text):
                            event.widget.coords(text, midx, midy1)
                else:
                    exit_coords = (x + r, y - r / 2, midx, midy2, x3, y3)
                    for text in exit_arrow_text:
                        if "1" in event.widget.gettags(text):
                            event.widget.coords(text, midx, midy2)

            elif "2" in event.widget.gettags(item):
                if x >= x2:
                    exit_coords = (x - r, y + r / 2, midx, midy1, x3, y3)
                    for text in exit_arrow_text:
                        if "2" in event.widget.gettags(text):
                            event.widget.coords(text, midx, midy1)
                else:
                    exit_coords = (x + r, y - r / 2, midx, midy2, x3, y3)
                    for text in exit_arrow_text:
                        if "2" in event.widget.gettags(text):
                            event.widget.coords(text, midx, midy2)

            event.widget.coords(item, *exit_coords)

    @staticmethod
    def move_inbound_transitions(event, name_tag, x, y, r):
        entry_arrows = event.widget.find_withtag("to" + name_tag)
        entry_arrow_text = event.widget.find_withtag("text_to" + name_tag)

        for item in entry_arrows:
            moved = False
            entry = event.widget.coords(item)

            x4, y4, x5, y5, x6, y6 = entry
            midx = (x4 + x) / 2
            midy1 = (y + y4) / 2 - np.abs(x - x4) / 6
            midy2 = (y + y4) / 2 + np.abs(x - x4) / 6
            entry_coords = None

            if x >= x4:
                entry_coords = (x4, y4, midx, midy1, x - r, y - r / 2)
                for text in entry_arrow_text:
                    event.widget.coords(text, midx, midy1)
            else:
                entry_coords = (x4, y4, midx, midy2, x + r, y + r / 2)
                for text in entry_arrow_text:
                    event.widget.coords(text, midx, midy2)

            event.widget.coords(item, *entry_coords)

    def clear_input(self, event):
        event.widget.delete("circle", "arrow", "label", "transition", "text")
        self.states = []
