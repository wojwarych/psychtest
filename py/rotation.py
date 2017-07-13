#TODO: fix the problem with non-transparent background for RotationFigure class

import tkinter as tk
from tkinter import ttk

import os.path
from PIL import Image, ImageTk, ImageOps
import random
import time

SUPER_LARGE = ("Verdana", 16)
LARGE_FONT = ("Verdana", 11)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 9)

ROTATION_INTRO = "MENTAL ROTATION TEST"
ROTATION_LETTER = """You're about to shown two letters.
Your task is to decide whether the letter on the left is the same
or flipped. If you think that the letter is flipped, press left arrow key.
Otherwise, press right arrow key."""
ROTATION_ANIM = """You're about to shown two images of an animal.
Your task is to decide whether the image on the left is the same
or flipped. If you think that the image is flipped, press left arrow key.
Otherwise, press right arrow key."""
ROTATION_FIGURE = """You're about to shown two figures.
Your task is to decide whether the figure on the left is the same
or flipped. If you think that the figure is flipped, press left arrow key.
Otherwise, press right arrow key."""
thank_you_note = (
	"Thank you in participating in test. Click 'Next', to go further")


class Rotation(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)

		#title of test
		descrip_frame = tk.Frame(self)
		descrip_frame.grid(row=0, column=0)

		descrip_text = tk.Label(
			descrip_frame, text=ROTATION_INTRO, font=LARGE_FONT,
			justify='center')
		descrip_text.grid(row=0, column=0)
		
		#buttons to navigate through module
		buttonframe = tk.Frame(self)
		buttonframe.grid(row=1, column=0)

		self.nextbut = ttk.Button(
			buttonframe, text="Next", command=lambda: self.test_handler())
		self.nextbut.grid(row=0, column=0, padx=15, pady=5)
		self.nextbut.bind("<Return>", lambda f: self.test_handler())
		
		returnbut = ttk.Button(buttonframe, text="Return",
			command=lambda: self.controller.show_frame("StartPage"))
		returnbut.grid(row=0, column=1, padx=15, pady=5)
		returnbut.bind(
			"<Return>",
			lambda f: self.controller.show_frame("StartPage"), "+")


	def postupdate(self):


		"""Get starting focus in module"""

		self.nextbut.focus_set()


	def test_handler(self):


		"""Navigate through different types of experiment"""

		if self.controller.type_rotation.get() == 'letters':

			self.controller.show_frame("RotationLetter")

		elif self.controller.type_rotation.get() == 'animal':

			self.controller.show_frame("RotationAnimal")

		elif self.controller.type_rotation.get() == 'figure':

			self.controller.show_frame("RotationFigure")

class RotationLetter(tk.Frame):

