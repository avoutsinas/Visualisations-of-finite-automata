from distutils.core import setup  # Need this to handle modules
import py2exe
import numpy
import string
import tkinter
import PIL
import webbrowser

setup(
    windows=[
        {
            "script": "main.py",
            "icon_resources": [(1, "images//logo.ico")],
            "dest_base": "VoFA"
        }
    ],
    version='1.0',
    name='Visualisations of Finite Automata',
)

# To compile into executable folder run powershell command : 'py setup.py py2exe'
