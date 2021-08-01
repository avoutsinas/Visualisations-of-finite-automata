import tkinter as tk
from tkinter import simpledialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
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

        self.image = Image.open("images\Blackboard.jpg").resize((self.width, self.height), Image.ANTIALIAS)
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
        self.start_flag = False

        self.states = []
        self.transitions = []
        self.found_state = []

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
        new_state = ""
        state_name = simpledialog.askstring(title="State Creation", prompt="Enter the name of the State",
                                            parent=self.input_canvas)
        final = simpledialog.askinteger(title="State Creation", prompt="Is this a final state?",
                                        parent=self.input_canvas)

        while state_name == "" or state_name in [i.get_name() for i in self.states]:
            state_name = simpledialog.askstring(title="State Creation", prompt="States must have non-empty and unique "
                                                                               "names.\n\n" "Please select a unique "
                                                                               "name for this state",
                                                parent=self.input_canvas)
        while final not in [0, 1, None]:
            final = simpledialog.askinteger(title="State Creation", prompt="Please enter 0 for non-final\nor 1 for "
                                                                           "final",
                                            parent=self.input_canvas)

        if state_name is not None and final is not None:
            x, y, r, r2 = event.x, event.y, self.radius, self.radius - 3

            if not self.states:
                self.input_canvas.create_line(x - r, y, x - 2.2 * r, y, arrow=tk.FIRST, tags=(state_name, "arrow"))
                self.input_canvas.create_oval(x - r, y - r, x + r, y + r, outline='black', fill='beige',
                                              tags=(state_name, "circle", "first"))
                self.input_canvas.create_text(x, y, text=state_name, fill="black", tags=(state_name, "first", "label"))
                if final == 1:
                    new_state = State(state_name, True, True)
                    self.input_canvas.create_oval(x - r2, y - r2, x + r2, y + r2, outline='black', fill='',
                                                  tags=(state_name + "final", "circle"))
                else:
                    new_state = State(state_name, True, False)
            else:
                self.input_canvas.create_oval(x - r, y - r, x + r, y + r, outline='black', fill='beige',
                                              tags=(state_name, "circle"))
                self.input_canvas.create_text(x, y, text=state_name, fill="black", tags=(state_name, "label"))
                if final == 1:
                    new_state = State(state_name, False, True)
                    self.input_canvas.create_oval(x - r2, y - r2, x + r2, y + r2, outline='black', fill='',
                                                  tags=(state_name + "final", "circle"))
                else:
                    new_state = State(state_name, False, False)

        if state_name not in ["", None] and final is not None:
            self.states.append(new_state)
        print(self.states)

    def select_state(self, event):
        x, y = event.x, event.y
        self.input_canvas.bind('<Motion>', self.move_state)
        self.input_canvas.bind('<ButtonRelease-1>', self.deselect)
        self.input_canvas.bind('<Control-1>', self.create_transition)

        tags = self.input_canvas.gettags(tk.CURRENT)
        name_tag = tags[0]
        print(name_tag)

        if "label" in tags:
            self.input_canvas.addtag_withtag('selected_txt', tk.CURRENT)
            self.input_canvas.addtag_closest('selected', x, y, halo=13, start=tk.CURRENT)
            self.input_canvas.addtag_withtag("selected_final", name_tag + "final")
            self.input_canvas.addtag_withtag("selected_exit_transition", "from" + name_tag)
            self.input_canvas.addtag_withtag("selected_entry_transition", "to" + name_tag)
            # print(self.input_canvas.gettags(tk.CURRENT))

            if "first" in self.input_canvas.gettags(tk.CURRENT):
                self.input_canvas.addtag_withtag('selected_arrow', "arrow")

    def move_state(self, event):
        x, y, r, r2 = event.x, event.y, self.radius, self.radius - 3

        tags = self.input_canvas.gettags(tk.CURRENT)
        name_tag = tags[0]

        if "label" in tags:
            self.input_canvas.coords('selected', x - r, y - r, x + r, y + r)
            self.input_canvas.coords('selected_txt', x, y)
            self.input_canvas.coords("selected_final", x - r2, y - r2, x + r2, y + r2)
            if "first" in self.input_canvas.gettags(tk.CURRENT) and "label" in tags:
                self.input_canvas.coords("selected_arrow", x - r, y, x - 2.2 * r, y)

            exit_arrows = self.input_canvas.find_withtag("from" + name_tag)
            print(exit_arrows)
            exit = self.input_canvas.coords("selected_exit_transition")
            if len(exit) > 0:
                x1, y1, x2, y2 = self.input_canvas.coords("selected_exit_transition")
                self.input_canvas.coords("selected_exit_transition", x + r, y, x2, y2)

            entry = self.input_canvas.coords("selected_entry_transition")
            if len(entry) > 0:
                x3, y3, x4, y4 = entry
                self.input_canvas.coords("selected_entry_transition", x3, y3, x - r, y)

    def create_transition(self, event):
        x, y, r = event.x, event.y, self.radius
        tags = self.input_canvas.gettags(tk.CURRENT)
        name_tag = tags[0]
        print(name_tag)

        if len(self.found_state) < 2:
            if self.found_state == [] and name_tag in [i.get_name() for i in self.states]:
                if "label" in tags:
                    self.input_canvas.addtag_withtag('start_point', tk.CURRENT)
                    self.start_x = x
                    self.start_y = y
                    self.found_state.append(name_tag)
                    print("found starting point")
                    print(tags)
                    print(self.found_state)

            if len(self.found_state) == 1 and name_tag in [i.get_name() for i in self.states]:
                if name_tag != self.found_state[0]:
                    if "label" in tags:
                        self.input_canvas.addtag_withtag('end_point', tk.CURRENT)
                        self.end_x = x
                        self.end_y = y
                        self.found_state.append(name_tag)
                        print("found end point")
                        print(tags)
                        print(self.found_state)

                        if self.start_x < self.end_x:
                            self.input_canvas.create_line(self.start_x + r, self.start_y, self.end_x - r, self.end_y,
                                                          arrow=tk.LAST, tags=(
                                    "from" + self.found_state[0], "to" + self.found_state[1],
                                    "transition"))
                        else:
                            self.input_canvas.create_line(self.start_x - r, self.start_y, self.end_x + r, self.end_y,
                                                          arrow=tk.LAST, tags=(
                                    "from" + self.found_state[0], "to" + self.found_state[1],
                                    "transition"))

                        self.found_state = []

    def deselect(self, event):
        self.input_canvas.dtag('selected')  # removes the 'selected' tag
        self.input_canvas.dtag('selected_txt')
        self.input_canvas.dtag("selected_final")
        self.input_canvas.dtag("selected_exit_transition")
        self.input_canvas.dtag("selected_entry_transition")
        self.input_canvas.unbind('<Motion>')
        self.input_canvas.bind('<Shift-1>', self.create_state)

    def clear_input(self, event):
        self.input_canvas.delete("circle", "arrow", "label", "transition")
        self.states = []