#TODO: STORE ANSWERS FOR THE EACH ANGLE

	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)
		self.create_widgets()


	def create_widgets(self):
		
		try:

			#destroy useless widgets if you went back to beginning
			#of class
			self.start_test.destroy()
			self.buttonframe.destroy()

		except:
			pass


		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		#description of version
		self.descrip_text = tk.Label(
			self.descrip_frame, text=ROTATION_LETTER,
			font=NORMAL_FONT, justify='center')
		self.descrip_text.grid(row=0, column=0)
		
		#buttons to go through the test with bidings
		self.buttonframe = tk.Frame(self)
		self.buttonframe.grid(row=1, column=0)

		self.startbut = ttk.Button(
			self.buttonframe, text="Start",
			command=lambda: self.start_window())
		self.startbut.grid(row=0, column=0, padx=15, pady=5)
		self.startbut.bind("<Return>", lambda f: self.start_window())
		self.startbut.focus_set()

		self.returnbut = ttk.Button(
			self.buttonframe, text="Return",
			command=lambda: self.controller.show_frame("Rotation"))
		self.returnbut.grid(row=0, column=1, padx=15, pady=5)
		self.returnbut.bind(
			"<Return>",
			lambda f: self.controller.show_frame("Rotation"), "+")

		#choose the letter
		self.generate_image()


	def postupdate(self):


		"""Get focus for the first button"""

		self.startbut.focus_set()


	def start_window(self):


		"""Prepare window for the test"""
		
		#remove description of test
		self.descrip_text.destroy()

		#text to start experiment
		self.start_test = tk.Label(
			self.descrip_frame, text="Click 'Enter' to start the test",
			font=LARGE_FONT, justify='center')
		self.start_test.grid(row=0, column=0)
		
		#change functions of buttons to go further the experiment	
		self.startbut['command'] = lambda: self.test_window()
		self.startbut.bind("<Return>", lambda f: self.test_window())
		self.startbut.focus_set()

		self.returnbut['command'] = lambda: self.create_widgets()
		self.returnbut.bind("<Return>", lambda f: self.create_widgets())


	def test_window(self, the_number=100):


		"""Body of experiment"""

		#remove useless widgets
		self.start_test.destroy()
		self.buttonframe.destroy()

		
		if self.controller.rot_counter < the_number:

			#create fixation point
			self.fix_point = tk.Label(
				self.descrip_frame, text="+", font=SUPER_LARGE, justify='center')
			self.fix_point.grid(row=0, column=0)

			#remove fix point after 3 secs and show letters
			self.fix_point.after(3000, self.pick_letters)

			self.controller.rot_counter += 1

		else:

			#merged dict for summary purposes
			self.merge_dicts()
			self.controller.show_frame("RotationFinish")


	def arrow_left(self):

		
		"""Stores the answer if user clicked left arrow key"""
		
		#stop counting time of reaction
		#store the reaction time to proper dicts
		self.stop_count()
		self.collect_answers()


		#if letter is flipped - good answer; either - bad
		if self.made_decision == 1:

			self.controller.rot_good_answ += 1

		else:

			self.controller.rot_bad_answ += 1

		self.clear_window()


	def arrow_right(self):


		"""Stores the answer if user clicked right arrow key"""
		
		#stop counting time of reaction
		#store the reaction time to proper dicts
		self.stop_count()
		self.collect_answers()

		#if letter is not flipped - good answer; either - bad
		if self.made_decision == 0:

			self.controller.rot_good_answ += 1

		else:

			self.controller.rot_bad_answ += 1

		self.clear_window()


	def clear_window(self):


		"""Remove previous images and go back to body of experiment"""

		self.descrip_text.grid_remove()
		self.descrip_text2.grid_remove()
		self.test_window()


	def dict_of_letters(self):


		"""Create dict of paths to images of letters"""

		letters = ('F', 'G', 'J')
		self.dict_letters = {}
		basepath = os.path.dirname(__file__)

		for num, word in enumerate(letters):

			imagepath = os.path.abspath(
				os.path.join(basepath, '..', 'img', letters[num]+'.png'))

			self.dict_letters[letters[num]] = imagepath

	
	def pick_random_letter(self):


		""""Choice random letter from created dict"""

		self.dict_of_letters()		
		self.random_letter = random.choice(list(self.dict_letters.values()))


	def generate_image(self):


		"""Create image to work on"""

		self.pick_random_letter()
		pic = Image.open(self.random_letter)
		self.work_pic = pic


	def pick_letters(self):


		"""Assign prepared images to variables and show in frame"""

		#decide whether the image1 will be flipped or not
		#create letters
		self.made_decision = self.flip_decision()
		image1 = self.rotate_letter(self.work_pic)
		image1 = self.make_imagetk(image1)
		image2 = self.make_imagetk(self.work_pic)

		#show letters
		self.descrip_text = tk.Label(self.descrip_frame, image=image1)
		self.descrip_text.image = image1
		self.descrip_text.grid(row=0, column=0, pady=15, padx=15)

		self.descrip_text2 = tk.Label(self.descrip_frame, image=image2)
		self.descrip_text2.image = image2
		self.descrip_text2.grid(row=0, column=1, pady=15, padx=15)

		#start counting time of reaction after showing letters
		self.start_count()
		
		self.descrip_text.bind("<Left>", lambda f: self.arrow_left())
		self.descrip_text.bind("<Right>", lambda f: self.arrow_right(), "+")
		self.descrip_text.focus_set()


	def start_count(self):


		"""Start counting time from showing images"""

		self.controller.rot_start_time = time.time()


	def stop_count(self):


		"""Stop counting time after user's reaction"""

		self.controller.rot_stop_time = (round(time.time()
			- self.controller.rot_start_time, 4))


	def flip_decision(self):


		"""Choose if image1 should be flipped horrizontally or not"""

		return(random.getrandbits(1))


	def flip_image(self, image):


		"""Flip horrizontally image"""

		return(ImageOps.mirror(image))


	def make_imagetk(self, image):


		"""Make image availabale to show for tkinter"""

		return(ImageTk.PhotoImage(image))


	def pre_rotate(self, image):


		"""Prepare image so after rotation
			it still has transparent background"""

		image_work = image.convert('RGBA')
		return(image_work)


	def rotate_letter(self, image):

		
		"""Rotate image at specific angle and flip if True"""

		#create list of possible angles
		angles = [i for i in range (30, 331, 30)]
		#assign to attribute - it'll be used later to create dicts
		self.chosen_angle = random.choice(angles)
		
		#make background transparent for image and rotate it
		im2 = self.pre_rotate(image)
		rot = im2.rotate(self.chosen_angle, expand=1)

		#flip image if true
		if self.made_decision == True:
			
			rot_flip = self.flip_image(rot)
			return(rot_flip)
		
		else:
			
			return(rot)


	def collect_answers(self):


		"""Assign time reaction to proper dict"""

		#if image flipped - assign to flipped dict
		#else to not flipped, assign to proper key-angle in dict
		#by checking chosen angle
		if self.made_decision == 1:

			for key in self.controller.rot_flip_angle_time:
				
				if self.chosen_angle == key:
					(self.controller.rot_flip_angle_time[key].
						append(self.controller.rot_stop_time))
				
				else:
					pass

		else:

			for key in self.controller.rot_angle_time:
				
				if self.chosen_angle == key:
					(self.controller.rot_angle_time[key].
						append(self.controller.rot_stop_time))
				
				else:
					pass


	def merge_dicts(self):


		"""Create common dict to show later in summary"""

		dict_list = [self.controller.rot_angle_time,
			self.controller.rot_flip_angle_time]

		for item in dict_list:

			for key, value in item.items():

				(self.controller.rot_merged_times.
					setdefault(key, []).extend(value))


