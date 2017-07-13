import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from statistics import mean

SUPER_LARGE = ("Verdana", 16)
LARGE_FONT = ("Verdana", 11)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 9)


class Summary(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.controller = controller

		self.main_frame()


	def main_frame(self):


		descrip_frame = tk.Frame(self)
		descrip_frame.grid(row=0, column=0)

		self.krep_results = tk.Label(
			descrip_frame, text="Kraepelin Test Results", justify="center",
			font=LARGE_FONT)
		self.krep_results.grid(row=0, column=0, padx=1, pady=2)

		self.stroop_results = tk.Label(
			descrip_frame, text="Stroop Test Results", justify="center",
			font=LARGE_FONT)
		self.stroop_results.grid(row=0, column=1, padx=1, pady=2)

		self.rotation_results = tk.Label(
			descrip_frame, text="Mental Rotation Results", justify="center",
			font=LARGE_FONT)
		self.rotation_results.grid(row=0, column=2, padx=1, pady=2)

		
		show_plot_frame = tk.Frame(self)
		show_plot_frame.grid(row=1, column=0)

		self.krep_button = ttk.Button(
			show_plot_frame, text="Show",
			command=lambda: self.show_krep())
		self.krep_button.grid(row=0, column=0, padx=45, pady=30)

		self.stroop_button = ttk.Button(
			show_plot_frame, text="Show",
			command=lambda: self.show_stroop())
		self.stroop_button.grid(row=0, column=1, padx=45, pady=30)

		self.rotation_button = ttk.Button(
			show_plot_frame, text="Show",
			command=lambda: self.show_rotation())
		self.rotation_button.grid(row=0, column=2, padx=45, pady=30)


	def show_krep(self):


		if len(self.controller.krep_answer_total) == 0:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Kraepelin Test")
			result_frame.resizable(0, 0)

			result_frame.bind("<Escape>", lambda f: result_frame.destroy())

			msg_label = tk.Label(
				result_frame, text="You haven't done this test!")
			msg_label.grid(row=0, column=0)

			ok_button = ttk.Button(
				result_frame, text="Ok",
				command=lambda: result_frame.destroy())
			ok_button.grid(row=1, column=0)
		

		else:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Kraepelin Test")
			result_frame.resizable(0, 0)

			result_frame.bind("<Escape>",
				lambda f: result_frame.destroy(), "+")

			stats_frame = tk.Frame(result_frame)
			stats_frame.grid(row=0, column=0)

			reformat_good_answ = ("Number of good answers: "
				+str(self.controller.krep_good_answ))
			good_answers = tk.Label(
				stats_frame, text=reformat_good_answ, justify='left',
				font=LARGE_FONT)
			good_answers.grid(row=0, column=0, padx=1, pady=1)

			reformat_bad_answ = ("Number of good answers: "
				+str(self.controller.krep_bad_answ))
			bad_answers = tk.Label(
				stats_frame, text=reformat_bad_answ, justify='left',
				font=LARGE_FONT)
			bad_answers.grid(row=1, column=0, padx=1, pady=1)

			reformat_fast = ("Fastest time of reaction: "
				+str(round(min(self.controller.krep_time_stamps), 4))
				+" sec")
			fastest_time = tk.Label(
				stats_frame, text=reformat_fast, anchor='e', font=LARGE_FONT)
			fastest_time.grid(row=2, column=0, padx=1, pady=1)

			reformat_slow = ("Slowest time of reaction: "
				+str(round(max(self.controller.krep_time_stamps), 4))
				+" sec")
			slowest_time = tk.Label(
				stats_frame, text=reformat_slow, anchor='e', font=LARGE_FONT)
			slowest_time.grid(row=3, column=0, padx=1, pady=1)

			reformat_avg = ("Average time of reaction: "
				+str(round(mean(self.controller.krep_time_stamps), 4))
				+" sec")
			avg_time = tk.Label(
				stats_frame, text=reformat_avg, anchor='e', font=LARGE_FONT)
			avg_time.grid(row=4, column=0, padx=1, pady=1)


			plot_frame = tk.Frame(result_frame)
			plot_frame.grid(row=1, column=0)

			f = Figure(figsize=(5,2.75), dpi=100, frameon=True)
			a = f.add_subplot(111)
			a.plot(range(1, (len(self.controller.krep_answer_total)+1)),
				self.controller.krep_time_stamps)

			canvas = FigureCanvasTkAgg(f, plot_frame)
			canvas.show()
			canvas.get_tk_widget().pack(side='left')


	def show_stroop(self):


		if self.controller.stroop_counter == 0:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Stroop Test")
			result_frame.resizable(0, 0)

			result_frame.bind(
				"<Escape>", lambda f: result_frame.destroy(), "+")

			msg_label = tk.Label(
				result_frame, text="You haven't done this test!")
			msg_label.grid(row=0, column=0, padx=20, pady=20)

			ok_button = ttk.Button(
				result_frame, text="Ok",
				command=lambda: result_frame.destroy())
			ok_button.grid(row=1, column=0, padx=20, pady=20)

		else:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Stroop Test")
			result_frame.resizable(0, 0)

			result_frame.bind(
				"<Escape>", lambda f: result_frame.destroy(), "+")

			stats_frame = tk.Frame(result_frame)
			stats_frame.grid(row=0, column=0)

			reformat_good_answ = ("Number of good answers: "
				+str(self.controller.stroop_good_answ))
			good_answers = tk.Label(
				stats_frame, text=reformat_good_answ, anchor='w',
				font=LARGE_FONT)
			good_answers.grid(row=0, column=0, padx=2, pady=2)

			reformat_bad_answ = ("Number of good answers: "
				+str(self.controller.stroop_bad_answ))
			bad_answers = tk.Label(
				stats_frame, text=reformat_bad_answ, anchor='w',
				font=LARGE_FONT)
			bad_answers.grid(row=1, column=0, padx=2, pady=2)

			#TOTAL ANSWERS
			reformat_fast = ("Fastest time of reaction: "
				+str(round(min(self.controller.stroop_time_stamps), 4))
				+" sec")
			fastest_time = tk.Label(
				stats_frame, text=reformat_fast, anchor='w', font=LARGE_FONT)
			fastest_time.grid(row=2, column=0, padx=2, pady=2)

			reformat_slow = ("Slowest time of reaction: "
				+str(round(max(self.controller.stroop_time_stamps), 4))
				+" sec")
			slowest_time = tk.Label(
				stats_frame, text=reformat_slow, anchor='w', font=LARGE_FONT)
			slowest_time.grid(row=3, column=0, padx=2, pady=2)

			reformat_avg = ("Average time of reaction: "
				+str(round(mean(self.controller.stroop_time_stamps), 4))
				+" sec")
			avg_time = tk.Label(
				stats_frame, text=reformat_avg, anchor='w', font=LARGE_FONT)
			avg_time.grid(row=4, column=0, padx=2, pady=2)

			#CONGRUENT ANSWERS
			reformat_fast_cong = ("Fastest time of reaction (congruent): "
				+str(round(min(self.controller.stroop_time_stamps_cong), 4))
				+" sec")
			fastest_time_cong = tk.Label(
				stats_frame, text=reformat_fast_cong, anchor='w', font=LARGE_FONT)
			fastest_time_cong.grid(row=0, column=1, padx=2, pady=2)

			reformat_slow_cong = ("Slowest time of reaction (congruent): "
				+str(round(max(self.controller.stroop_time_stamps_cong), 4))
				+" sec")
			slowest_time_cong = tk.Label(
				stats_frame, text=reformat_slow_cong, anchor='w', font=LARGE_FONT)
			slowest_time_cong.grid(row=1, column=1, padx=2, pady=2)

			reformat_avg_cong = ("Average time of reaction (congruent): "
				+str(round(mean(self.controller.stroop_time_stamps_cong), 4))
				+" sec")
			avg_time_cong = tk.Label(
				stats_frame, text=reformat_avg_cong, anchor='w', font=LARGE_FONT)
			avg_time_cong.grid(row=2, column=1, padx=2, pady=2)

			#NON-CONGRUENT ANSWERS
			reformat_fast_ncong = ("Fastest time of reaction (noncongruent): "
				+str(round(min(
					self.controller.stroop_time_stamps_noncong), 4))
				+" sec")
			fastest_time_ncong = tk.Label(
				stats_frame, text=reformat_fast_ncong, anchor='w', font=LARGE_FONT)
			fastest_time_ncong.grid(row=0, column=2, padx=2, pady=2)

			reformat_slow_ncong = ("Slowest time of reaction (noncongruent): "
				+str(round(max(
					self.controller.stroop_time_stamps_noncong), 4))
				+" sec")
			slowest_time_ncong = tk.Label(
				stats_frame, text=reformat_slow_ncong, anchor='w', font=LARGE_FONT)
			slowest_time_ncong.grid(row=1, column=2, padx=2, pady=2)

			reformat_avg_ncong = ("Average time of reaction (noncongruent): "
				+str(round(mean(
					self.controller.stroop_time_stamps_noncong), 4))
				+" sec")
			avg_time_ncong = tk.Label(
				stats_frame, text=reformat_avg_ncong, anchor='w', font=LARGE_FONT)
			avg_time_ncong.grid(row=2, column=2, padx=2, pady=2)

			plot_frame = tk.Frame(result_frame)
			plot_frame.grid(row=1, column=0)

			fig1 = Figure(figsize=(5,2.75), dpi=100, frameon=True)
			a1 = fig1.add_subplot(111)
			a1.plot(
				range(1, self.controller.stroop_counter+1),
				self.controller.stroop_time_stamps)

			canvas1 = FigureCanvasTkAgg(fig1, plot_frame)
			canvas1.show()
			canvas1.get_tk_widget().pack(side='left')

			fig2 = Figure(figsize=(5,2.75), dpi=100, frameon=True)
			a2 = fig2.add_subplot(111)
			a2.plot(
				range(1,(len(self.controller.stroop_time_stamps_cong)+1)),
				self.controller.stroop_time_stamps_cong)
			
			canvas2 = FigureCanvasTkAgg(fig2, plot_frame)
			canvas2.show()
			canvas2.get_tk_widget().pack(side='left')

			fig3 = Figure(figsize=(5,2.75), dpi=100, frameon=True)
			a3 = fig3.add_subplot(111)
			a3.plot(
				range(1,(len(self.controller.stroop_time_stamps_noncong)+1)),
				self.controller.stroop_time_stamps_noncong)

			canvas3 = FigureCanvasTkAgg(fig3, plot_frame)
			canvas3.show()
			canvas3.get_tk_widget().pack(side='left')


	def show_rotation(self):


		if self.controller.rot_counter == 0:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Mental Rotation")
			result_frame.resizable(0, 0)

			result_frame.bind(
				"<Escape>", lambda f: result_frame.destroy(), "+")

			msg_label = tk.Label(
				result_frame, text="You haven't done this test!")
			msg_label.grid(row=0, column=0, padx=20, pady=20)

			ok_button = ttk.Button(
				result_frame, text="Ok",
				command=lambda: result_frame.destroy())
			ok_button.grid(row=1, column=0, padx=20, pady=20)

		else:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Mental Rotation")
			result_frame.resizable(0, 0)

			result_frame.bind(
				"<Escape>", lambda f: result_frame.destroy(), "+")

			stats_frame = tk.Frame(result_frame)
			stats_frame.grid(row=0, column=0)

			reformat_good_answ = ("Number of good answers: "
				+str(self.controller.rot_good_answ))
			good_answers = tk.Label(
				stats_frame, text=reformat_good_answ, anchor='w',
				font=LARGE_FONT)
			good_answers.grid(row=0, column=0, padx=2, pady=2)

			reformat_bad_answ = ("Number of good answers: "
				+str(self.controller.rot_bad_answ))
			bad_answers = tk.Label(
				stats_frame, text=reformat_bad_answ, anchor='w',
				font=LARGE_FONT)
			bad_answers.grid(row=1, column=0, padx=2, pady=2)

			not_flipped_fast_val = ("Fastest reaction for normal images: "
				+str(round(min(list(
					self.controller.rot_angle_time.values())), 4))
				+" sec")
			not_flipped_fast = tk.Label(
				stats_frame, text=not_flipped_fast_val, anchor='w',
				font=LARGE_FONT)
			not_flipped_fast.grid(row=0, column=1, padx=2, pady=2)

			not_flipped_slow_val = ("Slowest reaction for normal images: "
				+str(round(max(list(
					self.controller.rot_angle_time.values())), 4))
				+" sec")
			not_flipped_slow = tk.Label(
				stats_frame, text=not_flipped_slow_val, anchor='w',
				font=LARGE_FONT)
			not_flipped_fast.grid(row=1, column=1, padx=2, pady=2)

			not_flipped_avg_val = ("Average reaction for normal images: "
				+str(round(mean(list(
					self.controller.rot_angle_time.values())), 4))
				+" sec")
			not_flipped_slow = tk.Label(
				stats_frame, text=not_flipped_avg_val, anchor='w',
				font=LARGE_FONT)
			not_flipped_fast.grid(row=2, column=1, padx=2, pady=2)

			flipped_fast_val = ("Fastest reaction for flipped images: "
			+str(round(min(list(
				self.controller.rot_flip_angle_time.values())), 4))
			+" sec")
			flipped_fast = tk.Label(
				stats_frame, text=flipped_fast_val, anchor='w',
				font=LARGE_FONT)
			flipped_fast.grid(row=0, column=3, padx=2, pady=2)

			flipped_slow_val = ("Slowest reaction for flipped images: "
			+str(round(max(list(
				self.controller.rot_flip_angle_time.values())), 4))
			+" sec")
			flipped_slow = tk.Label(
				stats_frame, text=flipped_slow_val, anchor='w',
				font=LARGE_FONT)
			flipped_slow.grid(row=1, column=3, padx=2, pady=2)

			flipped_avg_val = ("Average reaction for flipped images: "
			+str(round(min(list(
				self.controller.rot_flip_angle_time.values())), 4))
			+" sec")
			flipped_avg = tk.Label(
				stats_frame, text=flipped_avg_val, anchor='w',
				font=LARGE_FONT)
			flipped_avg.grid(row=2, column=3, padx=2, pady=2)
			
			plot_frame = tk.Frame(result_frame)
			plot_frame.grid(row=1, column=0)

			fig1 = Figure(figsize=(5,2.75), dpi=100, frameon=True)
			a1 = fig1.add_subplot(111)

			x_axis1 = []
			y_axis1 = []
			for key, value in self.controller.rot_angle_time.items():

				if value:

					x_axis1.append(int(key))
					y_axis1.append(mean(value))


			a1.plot(x_axis1, y_axis1)

			canvas1 = FigureCanvasTkAgg(fig1, plot_frame)
			canvas1.show()
			canvas1.get_tk_widget().pack(side='left')

			fig2 = Figure(figsize=(5,2.75), dpi=100, frameon=True)
			a2 = fig2.add_subplot(111)

			x_axis2 = []
			y_axis2 = []
			for key, value in self.controller.rot_flip_angle_time.items():

				if value:

					x_axis2.append(int(key))
					y_axis2.append(mean(value))

			a2.plot(x_axis2, y_axis2)

			canvas2 = FigureCanvasTkAgg(fig2, plot_frame)
			canvas2.show()
			canvas2.get_tk_widget().pack(side='left')

			fig3 = Figure(figsize=(5,2.75), dpi=100, frameon=True)
			a3 = fig3.add_subplot(111)

			x_axis3 = []
			y_axis3 = []
			for key, value in self.controller.rot_merged_times.items():

				if value:

					x_axis3.append(int(key))
					y_axis3.append(mean(value))

			a2.plot(x_axis3, y_axis3)

			canvas2 = FigureCanvasTkAgg(fig3, plot_frame)
			canvas2.show()
			canvas2.get_tk_widget().pack(side='left')