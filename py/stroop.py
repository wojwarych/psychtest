import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

import random
import time

#constans
LARGE_FONT = ("Verdana", 11)
NORMAL_FONT = ("Verdana", 10)

STROOP_ENTRANCE = 5*'\n'+'STROOP TEST'
STROOP_COLOR = """You will see two words describing colours
(e.g. 'blue', 'red') in different font colours. If the meaning of
the word and colour of the font are the same, press left arrow key.
Otherwise, click right arrow key."""
STROOP_NUMBERS = """You will see two numbers in different font sizes.
If one's number value and font size are greater than the other number
value and size - press left arrow key. Otherwise, click right arrow key."""
STROOP_FIGURAL = "Choose wether the figure is made of the same words\nas the figure."
thank_you_note = (
	"Thank you in participating in test. Click 'Next', to go further")


class Stroop(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.controller = controller

		#set sizes of window
		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)


		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		#description label
		descrip_lab = tk.Label(
			self.descrip_frame, text="STROOP TEST",
			font=LARGE_FONT, justify='center')
		descrip_lab.grid(row=0, column=0)
		
		#navigation buttons
		buttonframe = tk.Frame(self)
		buttonframe.grid(row=1, column=0)

		self.nextbut = ttk.Button(
			buttonframe, text="Next >",
			command=lambda: self.navigate_stroop())
		self.nextbut.bind("<Return>", lambda f: self.navigate_stroop())
		self.nextbut.grid(row=0, column=0, padx=15, pady=5)

		self.returnbut = ttk.Button(buttonframe, text="Return",
			command=lambda: self.controller.show_frame("StartPage"))
		self.returnbut.bind("<Return>",
			lambda f: self.controller.show_frame("StartPage"), "+")
		self.returnbut.grid(row=0, column=1, padx=15, pady=5)


	def postupdate(self):


		self.nextbut.focus()


	def navigate_stroop(self):


		if self.controller.mode_stroop.get() == 'classic':
			self.controller.show_frame("StroopColor")

		elif self.controller.mode_stroop.get() == 'numbers':
			self.controller.show_frame("StroopNumber")

		else:
			self.controller.show_frame("StroopFigural")