class RotationFigure(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)
		self.create_widgets()
		
		#fetch the image
		self.image_path()
		#generate figure to rotate it later
		self.generate_image()


	def create_widgets(self):


		try:

			#destroy useless widgets if you went back to beginning
			#of class
			self.start_test.destroy()
			self.buttonframe.destroy()

		except:
			pass

		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		self.descrip_text = tk.Label(
			self.descrip_frame, text=ROTATION_FIGURE, font=NORMAL_FONT,
			justify='center')
		self.descrip_text.grid(row=0, column=0)
		
		#navigation through the class
		self.buttonframe = tk.Frame(self)
		self.buttonframe.grid(row=1, column=0)

		self.startbut = ttk.Button(
			self.buttonframe, text="Start",
			command=lambda: self.start_window())
		self.startbut.grid(row=0, column=0, padx=15, pady=5)
		self.startbut.bind("<Return>", lambda f: self.start_window())
		self.startbut.focus_set()

		self.returnbut = ttk.Button(
			self.buttonframe, text="Return",
			command=lambda: self.controller.show_frame("Rotation"))
		self.returnbut.grid(row=0, column=1, padx=15, pady=5)
		self.returnbut.bind(
			"<Return>",
			lambda f: self.controller.show_frame("Rotation"), "+")


	def start_window(self):

		#destroy the description of the version
		self.descrip_text.destroy()

		#descrip to start, change functions binded
		#to navigation buttons
		self.start_descrip = tk.Label(
			self.descrip_frame, text="Click 'Enter' to start the test",
			font=LARGE_FONT, justify='center')
		self.start_descrip.grid(row=0, column=0)

		self.startbut['command'] = lambda: self.test_window()
		self.startbut.bind("<Return>", lambda f: self.test_window())
		self.startbut.focus_set()

		self.returnbut['command'] = lambda: self.create_widgets()
		self.returnbut.bind("<Return>", lambda f: self.create_widgets(), "+")


	def postupdate(self):


		"""Get focus for the first button"""

		self.startbut.focus_set()


	def test_window(self, the_number=100):

		#destroy useless widgets so they don't still apppear in frame
		self.start_descrip.destroy()
		self.buttonframe.destroy()

		if self.controller.rot_counter < the_number:

			#create fixation point
			self.fix_point = ttk.Label(
				self.descrip_frame, text="+", font=SUPER_LARGE,
				justify='center')
			self.fix_point.grid(row=0, column=0)

			#after 3 secs show created figures
			self.fix_point.after(3000, self.show_figure)

			self.controller.rot_counter += 1

		else:

			#merge dicts for flipped and not flipped figures
			self.merge_dicts()
			self.controller.show_frame("RotationFinish")


	def show_figure(self):


		#decide whether flip the figure or not
		#create figures
		self.made_decision = self.flip_decision()
		image1 = self.rotate_image(self.work_pic)
		image1 = self.make_imagetk(image1)
		image2 = self.make_imagetk(self.work_pic)

		#show figures
		self.rotated_img = tk.Label(self.descrip_frame, image=image1)
		self.rotated_img.image = image1
		self.rotated_img.grid(row=0, column=0, padx=15, pady=15)

		self.fixed_img = tk.Label(self.descrip_frame, image=image2)
		self.fixed_img.image = image2
		self.fixed_img.grid(row=0, column=1, padx=15, pady=15)

		#figures are shown - count time of the reaction
		self.start_count()

		self.rotated_img.bind("<Left>", lambda f: self.arrow_left())
		self.rotated_img.bind("<Right>", lambda f: self.arrow_right())
		self.rotated_img.focus_set()


	def image_path(self):


		figure = '2dfigure2'
		basepath = os.path.dirname(__file__)

		self.imagepath = os.path.abspath(
				os.path.join(basepath, '..', 'img', figure+'.png'))


	def generate_image(self):


		"""Create figure to work with"""

		self.work_pic = Image.open(self.imagepath)
		#alpha-layer for transparency
		self.work_pic = self.work_pic.convert('RGBA')


	def make_imagetk(self, image):


		"""Make the image able to show in tk.Label"""

		return(ImageTk.PhotoImage(image))


	def rotate_image(self, image):


		# angle != 180 since flipped image in 180 degrees
		#looks the same as not flipped
		angles = [angle for angle in range(30, 331, 30) if angle != 180]

		self.chosen_angle = random.choice(angles)

		#return flipped image if decision == 1; else only rotated
		if self.made_decision == True:

			im_final = image.rotate(self.chosen_angle, expand=1)
			im_final = self.make_flip(im_final)
			return(im_final)

		else:

			im_final = image.rotate(self.chosen_angle, expand=1)
			return(im_final)


	@staticmethod
	def flip_decision():


		"""Random selection if the figure will be flipped"""

		return(random.getrandbits(1))


	@staticmethod
	def make_flip(image):


		"""Flip vertically image"""

		return(ImageOps.mirror(image))


	def start_count(self):


		"""Start counting the reaction of user"""

		self.controller.rot_start_time = time.time()


	def stop_count(self):


		"""Stop counting reaction of user after his action"""

		self.controller.rot_stop_time = (round(time.time()
			- self.controller.rot_start_time, 4))


	def arrow_left(self):


		"""Collect data when clicked arrow left"""

		#stop counting and collect answer to proper dicts
		self.stop_count()
		self.collect_answers()

		#if figure was flipped - good answer; else - bad;
		if self.made_decision == 1:

			self.controller.rot_good_answ += 1

		else:

			self.controller.rot_bad_answ += 1


		self.clear_window()


	def arrow_right(self):


		"""Collect data when clicked arrow left"""

		#stop counting and collect answer to proper dicts
		self.stop_count()
		self.collect_answers()

		#if figure was not flipped - good answer; else - bad
		if self.made_decision == 0:

			self.controller.rot_good_answ += 1

		else:

			self.controller.rot_bad_answ += 1

		self.clear_window()


	def clear_window(self):


		self.rotated_img.grid_remove()
		self.fixed_img.grid_remove()

		self.test_window()


	def collect_answers(self):


		"""Assign time reaction to proper dict"""

		#if image flipped - assign to flipped dict
		if self.made_decision == 1:

			for key in self.controller.rot_flip_angle_time:
				
				if self.chosen_angle == key:
					(self.controller.rot_flip_angle_time[key].
						append(self.controller.rot_stop_time))
				
				else:
					pass

		else:

			for key in self.controller.rot_angle_time:
				
				if self.chosen_angle == key:
					(self.controller.rot_angle_time[key].
						append(self.controller.rot_stop_time))
				
				else:
					pass


	def merge_dicts(self):


		"""Create common dict to show later in summary"""

		dict_list = [self.controller.rot_angle_time,
			self.controller.rot_flip_angle_time]

		for item in dict_list:

			for key, value in item.items():

				(self.controller.rot_merged_times.
					setdefault(key, []).extend(value))


