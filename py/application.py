import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


import os.path
import webbrowser

from kraepelin import Kraepelin, KrepTest, KrepFinish
from start_page import StartPage
from stroop import Stroop, StroopColor, StroopNumber, StroopFigural, StroopFinish
from rotation import Rotation, RotationLetter, RotationFigure, RotationAnimal, RotationFinish
from summary import Summary

#constans
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 9)
ABOUT_DESCRIPTION = """This is the test text about 'PsychTest' project."""
APP_DESCRIPTION = """Welcome to PsychTest.

Choose tests you want to run.

Click "Settings" to change test's properties"""


class PsychTest(tk.Tk):


	def __init__(self, *args, **kwargs):


		tk.Tk.__init__(self, *args, **kwargs)

		#setting the name and logo of window
		basepath = os.path.dirname(__file__)
		imagepath = os.path.abspath(os.path.join(basepath, "..", "img",
			"brain_icon.ico"))

		tk.Tk.wm_title(self, "PsychTest")
		tk.Tk.iconbitmap(self, default=imagepath)

		#Container for frames to pop-up from stack
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		#Adding menubar with cascade for settings and 'About' window
		menubar = tk.Menu(container)

		#settings option in menu cascade
		mainmenu = tk.Menu(menubar, tearoff=0)
		mainmenu.add_command(
			label="Settings",
			command=lambda: self.showSettings())
		mainmenu.add_separator()

		#exit option in menu cascade
		mainmenu.add_command(label="Exit", command=lambda: self.quit_msg())
		menubar.add_cascade(label="Menu", menu=mainmenu)
		
		#about cascade
		menubar.add_command(
			label="About",
			command=lambda: self.show_about(ABOUT_DESCRIPTION))
		
		tk.Tk.config(self, menu=menubar)

		#variables for checkbuttons
		self.krep = tk.IntVar()
		self.stroop = tk.IntVar()
		self.rotation = tk.IntVar()

		#KRAEPELIN MODULE VARS
		self.krep_counter = 0
		self.krep_answer = tk.StringVar()
		self.krep_answer_total = []
		self.krep_good_answ = 0
		self.krep_bad_answ = 0
		self.krep_compare_total = []
		self.krep_time_stamps = []
		self.krep_time_start = float()
		self.krep_time_finish = float()

		#STROOP MODULE VARS
		self.stroop_counter = 0
		self.stroop_good_answ = 0
		self.stroop_bad_answ = 0
		self.stroop_start_time = float()
		self.stroop_finish_time = float()
		self.stroop_time_stamps = []
		self.stroop_time_stamps_cong = []
		self.stroop_time_stamps_noncong = []

		#ROTATION MODULE VARS
		self.rot_counter = 0
		self.rot_good_answ = 0
		self.rot_bad_answ = 0
		self.rot_angle_time = {x: [] for x in range(30, 331, 30)}
		self.rot_flip_angle_time = {x: [] for x in range(30, 331, 30)}
		self.rot_start_time = float()
		self.rot_stop_time = float()
		self.rot_merged_times = {}

		#default options of tests
		self.value_radio_cols = tk.IntVar()
		self.value_radio_cols.set(5)

		self.value_radio_nums = tk.IntVar()
		self.value_radio_nums.set(10)

		self.mode_stroop = tk.StringVar()
		self.mode_stroop.set('classic')

		self.type_rotation = tk.StringVar()
		self.type_rotation.set('letters')

		#Pack the other windows, as a classes, in a stack;
		#they are children of 'container' frame
		self.frames = {}

		for F, geometry in zip((
								StartPage,
								Kraepelin,
								KrepTest,
								KrepFinish,
								Stroop,
								StroopColor,
								StroopNumber,
								StroopFigural,
								StroopFinish,
								Rotation,
								RotationLetter,
								RotationFigure,
								RotationAnimal,
								RotationFinish,
								Summary,
							   ),
							   (
								'600x333',
								'495x333',
								'475x475',
								'475x475',
								'475x475',
								'475x475',
								'475x475',
								'475x475',
								'475x475',
								'475x475',
								'475x475',
								'475x475',
								'475x475',
								'475x475',
								'775x160',
							   )
							  ):
			page_name = F.__name__

			frame = F(container, self)

			self.frames[page_name] = (frame, geometry)

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame("StartPage")

		self.protocol("WM_DELETE_WINDOW", self.quit_msg)


	def show_frame(self, cont):


		"""Method to pop-up selected frame"""

		frame, geometry = self.frames[cont]
		self.update_idletasks()
		self.geometry(geometry)
		frame.tkraise()
		try:
			frame.postupdate()
		except AttributeError:
			pass


	def show_frame_handle(self):


		"""Method to choose proper starting experiment by program"""
		
		if self.krep.get() == 1:
			
			self.show_frame("Kraepelin")
		
		elif (self.stroop.get() == 1) & (self.krep.get() == 0):
			
			self.show_frame("Stroop")
		
		elif ((self.rotation.get() == 1)
			& (self.krep.get() == 0 & self.stroop.get() == 0)):
			
			self.show_frame("Rotation")
		

	@staticmethod
	def show_about(msg):


		"""Show separate 'about' window, where you can get more info about project"""

		about_frame = tk.Toplevel()
		about_frame.wm_title("About Project")

		#event to close toplevel window
		about_frame.bind("<Escape>", lambda f: about_frame.destroy())
		about_frame.focus_set()
		
		#info about test
		upper_frame = tk.Frame(about_frame)
		upper_frame.grid(row=0, column=0)

		about_label = ttk.Label(upper_frame, text=msg, font=NORMAL_FONT)
		about_label.grid(row=0, column=0, padx=5, pady=5)

		lower_frame = tk.Frame(about_frame)
		lower_frame.grid(row=1, column=0)

		#navbuttons for opening 'mailto:'' and github.com
		e_mail = ttk.Button(
			lower_frame, text="E-mail",
			command=lambda: PsychTest.send_mail("woj.warych@gmail.com"))
		e_mail.grid(row=0, column=0, padx=3, pady=3)

		git_hub = ttk.Button(
			lower_frame, text="Git Hub",
			command=lambda: PsychTest.git_browser("https://github.com/wojwarych"))
		git_hub.grid(row=0, column=1, padx=3, pady=3)
		
		#Get rid of minimize and maximize button
		#Disable resize the window by the user 
		about_frame.attributes("-toolwindow", 1)
		about_frame.resizable(0, 0)
		about_frame.geometry("300x300")
		about_frame.mainloop()


	@classmethod
	def git_browser(cls, url):
		

		"""Method to open browser with desired url"""

		return(webbrowser.open_new_tab(url))


	@classmethod
	def send_mail(cls, recipient):


		"""Method to open browser with 'mailto:'"""

		return(webbrowser.open("mailto:{}".format(recipient)))



	def quit_msg(self):


		"""Show window when quitting the whole app"""

		if messagebox.askokcancel("Quit",
			"Do you really wish to quit? All the results will be lost."):
			self.destroy()

	def showSettings(self):

	
		"""Separate window to tweak settings of tests"""

		settings_window = tk.Toplevel()
		settings_window.wm_title("Test Settings")

		#event to close window
		settings_window.bind("<Escape>", lambda f: settings_window.destroy())
		settings_window.focus_set()

		#create frame for settings of all tests
		settings_frame = tk.Frame(settings_window)
		settings_frame.grid(row=0, column=0, rowspan=4, columnspan=3)

		#frame for Kraepelin settings
		#title of test and proposed options
		krep_frame = tk.Frame(settings_frame)
		krep_frame.grid(row=0, column=0, rowspan=4, padx=2, pady=2)

		krep_name = ttk.Label(
			krep_frame, font=SMALL_FONT, text="KRAEPELIN TEST")
		krep_name.grid(row=0, column=0)

		krep_option1 = ttk.Label(
			krep_frame, font=SMALL_FONT, text="Number of columns:")
		krep_option1.grid(row=1, column=0)

		#frame for radiobutton with options to choose
		#variable to store number of columns
		cols_krep_grid = tk.Frame(krep_frame)
		cols_krep_grid.grid(row=2, column=0)

		self.value_radio_cols = tk.IntVar(cols_krep_grid)
		self.value_radio_cols.set(5)

		#create each radiobutton with option
		possible_num_cols = [
							 ('5', 5), ('10', 10), ('15', 15), ('20', 20),
							 ('25', 25)
							]
		for text, mode in possible_num_cols:
			num_cols = ttk.Radiobutton(
				cols_krep_grid, text=text, variable=self.value_radio_cols,
				value=mode, command=lambda: self.value_radio_cols.get())
			num_cols.pack(side='left')

		#option no. 2 - digits in one column
		krep_option2 = ttk.Label(
			krep_frame, font=SMALL_FONT, text="Digits in column:")
		krep_option2.grid(row=3, column=0)

		#frame for radiobutton with options to choose
		#variable to store number of columns
		cols_krep_grid2 = tk.Frame(krep_frame)
		cols_krep_grid2.grid(row=4, column=0)

		self.value_radio_nums = tk.IntVar(cols_krep_grid)
		self.value_radio_nums.set(10)

		#create each radiobutton with option
		possible_digits = [
						   ('10', 10), ('15', 15), ('20', 20), ('25', 25),
						   ('30', 30)
						  ]
		for text, mode in possible_digits:
			num_numbers = ttk.Radiobutton(
				cols_krep_grid2, text=text, variable=self.value_radio_nums,
				value=mode, command=lambda: self.value_radio_nums.get())
			num_numbers.pack(side='left')


		#frame for stroop test
		stroop_frame = tk.Frame(settings_frame)
		stroop_frame.grid(row=0, column=1, rowspan=3, padx=2, pady=2)

		#title of test
		#first option
		stroop_name = ttk.Label(
			stroop_frame, font=SMALL_FONT, text="STROOP TEST")
		stroop_name.grid(row=0, column=0)

		stroop_option1 = ttk.Label(
			stroop_frame, font=SMALL_FONT, text="Version of test:")
		stroop_option1.grid(row=1, column=0)

		#frame for radiobutton with options to choose
		#variable to choose version of test
		version_stroop_grid = tk.Frame(stroop_frame)
		version_stroop_grid.grid(row=2, column=0)

		self.mode_stroop = tk.StringVar(version_stroop_grid)
		self.mode_stroop.set('classic')


		#create each radiobutton with option (version)
		possible_versions = [
							 ('Classic', 'classic'), ('Numbers', 'numbers'),
							 ('Figural', 'figural')
							]
		for text, mode in possible_versions:
			version_stroop = ttk.Radiobutton(
				version_stroop_grid, text=text, variable=self.mode_stroop,
				value=mode, command=lambda: self.mode_stroop.get())
			version_stroop.pack(anchor='w')

		#frame for mental rotation
		rotation_frame = tk.Frame(settings_frame)
		rotation_frame.grid(row=0, column=2, rowspan=3, padx=2, pady=2)

		#title of test
		#first option
		rotation_name = ttk.Label(
			rotation_frame, font=SMALL_FONT, text="MENTAL ROTATION:")
		rotation_name.grid(row=0, column=0)

		rotation_option1 = ttk.Label(
			rotation_frame, font=SMALL_FONT, text="Type of test:")
		rotation_option1.grid(row=1, column=0)

		#frame for radiobutton with options to choose
		#variable to choose version of test
		type_rotation_grid = tk.Frame(rotation_frame)
		type_rotation_grid.grid(row=2, column=0)

		self.type_rotation = tk.StringVar(type_rotation_grid)
		self.type_rotation.set('letters')
		
		#create each radiobutton with option (version)
		possible_types = [
						  ('Letters', 'letters'), ('Figure', 'figure'),
						  ('Animal', 'animal')
						 ]
		for text, mode in possible_types:
			version_rotation = ttk.Radiobutton(
				type_rotation_grid, text=text, variable=self.type_rotation,
				value=mode, command=lambda: self.type_rotation.get())
			version_rotation.pack(anchor='w')

##############################################################################

if __name__ == "__main__":
	
	app = PsychTest()
	app.mainloop()