class StroopColor(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.grid_columnconfigure(0, weight=2)
		
		self.controller = controller

		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)


		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		#description label
		descrip_lab = tk.Label(
			self.descrip_frame, text=STROOP_COLOR,
			font=NORMAL_FONT, justify='center')
		descrip_lab.grid(row=0, column=0)
		
		#navigation buttons
		self.buttonframe = tk.Frame(self)
		self.buttonframe.grid(row=1, column=0)

		self.nextbut = ttk.Button(
			self.buttonframe, text="Next >",
			command=lambda: self.test_window())
		self.nextbut.bind("<Return>", lambda f: self.test_window())
		self.nextbut.grid(row=0, column=0, padx=15, pady=5)

		self.returnbut = ttk.Button(self.buttonframe, text="Return",
			command=lambda: self.controller.show_frame("Stroop"))
		self.returnbut.bind("<Return>",
			lambda f: self.controller.show_frame("Stroop"), "+")
		self.returnbut.grid(row=0, column=1, padx=15, pady=5)


	def postupdate(self):


		"""override tkraise in controller"""
		self.nextbut.focus()
		

	def test_window(self):


		#remove description of test and nav buttons from view
		self.descrip_frame.grid_remove()
		self.buttonframe.grid_remove()

		#frame for experiment's text
		text_color_frame = tk.Frame(self)
		text_color_frame.grid(row=0, column=0)

		self.text_color = tk.Text(
			text_color_frame, font=LARGE_FONT, width=25, bg="#F0F0F0",
			borderwidth=0)
		self.text_color.grid(row=0, column=0)

		#starting experiment
		self.text_color.insert('1.0', 10*'\n'+"Click 'Enter' to start the test")
		
		self.text_color.tag_configure("center", justify='center')
		self.text_color.tag_add("center", "1.0", tk.END)
		
		self.text_color['state'] = 'disabled'

		self.nav_button = ttk.Button(
			text_color_frame, text="Start", command=lambda: self.color_test())
		self.nav_button.grid(row=1, column=0)

		self.nav_button.bind("<Return>", lambda f: self.color_test(), "+")
		self.nav_button.focus_set()


	def color_test(self, the_number=5):


		#remove start button from the view
		self.nav_button.grid_remove()

		#bigger font in self.text_color for fixation point
		self.fixation_font = Font(family='Verdana', size=18)
		self.text_color.tag_configure('fix_big', font=self.fixation_font)

		if self.controller.stroop_counter < the_number:
			#delete previous text from widget
			self.text_color['state'] = 'normal'
			
			self.text_color.delete('1.0', tk.END)
			self.text_color.insert('1.0', 6*"\n"+"+")
			
			#justify and make bigger font for fixation point
			self.text_color.tag_add("center", "1.0", tk.END)
			self.text_color.tag_add('fix_big', '1.0', tk.END)
			
			self.text_color['state'] = 'disabled'
			
			#show after 3 secs coloured word
			self.text_color.after(3000, self.random_word)

			self.controller.stroop_counter += 1

		else:
			self.controller.show_frame("StroopFinish")


	def random_word(self):


		#get word from this function
		self.random_choice()

		self.text_color['state'] = 'normal'
		
		#delete fixation point and add word from self.random_choice()
		self.text_color.delete('1.0', tk.END)
		self.text_color.insert('1.0', 10*"\n"+self.the_string)
		
		#set its properties - color, font, justify
		self.text_color.tag_add('center', '1.0', tk.END)
		self.text_color.tag_add('COLOR', '1.0', tk.END)
		self.text_color['state'] = 'disabled'

		self.start_count()
		
		#event handling for correct/wrong answer
		self.text_color.bind("<Left>", lambda f: self.arrow_left())
		self.text_color.bind("<Right>", lambda f: self.arrow_right())
		self.text_color.focus_set()


	def random_choice(self):


		#colours and words to choose from
		colour = {
				  'blue':'#0f52ba', 'green':'#92c544', 'yellow':'#fec611',
				  'red':'#d41c1c'
				 }
		string_type = ['blue', 'green', 'yellow', 'red']

		#get random word from list and random colour from dict
		#self.check gets key from dict for arrow_up() and arrown_down()
		#to check correct answer
		self.the_string = random.choice(string_type)
		self.check, self.the_colour = random.choice(list(colour.items()))

		#bigger font in self.text_color for words themselves
		self.word_font = Font(family='Verdana', size=12, weight='bold')
		self.text_color.tag_configure(
			'COLOR', foreground=self.the_colour, font=self.word_font)


	def arrow_left(self):


		#if color and meaning is congruent and
		#user pressed arrow left -> good answer; else - bad answer
		if self.the_string == self.check:
			self.controller.stroop_good_answ += 1

		else:
			self.controller.stroop_bad_answ += 1

		#return to function, to delete word and
		#create fixation point again
		self.stop_count()


	def arrow_right(self):


		#if color and meaning is not congruent and
		#user pressed arrown right -> good answer; else - bad answer
		if self.the_string != self.check:
			self.controller.stroop_good_answ += 1

		else:
			self.controller.stroop_bad_answ += 1

		#return to function, to delete word and create
		#fixation point again
		self.stop_count()


	def start_count(self):


		self.controller.stroop_start_time = time.time()


	def stop_count(self):

		"""Stop counting time after user's click"""

		#store time to list - congruent or not - and to common list

		if self.the_string == self.check:
			self.controller.stroop_finish_time = (round(time.time()
				- self.controller.stroop_start_time, 4))

			self.controller.stroop_time_stamps.append(
				self.controller.stroop_finish_time)

			self.controller.stroop_time_stamps_cong.append(
				self.controller.stroop_finish_time)

		else:
			self.controller.stroop_finish_time = (round(time.time()
				- self.controller.stroop_start_time, 4))
			
			self.controller.stroop_time_stamps.append(
				self.controller.stroop_finish_time)
			
			self.controller.stroop_time_stamps_noncong.append(
				self.controller.stroop_finish_time)

		#back to body of function
		self.color_test()