class RotationAnimal(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.grid_rowconfigure(0, weight=2, minsize=317)
		self.grid_columnconfigure(0, minsize=475)
		self.create_widgets()
		self.image_path()
		self.generate_image()


	def create_widgets(self):

		try:
			
			#destroy useless widgets if you went back to beginning
			#of class
			self.descrip_frame.destroy()
			self.buttonframe.destroy()

		except:

			pass


		self.descrip_frame = tk.Frame(self)
		self.descrip_frame.grid(row=0, column=0)

		self.descrip_text = tk.Label(
			self.descrip_frame, text=ROTATION_ANIM, font=NORMAL_FONT,
			justify='center')
		self.descrip_text.grid(row=0, column=0)
		
		#navigation through the class
		self.buttonframe = tk.Frame(self)
		self.buttonframe.grid(row=1, column=0)

		self.startbut = ttk.Button(
			self.buttonframe, text="Start",
			command=lambda: self.start_window())
		self.startbut.grid(row=0, column=0, padx=15, pady=5)
		self.startbut.bind("<Return>", lambda f: self.start_window())
		self.startbut.focus_set()

		self.returnbut = ttk.Button(
			self.buttonframe, text="Return",
			command=lambda: self.controller.show_frame("Rotation"))
		self.returnbut.grid(row=0, column=1, padx=15, pady=5)
		self.returnbut.bind(
			"<Return>",
			lambda f: self.controller.show_frame("Rotation"), "+")


	def start_window(self):


		#destroy the description of the version
		self.descrip_text.destroy()

		#descrip to start, change functions binded
		#to navigation buttons
		self.start_descrip = ttk.Label(
			self.descrip_frame, text="Click 'Enter' to start the test",
			font=LARGE_FONT, justify='center')
		self.start_descrip.grid(row=0, column=0)

		self.startbut['command'] = lambda: self.test_window()
		self.startbut.bind("<Return>", lambda f: self.test_window())
		self.startbut.focus_set()

		self.returnbut['command'] = lambda: self.create_widgets()
		self.returnbut.bind("<Return>", lambda f: self.create_widgets(), "+")


	def test_window(self, the_number=50):

		#destroy useless widgets so they don't still apppear in frame
		self.start_descrip.destroy()
		self.buttonframe.destroy()

		if self.controller.rot_counter < the_number:
			
			#create fixation point
			self.fix_point = ttk.Label(
				self.descrip_frame, text="+", font=SUPER_LARGE,
				justify='center')
			self.fix_point.grid(row=0, column=0)
			
			#after 3 secs show created figures
			self.fix_point.after(3000, self.show_animal)

			self.controller.rot_counter += 1

		else:

			#merge dicts for flipped and not flipped figures
			self.merge_dicts()
			self.controller.show_frame("RotationFInish")


	def show_animal(self):

		#decide whether flip the figure or not
		#create figures
		self.made_decision = self.flip_decision()
		image1 = self.rotate_image(self.work_pic)
		image1 = self.make_imagetk(image1)
		image2 = self.make_imagetk(self.work_pic)
		
		#show figures
		self.rotated_img = tk.Label(self.descrip_frame, image=image1)
		self.rotated_img.image = image1
		self.rotated_img.grid(row=0, column=0, padx=15, pady=15)

		self.fixed_img = tk.Label(self.descrip_frame, image=image2)
		self.fixed_img.image = image2
		self.fixed_img.grid(row=0, column=1, padx=15, pady=15)

		#figures are shown - count time of the reaction
		self.start_count()

		self.rotated_img.bind("<Left>", lambda f: self.arrow_left())
		self.rotated_img.bind("<Right>", lambda f: self.arrow_right())
		self.rotated_img.focus_set()


	def image_path(self):


		animal = 'elephant'
		basepath = os.path.dirname(__file__)

		self.imagepath = os.path.abspath(
				os.path.join(basepath, '..', 'img', animal+'.png'))


	def generate_image(self):


		self.work_pic = Image.open(self.imagepath)
		#alpha-layer for transparency
		self.work_pic = self.work_pic.convert('RGBA')


	def make_imagetk(self, image):


		"""Create image to work on"""

		image = ImageTk.PhotoImage(image)
		return(image)


	def rotate_image(self, image):


		#choice of angles to rotate
		angles = [angle for angle in range(30, 331, 30)]

		#store the angle for later purposes - dicts
		self.chosen_angle = random.choice(angles)

		#if decision == True -> return rotated and flipped image
		#otherwise only rotated
		if self.made_decision == True:

			im_final = image.rotate(self.chosen_angle, expand=1)
			im_final = self.make_flip(im_final)
			return(im_final)

		else:

			im_final = image.rotate(self.chosen_angle, expand=1)
			return(im_final)


	@staticmethod
	def flip_decision():


		"""Random selection whether flip or not"""

		return(random.getrandbits(1))


	@staticmethod
	def make_flip(image):


		""""Flip image vertically"""

		return(ImageOps.mirror(image))


	def start_count(self):


		"""Start counting time till the reaction of the user"""

		self.controller.rot_start_time = time.time()


	def stop_count(self):


		"""Stop counting time after the reaction of user"""

		self.controller.rot_stop_time = (round(time.time()
			- self.controller.rot_start_time, 4))


	def arrow_left(self):

		
		#stop counting and collect answers to proper dicts
		self.stop_count()
		self.collect_answers()

		#if image is flipped - good answer, else - bad
		if self.made_decision == 1:

			self.controller.rot_good_answ += 1

		else:

			self.controller.rot_bad_answ += 1


		self.clear_window()


	def arrow_right(self):


		#stop counting and collect answers to proper dicts
		self.stop_count()
		self.collect_answers()

		#if image is flipped - good answer, else - bad
		if self.made_decision == 0:

			self.controller.rot_good_answ += 1

		else:

			self.controller.rot_bad_answ += 1

		self.clear_window()


	def clear_window(self):


		self.rotated_img.grid_remove()
		self.fixed_img.grid_remove()

		self.test_window()


	def collect_answers(self):


		"""Assign time reaction to proper dict"""

		#if image flipped - assign to flipped dict
		if self.made_decision == 1:

			for key in self.controller.rot_flip_angle_time:
				
				if self.chosen_angle == key:
					(self.controller.rot_flip_angle_time[key].
						append(self.controller.rot_stop_time))
				
				else:
					pass

		else:

			for key in self.controller.rot_angle_time:
				
				if self.chosen_angle == key:
					(self.controller.rot_angle_time[key].
						append(self.controller.rot_stop_time))
				
				else:
					pass


	def merge_dicts(self):


		"""Create common dict to show later in summary"""

		dict_list = [self.controller.rot_angle_time,
			self.controller.rot_flip_angle_time]

		for item in dict_list:

			for key, value in item.items():

				(self.controller.rot_merged_times.
					setdefault(key, []).extend(value))


	def postupdate(self):


		self.navbutton.focus()


class RotationFinish(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)

		self.grid_columnconfigure(0, weight=2)
		self.controller = controller

		text_frame_finish = tk.Frame(self)
		text_frame_finish.grid(row=0, column=0)

		self.text_finish = tk.Text(
			text_frame_finish, font=LARGE_FONT, width=25, bg="#F0F0F0",
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
			nav_frame, text="Next",
			command=lambda: self.controller.show_frame("Summary"))
		self.navbutton.bind(
			"<Return>", lambda f: self.controller.show_frame("Summary"))
		self.navbutton.grid(row=1, column=0, padx=15, pady=15)

		self.menubutton = ttk.Button(
			nav_frame, text="Menu",
			command=lambda: self.controller.show_frame("StartPage"))
		self.menubutton.bind(
			"<Return>", lambda f: self.controller.show_frame("StartPage"), "+")
		self.menubutton.grid(row=1, column=1, padx=15, pady=5)


	def postupdate(self):


		self.navbutton.focus()