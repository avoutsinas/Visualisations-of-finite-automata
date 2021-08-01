import tkinter as tk
from tkinter import simpledialog
from tkinter import *
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

        self.main_canvas = Canvas(self, width=self.width, height=self.height, bg='#00ffff')
        self.main_canvas.pack(expand=Y, fill=BOTH)

        self.input_canvas = tk.Canvas(self.main_canvas, width=self.width * 0.705, height=self.height * 0.435, bg='white')
        self.input_canvas.pack()

        self.output_canvas = tk.Canvas(self.main_canvas, width=self.width * 0.705, height=self.height * 0.435, bg='white')
        self.output_canvas.pack()

        self.input_window = tk.Canvas(self.main_canvas, width=self.width * 0.25, height=self.height * 0.435, bg='white')
        self.input_window.pack()

        self.output_window = tk.Canvas(self.main_canvas, width=self.width * 0.25, height=self.height * 0.435, bg='white')
        self.output_window.pack()

        self.setup()

        self.selected = None
        self.start_flag = False

        self.states = []
        self.transitions = []

    def setup(self):
        self.main_canvas.create_window(390, 35, anchor=NW, window=self.input_canvas)
        self.main_canvas.create_window(390, 420, anchor=NW, window=self.output_canvas)
        self.main_canvas.create_window(25, 35, anchor=NW, window=self.input_window)
        self.main_canvas.create_window(25, 420, anchor=NW, window=self.output_window)

        self.input_canvas.bind('<1>', self.select_circle)
        self.input_canvas.bind('<Shift-1>', self.create_state)
        # self.input_canvas.bind('<2>', self.make_arc)

    def create_state(self, event):
        new_state = ""
        state_name = simpledialog.askstring(title="State Creation", prompt="Enter the name of the State",
                                            parent=self.input_canvas)

        while state_name == "" or state_name in [i.get_name() for i in self.states]:
            state_name = simpledialog.askstring(title="State Creation", prompt="States must have non-empty and unique "
                                                                               "names.\n\n" "Please select a unique "
                                                                               "name for this state",
                                                parent=self.input_canvas)

        if state_name is not None:
            x, y, r = event.x, event.y, self.radius
            if not self.states:
                new_state = State(state_name, True, False)

                self.input_canvas.create_line(x - r, y, x - 2.2 * r, y, arrow=tk.FIRST, tags="arrow")
                self.input_canvas.create_oval(x - r, y - r, x + r, y + r, outline='black', fill='beige',
                                              tags=(state_name, "first"))
                self.input_canvas.create_text(x, y, text=state_name, fill="black", tags=(state_name, "first", "label"))
            else:
                new_state = State(state_name, False, False)

                self.input_canvas.create_oval(x - r, y - r, x + r, y + r, outline='black', fill='beige',
                                              tags=state_name)
                self.input_canvas.create_text(x, y, text=state_name, fill="black", tags=(state_name, "label"))

        self.states.append(new_state)
        print(self.states)

    def select_circle(self, event):
        x, y = event.x, event.y
        self.input_canvas.bind('<Motion>', self.move_state)
        self.input_canvas.bind('<ButtonRelease-1>', self.deselect)

        if "label" not in self.input_canvas.gettags(tk.CURRENT):
            self.input_canvas.addtag_withtag('selected', tk.CURRENT)
            self.input_canvas.addtag_closest('selected_txt', x, y, halo=13)
            print(self.input_canvas.gettags(tk.CURRENT))
        elif "label" in self.input_canvas.gettags(tk.CURRENT):
            self.input_canvas.addtag_withtag('selected_txt', tk.CURRENT)
            self.input_canvas.addtag_closest('selected', x, y, halo=13, start=tk.CURRENT)
            print(self.input_canvas.gettags(tk.CURRENT))

        if "first" in self.input_canvas.gettags(tk.CURRENT):
            self.start_flag = True
            self.input_canvas.addtag_withtag('selected_arrow', "arrow")
        else:
            self.start_flag = False

    def move_state(self, event):
        x, y, r = event.x, event.y, self.radius

        self.input_canvas.coords('selected', x - r, y - r, x + r, y + r)
        self.input_canvas.coords('selected_txt', x, y)
        if self.start_flag:
            self.input_canvas.coords("selected_arrow", x - r, y, x - 2.2 * r, y)

    def deselect(self, event):
        self.input_canvas.dtag('selected')  # removes the 'selected' tag
        self.input_canvas.dtag('selected_txt')
        self.input_canvas.unbind('<Motion>')
        self.input_canvas.bind('<Shift-1>', self.create_state)