class StroopNumber(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.controller = controller

		self.grid_rowconfigure(0, weight=2)
		self.grid_columnconfigure(0, weight=2)
		
		self.controller = controller

		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)


		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		#label for description of test
		descrip_lab = tk.Label(
			self.descrip_frame, text=STROOP_NUMBERS, font=NORMAL_FONT,
			justify='center')
		descrip_lab.grid(row=0, column=0)
		
		#navigation buttons
		self.buttonframe = tk.Frame(self)
		self.buttonframe.grid(row=1, column=0)

		self.nextbut = ttk.Button(
			self.buttonframe, text="Next >",
			command=lambda: self.test_window())
		self.nextbut.bind("<Return>", lambda f: self.test_window())
		self.nextbut.grid(row=0, column=0, padx=15, pady=5)

		self.returnbut = ttk.Button(self.buttonframe, text="Return",
			command=lambda: self.controller.show_frame("Stroop"))
		self.returnbut.bind("<Return>",
			lambda f: self.controller.show_frame("Stroop"), "+")
		self.returnbut.grid(row=0, column=1, padx=15, pady=5)


	def postupdate(self):

		"""Get starting focus for this experiment"""
		self.nextbut.focus()


	def test_window(self):


		#remove description of test and nav buttons from view
		self.descrip_frame.grid_remove()
		self.buttonframe.grid_remove()

		#frame for experiment's text
		number_frame = tk.Frame(self)
		number_frame.grid(row=0, column=0)

		self.numbers = tk.Text(
			number_frame, font=LARGE_FONT, width=25, bg="#F0F0F0",
			borderwidth=0)
		self.numbers.grid(row=0, column=0)

		#starting experiment
		self.numbers.insert('1.0', 10*'\n'+"Click 'Enter' to start the test")
		
		self.numbers.tag_configure("center", justify='center')
		self.numbers.tag_add("center", "1.0", tk.END)
		
		self.numbers['state'] = 'disabled'

		self.nav_button = ttk.Button(
			number_frame, text="Start", command=lambda: self.numbers_test())
		self.nav_button.grid(row=1, column=0)
		
		self.nav_button.bind("<Return>", lambda f: self.numbers_test())
		self.nav_button.focus_set()


	def numbers_test(self, the_number=5):


		#remove start button from the view
		self.nav_button.grid_remove()

		#bigger font in self.text_color for fixation point
		self.fixation_font = Font(family='Verdana', size=18)
		self.numbers.tag_configure('fix_big', font=self.fixation_font)

		if self.controller.stroop_counter < the_number:

			#delete previous text from widget
			self.numbers['state'] = 'normal'
			
			self.numbers.delete('1.0', tk.END)
			self.numbers.insert('1.0', 6*"\n"+"+")
			
			#justify and make bigger font for fixation point
			self.numbers.tag_add("center", "1.0", tk.END)
			self.numbers.tag_add('fix_big', '1.0', tk.END)
			
			self.numbers['state'] = 'disabled'
			
			#show after 3 secs coloured word
			self.numbers.after(3000, self.random_num)

			self.controller.stroop_counter += 1

		else:

			#end experiment
			self.controller.show_frame("StroopFinish")


	def random_num(self):


		#get word from this function
		self.random_choice()

		self.numbers['state'] = 'normal'
		
		#delete fixation point and add first digit
		#from self.random_choice()
		self.numbers.delete('1.0', tk.END)
		self.numbers.insert('1.0', 10*'\n')
		self.numbers.insert('11.0', str(self.first_num)+"     ")
		
		#set its properties - fontsize, justify
		self.numbers.tag_add('center', '1.0', tk.END)
		self.numbers.tag_add('first_font', '11.0', '11.end')

		#add second digit from self.random_choice()
		self.numbers.insert('first_font.last', str(self.second_num))
		
		#set its properties - fontsize, justify
		self.numbers.tag_add('second_font', 'first_font.last', tk.END)
		
		self.numbers['state'] = 'disabled'

		self.start_count()

		#event handling for correct/wrong answer
		self.numbers.bind("<Left>", lambda f: self.arrow_left())
		self.numbers.bind("<Right>", lambda f: self.arrow_right())
		self.numbers.focus_set()


	def random_choice(self):


		#get two non-identical numbers from 1 to 100 and assign them
		selection = random.sample(range(1, 100), k=2)

		self.first_num = selection[0]
		self.second_num = selection[1]

		#random choice of fontsize for both numbers
		self.sizes = [12, 18]
		random.shuffle(self.sizes)

		#create tag-fonts for numbers to change its properites
		first_font = Font(family='Verdana', size=self.sizes[0])
		second_font = Font(family='Verdana', size=self.sizes[1])

		self.numbers.tag_configure('first_font', font=first_font)
		self.numbers.tag_configure('second_font', font=second_font)


	def arrow_left(self):


		#if number values and sizes are congruent and
		#user pressed arrow left -> good answer; else: wrong

		if ((self.first_num > self.second_num
			and self.sizes[0] > self.sizes[1]
		or self.first_num < self.second_num
			and self.sizes[0] < self.sizes[1])):
			
			self.controller.stroop_good_answ += 1

		else:

			self.controller.stroop_bad_answ += 1

		#return to function, to delete numbers
		#and create fixation point again
		self.stop_count()


	def arrow_right(self):


		#if number values and sizes are not congruent and
		#user pressed arrown down -> good answer; else: wrong

		if (self.first_num > self.second_num
			and self.sizes[0] < self.sizes[1]
		or self.first_num < self.second_num
			and self.sizes[0] > self.sizes[1]):
			
			self.controller.stroop_good_answ += 1

		else:

			self.controller.stroop_bad_answ += 1

		#return to function, to delete number
		#and create fixation point again
		self.stop_count()


	def start_count(self):


		#start counting time when numbers are shown
		self.controller.stroop_start_time = time.time()


	def stop_count(self):


		#stop counting time after user's choice
		#add time to proper lists (depending on congruency)

		if ((self.first_num > self.second_num
			and self.sizes[0] > self.sizes[1])
		or (self.first_num < self.second_num
			and self.sizes[0] < self.sizes[1])):

			self.controller.stroop_finish_time = (round(time.time()
				- self.controller.stroop_start_time, 4))

			self.controller.stroop_time_stamps.append(
				self.controller.stroop_finish_time)

			self.controller.stroop_time_stamps_cong.append(
				self.controller.stroop_finish_time)

		else:

			self.controller.stroop_finish_time = (round(time.time()
				- self.controller.stroop_start_time, 4))

			self.controller.stroop_time_stamps.append(
				self.controller.stroop_finish_time)

			self.controller.stroop_time_stamps_noncong.append(
				self.controller.stroop_finish_time)

		#back to the body of test
		self.numbers_test()

