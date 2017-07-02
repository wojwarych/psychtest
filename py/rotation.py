import tkinter as tk
from tkinter import ttk

import os.path
from PIL import Image, ImageTk
import random

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

#TODO: ROTATION OF IMAGE ONE

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
			buttonframe, text="Start", command=lambda: self.start_window())
		self.startbut.grid(row=0, column=0, pady=5)

		self.startbut.bind("<Return>", lambda f: self.start_window())

		self.generate_image()


	def postupdate(self):


		self.startbut.focus_set()


	def start_window(self):

		
		#remove description of test and nav buttons from view
		self.descrip_text.grid_remove()

		#starting experiment
		self.start_test = tk.Label(
			self.descrip_frame, text="Click Enter to start the test",
			font=LARGE_FONT, justify='center')
		self.start_test.grid(row=0, column=0)
			
		self.startbut['command'] = lambda: self.test_window()
		self.startbut.bind("<Return>", lambda f: self.test_window())
		self.startbut.focus_set()


	def test_window(self, the_number=5):

		self.start_test.grid_remove()
		self.startbut.grid_remove()
		
		if self.controller.rot_counter < the_number:

			self.fix_point = tk.Label(
				self.descrip_frame, text="+", font=SUPER_LARGE, justify='center')
			self.fix_point.grid(row=0, column=0)
			self.fix_point.after(3000, self.pick_letters)

			self.controller.rot_counter += 1

		else:
			self.controller.show_frame("Summary")


	def clear_window(self):

		self.descrip_text.grid_remove()
		self.descrip_text2.grid_remove()

		self.test_window()

	def dict_of_letters(self):

		letters = ('F', 'G', 'J')
		self.dict_letters = {}
		basepath = os.path.dirname(__file__)

		for num, word in enumerate(letters):

			imagepath = os.path.abspath(
				os.path.join(basepath, '..', 'img', letters[num]+'.png'))

			self.dict_letters[letters[num]] = imagepath

	
	def pick_random_letter(self):

		self.dict_of_letters()		
		self.random_letter = random.choice(list(self.dict_letters.values()))


	def generate_image(self):

		self.pick_random_letter()
		pic = Image.open(self.random_letter)
		self.work_pic = ImageTk.PhotoImage(pic)


	def pick_letters(self):


		image1 = self.work_pic
		image2 = self.work_pic

		image1_rot = self.rotate_letter(image1)

		self.descrip_text = tk.Label(self.descrip_frame, image=image1)
		self.descrip_text.image = image1_rot
		self.descrip_text.grid(row=0, column=0, pady=5, padx=5)

		self.descrip_text2 = tk.Label(self.descrip_frame, image=image2)
		self.descrip_text2.image = image2
		self.descrip_text2.grid(row=0, column=1, pady=5, padx=5)
		
		self.descrip_text.bind("<Left>", lambda f: self.clear_window())
		self.descrip_text.focus_set()

	def rotate_letter(self, image):

		angles = [i for i in range (30, 361, 30)]

		image = image.rotate(random.choice(angles))

		return(image)


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