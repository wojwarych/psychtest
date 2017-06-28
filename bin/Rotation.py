import tkinter as tk
from tkinter import ttk

SUPER_LARGE = ("Verdana", 16)
LARGE_FONT = ("Verdana", 11)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 9)

ROTATION_INTRO = "MENTAL ROTATION TEST"

class Rotation(tk.Frame):

#TODO: NAVIGATION, DESCRIPTION, STROOPTEST CLASS FOR TEST ITSELF

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)

		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		self.descrip_text = tk.Label(
			self.descrip_frame, text=ROTATION_INTRO, font=LARGE_FONT,
			justify='center')
		self.descrip_text.grid(row=0, column=0)
		
		#Lines underneath - creating additional frames and gridding them in
		#order to properly set the widgets
		buttonframe = tk.Frame(self)
		buttonframe.grid(row=1, column=0)

		self.nextbut = ttk.Button(
			buttonframe, text="Next", command=lambda: self.test_handler())
		self.nextbut.grid(row=0, column=0, padx=15, pady=5)

		self.nextbut.bind("<Return>", lambda f: self.test_handler())
		
		self.quitbut = ttk.Button(	
			buttonframe, text="Quit", command=lambda: quit())
		self.quitbut.grid(row=0, column=1, padx=15, pady=5)


	def postupdate(self):


		self.nextbut.focus_set()


	def test_handler(self):


		if self.controller.type_rotation.get() == 'a':

			self.controller.show_frame("RotationLetter")


class RotationLetter(tk.Frame):

#TODO: NAVIGATION, DESCRIPTION, STROOPTEST CLASS FOR TEST ITSELF

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)

		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		self.descrip_text = tk.Label(
			self.descrip_frame, text=ROTATION_INTRO,
			font=LARGE_FONT, justify='center')
		self.descrip_text.grid(row=0, column=0)
		
		#Lines underneath - creating additional frames and gridding them in
		#order to properly set the widgets
		buttonframe = tk.Frame(self)
		buttonframe.grid(row=1, column=0)

		self.startbut = ttk.Button(
			buttonframe, text="Start", command=lambda: quit())
		self.startbut.grid(row=0, column=0, pady=5)

		self.startbut.bind("<Return>", lambda f: quit())


	def postupdate(self):
		self.startbut.focus_set()


class RotationFigure(tk.Frame):

#TODO: NAVIGATION, DESCRIPTION, STROOPTEST CLASS FOR TEST ITSELF

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)

		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		self.descrip_text = tk.Label(
			self.descrip_frame, text=ROTATION_INTRO, font=LARGE_FONT,
			justify='center')
		self.descrip_text.grid(row=0, column=0)
		
		#Lines underneath - creating additional frames and gridding them in
		#order to properly set the widgets
		buttonframe = tk.Frame(self)
		buttonframe.grid(row=1, column=0)

		self.startbut = ttk.Button(
			buttonframe, text="Start", command=lambda: quit())
		self.startbut.grid(row=0, column=0, pady=5)

		self.startbut.bind("<Return>", lambda f: quit())


	def postupdate(self):
		self.startbut.focus_set()


class RotationImage(tk.Frame):

#TODO: NAVIGATION, DESCRIPTION, STROOPTEST CLASS FOR TEST ITSELF

	def __init__(self, parent, controller):

		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)

		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		self.descrip_text = tk.Label(
			self.descrip_frame, text=ROTATION_INTRO, font=LARGE_FONT,
			justify='center')
		self.descrip_text.grid(row=0, column=0)
		
		#Lines underneath - creating additional frames and gridding them in
		#order to properly set the widgets
		buttonframe = tk.Frame(self)
		buttonframe.grid(row=1, column=0)

		self.startbut = ttk.Button(
			buttonframe, text="Start", command=lambda: quit())
		self.startbut.grid(row=0, column=0, pady=5)

		self.startbut.bind("<Return>", lambda f: quit())


	def postupdate(self):
		self.startbut.focus_set()