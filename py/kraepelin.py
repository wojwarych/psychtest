import tkinter as tk
from tkinter import ttk

from statistics import mean
import time
from random import randint, choice


#CONSTANS
LARGE_FONT = ("Verdana", 11)
SMALL_FONT = ("Verdana", 9)
KRAEP_DESCRIPTION = """Welcome to E-Kraepelin Test Version 0.1.
You are going to be shown a set of numbers between 0 to 9.
Your goal in this test is to count the sum of these numbers.
Next, type in your number and press enter.
The program counts your good and bad answers as well as time."""

thank_you_note = (
	"Thank you in participating in test.Click 'Next', to go further")

class Kraepelin(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.grid_rowconfigure(0, weight=2)
		self.controller = controller

		#description frame with label
		content_frame = tk.Frame(self)
		content_frame.grid(row=0, column=0)
		
		test_description = tk.Label(
			content_frame, font=LARGE_FONT, text=KRAEP_DESCRIPTION)
		test_description.grid(row=0, column=0)

		#frame for navigation button
		navigate_frame = tk.Frame(self)
		navigate_frame.grid(row=1, column=0)
		
		self.go_button = ttk.Button(
			navigate_frame, text="Go",
			command=lambda: self.controller.show_frame("KrepTest"))
		self.go_button.bind(
			"<Return>", lambda f: self.controller.show_frame("KrepTest"))
		self.go_button.grid(row=0, column=0, padx=15, pady=5)

		quit_button = ttk.Button(
			navigate_frame, text="Return",
			command=lambda: self.controller.show_frame("StartPage"))
		quit_button.grid(row=0, column=1, padx=15, pady=5)

		quit_button.bind(
			"<Return>",
			lambda f: self.controller.show_frame("StartPage"), "+")


	def postupdate(self):


		"""Function to change focus between classes-frames in controller"""
		
		self.go_button.focus()


class KrepTest(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)

		self.grid_columnconfigure(0, weight=2)
		self.controller = controller

		#Frame for text widget - "body" of kraepelin test
		#magic will happen there!
		text_frame = tk.Frame(self)
		text_frame.grid(row=0, column=0)
		
		self.text = tk.Text(
			text_frame, font=LARGE_FONT, width=25,bg="#F0F0F0", borderwidth=0)
		self.text.grid(row=0, column=0)

		#Insert introduction to the test and set text's properties
		self.text.insert('1.0', 10*'\n'+"Click 'Enter' to start the test")
		self.text.tag_configure("center", justify='center')
		self.text.tag_add("center", "1.0", tk.END)
		self.text['state'] = 'disabled'

		#frame for startbutton
		self.content_frame = tk.Frame(self)
		self.content_frame.grid(row=1, column=0)

		#startbutton to run test, binded to 'Enter' key
		self.startbutton = ttk.Button(
			self.content_frame, text="Start", command=lambda: self.one_test())
		
		self.startbutton.bind("<Return>", lambda f: self.one_test())
		self.startbutton.grid(row=0, column=0, padx=5, pady=5)

		self.return_button = ttk.Button(
			self.content_frame, text="Return",
			command=lambda: self.controller.show_frame("Kraepelin"))
		self.return_button.grid(row=0, column=1, padx=5, pady=5)

		self.return_button.bind(
			"<Return>",
			lambda f: self.controller.show_frame("Kraepelin"), "+")

	def postupdate(self):


		"""Method to get focus at the beginning"""
		
		self.startbutton.focus()


	def one_test(self):


		#Remove startbutton - no longer needed
		self.startbutton.destroy()
		self.return_button.destroy()

		#Run test units as long as it doesn't reach number of desired
		#shown columns
		if (self.controller.krep_counter
			< self.controller.value_radio_cols.get()):

			#enable change text in widget, delete, insert newlines
			#show fixation point and set properties
			self.text['state'] = 'normal'
			self.text.delete('1.0', tk.END)
			self.text.insert('1.0', 10*"\n"+"+")
			self.text.tag_add('center', '1.0', tk.END)
			self.text['state'] = 'disabled'
			
			#run one unit of test, after 3 secs of showing fix button
			self.text.after(3000, self.show_column)

			self.controller.krep_counter += 1

		else:
			self.check_value()
			self.controller.show_frame("KrepFinish")


	def show_column(self):


		#get column of numbers as a string in variable
		str_column = self.krep_test()
		#print(str_column)

		#enable change text in self.text widget in
		#order to insert str_column
		self.text['state'] = 'normal'

		self.text.delete('1.0', tk.END)
		self.text.insert('1.0', str_column)

		self.text.tag_add('center', '1.0', tk.END)

		self.text['state'] = 'disabled'

		#after putting new col start counting time
		#from showing col to event 'Enter' which stops timer
		#and sends value of self.controller.krep_answer
		self.start_count()

		self.entryvar = tk.Entry(
			self.content_frame, font=SMALL_FONT,
			textvariable=self.controller.krep_answer, justify=tk.CENTER,
			background="#F0F0F0", borderwidth=0, insertwidth=1)

		#clear entry for putting new value in new column
		self.entryvar.delete(0, tk.END)

		#go to method which stops counting time
		self.entryvar.bind("<Return>", lambda f: self.stop_count())
		self.entryvar.focus_set()

		self.entryvar.grid(row=0, column=1)

		#get sum of digits for further comparision and store them
		self.compare = sum(list(map(int, str_column.split())))
		self.controller.krep_compare_total.append(self.compare)


	def start_count(self):


		"""Start counting time when numbers appear"""
		
		self.controller.krep_time_start = time.time()


	def stop_count(self):


		"""Stop counting time after pressing button. Add time to list"""
		
		self.controller.krep_time_finish = (
			round(time.time() - self.controller.krep_time_start, 4))
		self.controller.krep_time_stamps.append(
			self.controller.krep_time_finish)

		#get inserted by the user value
		self.append_entry_answers()

		#get back to the body of test
		self.one_test()


	def append_entry_answers(self):


		"""Store value from self.entryvar in list for later comparison"""

		self.controller.krep_answer_total.append(
			int(self.controller.krep_answer.get()))


	def krep_test(self):


		"""Core of test - random numbers from 1 to 9 showed in column as a string"""
		
		column_str = ""
		column = ([randint(1,9) for num in
			range(self.controller.value_radio_nums.get())])
		
		for i, j in enumerate(column):
			column_str += str(column[i])
			column_str += "\n"

		return (column_str)


	def check_value(self):


		"""Check if value from showed column is equal to its
			self.controller.answer_krep"""
		
		for i, j in enumerate(self.controller.krep_compare_total):

			if (self.controller.krep_compare_total[i]
			== self.controller.krep_answer_total[i]):

				self.controller.krep_good_answ += 1

			else:
				self.controller.krep_bad_answ += 1


class KrepFinish(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)

		self.grid_columnconfigure(0, weight=2)
		self.controller = controller

		text_frame_finish = tk.Frame(self)
		text_frame_finish.grid(row=0, column=0)

		self.text_finish = tk.Text(
			text_frame_finish, font=LARGE_FONT, width=25,bg="#F0F0F0",
			borderwidth=0)
		self.text_finish.grid(row=0, column=0)
		finish_text = (10*'\n' + thank_you_note)
		self.text_finish.insert('1.0', finish_text)
		self.text_finish.tag_configure("center", justify='center')
		self.text_finish.tag_add("center", "1.0", tk.END)
		self.text_finish['state'] = 'disabled'

		nav_frame = tk.Frame(self)
		nav_frame.grid(row=1, column=0)

		self.navbutton = ttk.Button(
			nav_frame, text="Next", command=lambda: self.navigation())
		self.navbutton.bind("<Return>", lambda f: self.navigation())
		self.navbutton.grid(row=1, column=0, padx=5, pady=5)

		self.menubutton = ttk.Button(
			nav_frame, text="Menu",
			command=lambda: self.controller.show_frame("StartPage"))
		self.menubutton.bind(
			"<Return>",
			lambda f: self.controller.show_frame("StartPage"), "+")
		self.menubutton.grid(row=1, column=1, padx=5, pady=5)

	def postupdate(self):


		self.navbutton.focus()


	def navigation(self):


		if self.controller.stroop.get() == 1:

			self.controller.show_frame("Stroop")

		elif (self.controller.stroop.get() == 0 
			and self.controller.rotation.get() == 1):

			self.controller.show_frame("Rotation")

		elif (self.controller.stroop.get()
			and self.controller.rotation.get()) == 0:

			self.controller.show_frame("Summary")