#TODO: functionalities for StroopFigural
class StroopFigural(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.controller = controller

		self.grid_rowconfigure(0, weight=2)
		self.grid_columnconfigure(0, weight=2)
		
		self.controller = controller

		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)


		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		#description label
		descrip_lab = tk.Label(
			self.descrip_frame, text=STROOP_FIGURAL, font=LARGE_FONT,
			justify='center')
		descrip_lab.grid(row=0, column=0)
		
		#navigation buttons
		self.buttonframe = tk.Frame(self)
		self.buttonframe.grid(row=1, column=0)

		self.nextbut = ttk.Button(
			self.buttonframe, text="Next >",
			command=lambda: self.test_window())
		self.nextbut.bind("<Return>", lambda f: self.test_window())
		self.nextbut.grid(row=0, column=0, padx=15, pady=5)

		self.quitbut = ttk.Button(
			self.buttonframe, text="Quit", command=lambda: quit())
		self.quitbut.bind("<q>", lambda f: quit())
		self.quitbut.grid(row=0, column=1, padx=15, pady=5)


class StroopFinish(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)

		self.grid_columnconfigure(0, weight=2)
		self.controller = controller

		text_frame_finish = tk.Frame(self)
		text_frame_finish.grid(row=0, column=0)

		self.text_finish = tk.Text(text_frame_finish, font=LARGE_FONT,
			width=25, bg="#F0F0F0", borderwidth=0)
		self.text_finish.grid(row=0, column=0)
		finish_text = (10*'\n' + thank_you_note)
		self.text_finish.insert('1.0', finish_text)
		self.text_finish.tag_configure("center", justify='center')
		self.text_finish.tag_add("center", "1.0", tk.END)
		self.text_finish['state'] = 'disabled'

		nav_frame = tk.Frame(self)
		nav_frame.grid(row=1, column=0)

		self.navbutton = ttk.Button(nav_frame, text="Next",
			command=lambda: self.navigation())
		self.navbutton.bind("<Return>",
			lambda f: self.navigation())
		self.navbutton.grid(row=1, column=0, padx=5, pady=5)

		self.menubutton = ttk.Button(nav_frame, text="Menu",
			command=lambda: self.controller.show_frame("StartPage"))
		self.menubutton.bind("<Return>",
			lambda f: self.controller.show_frame("StartPage"), "+")
		self.menubutton.grid(row=1, column=1, padx=5, pady=5)


	def postupdate(self):


		self.navbutton.focus()


	def navigation(self):


		if self.controller.rotation.get() == 1:

			self.controller.show_frame("Rotation")

		else:

			self.controller.show_frame("Summary")