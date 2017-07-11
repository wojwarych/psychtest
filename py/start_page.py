import tkinter as tk
from tkinter import ttk

import os.path
from PIL import Image, ImageTk

#constans
SUPER_LARGE = ("Verdana", 16)
LARGE_FONT = ("Verdana", 11)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 9)
APP_DESCRIPTION = """Welcome to PsychTest.

Choose tests you want to run.

Click "Settings" to change test's properties"""


class StartPage(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(0, weight=1)
		self.controller = controller

		#frame for mainpicture
		picframe = tk.Frame(self)
		picframe.grid(row=0, column=0)

		#mainpicture
		basepath = os.path.dirname(__file__)
		imagepath = os.path.abspath(
			os.path.join(basepath, "..", "img", "brain.png"))

		pic = Image.open(imagepath)
		on_screen = ImageTk.PhotoImage(pic)
		logo = tk.Label(picframe, image=on_screen)
		logo.image = on_screen
		logo.grid(row=0, column=0, rowspan=3, sticky='nwse')

		#frame for rest of the frame
		content_frame = tk.Frame(self)
		content_frame.grid(row=0, column=1)

		#frame with description frame, which are grid in the frame above
		description_frame = tk.Frame(content_frame)
		description_frame.grid(row=0, column=0, padx=25, pady=25, sticky='we')
		description = tk.Label(
			description_frame, text=APP_DESCRIPTION, font=LARGE_FONT,
			justify='left')
		description.grid(row=0, column=0, sticky='nwse')

		#chekbuttons to choose which tests to run
		chckbutton_frame = tk.Frame(content_frame)
		chckbutton_frame.grid(row=1, column=0, padx=25, pady=25, sticky='w')

		chck_krep = tk.Checkbutton(
			chckbutton_frame, text="Kraepelin", variable=self.controller.krep,
			font=SMALL_FONT)
		chck_krep.grid(row=1, column=0, sticky='w')
		
		chck_stroop = tk.Checkbutton(
			chckbutton_frame, text="Stroop Test",
			variable=self.controller.stroop, font=SMALL_FONT)
		chck_stroop.grid(row=2, column=0, sticky='w')
		
		chck_rotation = tk.Checkbutton(
			chckbutton_frame, font=SMALL_FONT, text="Mental Rotation Test",
			variable=self.controller.rotation)
		chck_rotation.grid(row=3, column=0, sticky='w')

		#navigation buttons
		button_frame = tk.Frame(content_frame)
		button_frame.grid(row=2, column=0, padx=20, pady=20, sticky='se')

		self.nxt_button = ttk.Button(
			button_frame, text="Next >",
			command=lambda: self.controller.show_frame_handle())
		self.nxt_button.bind(
			"<Return>", lambda f: self.controller.show_frame_handle())
		self.nxt_button.grid(row=0, column=0, padx=2, sticky='se')

		quit_button = ttk.Button(
			button_frame, text="Quit", command=lambda: self.controller.quit_msg())
		quit_button.bind("<Return>", lambda f: self.controller.quit_msg(), "+")
		quit_button.grid(row=0, column=1, padx=2, sticky='se')


	def postupdate(self):


		'''Overrides the behaviour of tkraise() method, which messes focus()'''
		self.nxt_button.focus()