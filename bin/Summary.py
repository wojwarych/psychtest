import tkinter as tk
from tkinter import ttk

SUPER_LARGE = ("Verdana", 16)
LARGE_FONT = ("Verdana", 11)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 9)

class Summary(tk.Frame):

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		self.controller = controller