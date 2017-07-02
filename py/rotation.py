import tkinter as tk
from tkinter import ttk

import os.path
from PIL import Image, ImageTk

SUPER_LARGE = ("Verdana", 16)
LARGE_FONT = ("Verdana", 11)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 9)

ROTATION_INTRO = "MENTAL ROTATION TEST"
ROTATION_LETTER = """You're about to shown two same letters.
One of them will be shown normally, the other one
might be rotated and flipped vertically
(reflection symmetry). Your task is to decide if those letters
are the same (are not flipped vertically) or are different."""


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
		
		#Lines underneath - creating additional frames
		#and gridding them in order to properly set the widgets
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
			self.descrip_frame, text=ROTATION_LETTER,
			font=NORMAL_FONT, justify='center')
		self.descrip_text.grid(row=0, column=0)
		
		#Lines underneath - creating additional frames
		#and gridding them in order to properly set the widgets
		buttonframe = tk.Frame(self)
		buttonframe.grid(row=1, column=0)

		self.startbut = ttk.Button(
			buttonframe, text="Start", command=lambda: self.test_window())
		self.startbut.grid(row=0, column=0, pady=5)

		self.startbut.bind("<Return>", lambda f: self.test_window())


	def postupdate(self):


		self.startbut.focus_set()


	def test_window(self):

		#remove description of test and nav buttons from view
		self.descrip_text.grid_remove()

		#starting experiment
		self.start_test = tk.Label(
			self.descrip_frame, text="Click Enter to start the test",
			font=LARGE_FONT, justify='center')
		self.start_test.grid(row=0, column=0)
		

		self.startbut['command'] = lambda: self.letter_test()
		self.startbut.bind("<Return>", lambda f: self.letter_test())
		self.startbut.focus_set()


	def letter_test(self):


		self.grid_columnconfigure(0, minsize=475)
		self.grid_columnconfigure(1, minsize=475)
		self.startbut.grid_remove()

		self.start_test.grid_remove()

		self.fix_point = tk.Label(
			self.descrip_frame, text="+", font=SUPER_LARGE, justify='center')
		self.fix_point.grid(row=0, column=0)

		self.start_test.after(3000, self.pick_letters)


	def pick_letters(self):

		basepath = os.path.dirname(__file__)
		imageakpath = os.path.abspath(
		os.path.join(basepath, "..", "img", "F.png"))
		pic = Image.open(imagepath)
		on_screen = ImageTk.PhotoImage(pic)


		self.fix_point.grid_remove()

		self.descrip_text = tk.Label(
			self.descrip_frame, image=on_screen)
		self.descrip_frame.image = on_screen
		self.descrip_text.grid(row=0, column=0, pady=5, padx=5)

		self.descrip_text2 = tk.Label(
			self.descrip_frame, text="Second letter", font=LARGE_FONT,
			justify='center')
		self.descrip_text2.grid(row=0, column=1, pady=5, padx=5)


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
		
		#Lines underneath - creating additional frames
		#and gridding them in order to properly set the widgets
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
		
		#Lines underneath - creating additional frames
		#and gridding them in order to properly set the widgets
		buttonframe = tk.Frame(self)
		buttonframe.grid(row=1, column=0)

		self.startbut = ttk.Button(
			buttonframe, text="Start", command=lambda: quit())
		self.startbut.grid(row=0, column=0, pady=5)

		self.startbut.bind("<Return>", lambda f: quit())


	def postupdate(self):

		
		self.startbut.focus_set()