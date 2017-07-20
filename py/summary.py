import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from statistics import mean
import math
import numpy as np
import os

SUPER_LARGE = ("Verdana", 16)
LARGE_FONT = ("Verdana", 11)
NORMAL_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 9)


class Summary(tk.Frame):


	def __init__(self, parent, controller):


		tk.Frame.__init__(self, parent)
		self.controller = controller

		self.values_to_save = {}

		self.main_frame()


	def main_frame(self):


		#Frame for description of buttons and themselves
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

		#Frame for buttons to show separate windows with experiment
		#statistics and buttons to show stats
		show_plot_frame = tk.Frame(self)
		show_plot_frame.grid(row=1, column=0)

		self.krep_button = ttk.Button(
			show_plot_frame, text="Show",
			command=lambda: self.show_krep())
		self.krep_button.grid(row=0, column=0, padx=45, pady=10)
		self.krep_button.bind(
			"<Return>", lambda f: self.show_krep())

		self.stroop_button = ttk.Button(
			show_plot_frame, text="Show",
			command=lambda: self.show_stroop())
		self.stroop_button.grid(row=0, column=1, padx=45, pady=10)
		self.stroop_button.bind(
			"<Return>", lambda f: self.show_stroop(), "+")

		self.rotation_button = ttk.Button(
			show_plot_frame, text="Show",
			command=lambda: self.show_rotation())
		self.rotation_button.grid(row=0, column=2, padx=45, pady=10)
		self.rotation_button.bind(
			"<Return>", lambda f: self.show_rotation(), "+")

		#Buttons to save stats to csv file or to rerun experiments
		self.save_button = ttk.Button(
			show_plot_frame, text="Save results",
			command=lambda: self.save_results())
		self.save_button.grid(row=1, column=1, pady=10)

		self.rerun_button = ttk.Button(
			show_plot_frame, text="Run again",
			command= lambda: self.controller.show_frame("StartPage"))
		self.rerun_button.grid(row=1, column=2, pady=10)


	def postupdate(self):


		self.krep_button.focus_set()


	def show_krep(self):


		#show window without results if there's no experiment
		if len(self.controller.krep_answer_total) == 0:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Kraepelin Test")
			result_frame.resizable(0, 0)

			result_frame.bind("<Escape>", lambda f: result_frame.destroy())

			msg_label = tk.Label(
				result_frame, text="You haven't done this test!",
				font=LARGE_FONT)
			msg_label.grid(row=0, column=0, padx=20, pady=20)

			ok_button = ttk.Button(
				result_frame, text="Ok",
				command=lambda: result_frame.destroy())
			ok_button.bind(
				"<Return>", lambda f: result_frame.destroy())
			ok_button.grid(row=1, column=0)
			ok_button.focus_set()
		

		else:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Kraepelin Test")
			result_frame.resizable(0, 0)

			result_frame.bind("<Escape>",
				lambda f: result_frame.destroy(), "+")

			#frame for all stats in strings
			stats_frame = tk.Frame(result_frame)
			stats_frame.grid(row=0, column=0)

			#stats for good and bad answers for test
			reformat_good_answ = ("Number of good answers: "
				+str(self.controller.krep_good_answ))
			good_answers = tk.Label(
				stats_frame, text=reformat_good_answ, justify='left',
				font=LARGE_FONT)
			good_answers.grid(row=0, column=0, padx=2, pady=1)

			reformat_bad_answ = ("Number of bad answers: "
				+str(self.controller.krep_bad_answ))
			bad_answers = tk.Label(
				stats_frame, text=reformat_bad_answ, justify='left',
				font=LARGE_FONT)
			bad_answers.grid(row=1, column=0, padx=2, pady=2)

			#stats for fastest, slowest and average time of reaction
			reformat_fast = ("Fastest time of reaction: "
				+str(round(min(self.controller.krep_time_stamps), 4))
				+" sec")
			fastest_time = tk.Label(
				stats_frame, text=reformat_fast, anchor='w', font=LARGE_FONT)
			fastest_time.grid(row=2, column=0, padx=2, pady=2)

			reformat_slow = ("Slowest time of reaction: "
				+str(round(max(self.controller.krep_time_stamps), 4))
				+" sec")
			slowest_time = tk.Label(
				stats_frame, text=reformat_slow, anchor='w', font=LARGE_FONT)
			slowest_time.grid(row=3, column=0, padx=2, pady=2)

			reformat_avg = ("Average time of reaction: "
				+str(round(mean(self.controller.krep_time_stamps), 4))
				+" sec")
			avg_time = tk.Label(
				stats_frame, text=reformat_avg, anchor='w', font=LARGE_FONT)
			avg_time.grid(row=4, column=0, padx=2, pady=2)

			#collect answers and format them for further saving
			self.collect_to_save(
				"Kraepelin Good Answer", self.controller.krep_good_answ)

			self.collect_to_save(
				"Kraepelin Bad Answer", self.controller.krep_bad_answ)

			self.collect_to_save(
				"Kraepelin Fastest Reaction",
				round(min(self.controller.krep_time_stamps), 4))

			self.collect_to_save(
				"Kraepelin Slowest Reaction",
				round(max(self.controller.krep_time_stamps), 4))

			if (self.controller.stroop.get() and self.controller.rotation.get()) == 0:
				
				self.collect_to_save(
					"Kraepelin Average Reaction",
					round(mean(self.controller.krep_time_stamps), 4),
					end_of_line=True)

			else:

				self.collect_to_save(
					"Kraepelin Average Reaction",
					round(mean(self.controller.krep_time_stamps), 4))


			#frame for plottings
			plot_frame = tk.Frame(result_frame)
			plot_frame.grid(row=1, column=0)

			#plot for answers and their time reactions
			line_color = "#033192"
			results_time = Figure(figsize=(5.25, 4.25), dpi=100,
				facecolor="#F0F0F0F0")
			time_stamps = results_time.add_subplot(
				111,
				xticks=range((self.controller.krep_counter)+1),
				xlabel="Number of column",
				yticks=np.arange(
					0.00, math.ceil(max(self.controller.krep_time_stamps)+1.0),
					0.25),
				ylabel="Time of reaction",
				facecolor="#CECECE")
			time_stamps.plot(
				range(1, (len(self.controller.krep_answer_total)+1)),
				self.controller.krep_time_stamps,
				line_color,
				marker="o",
				linewidth=0.5)
			time_stamps.grid(True)

			canvas = FigureCanvasTkAgg(results_time, plot_frame)
			canvas.show()
			canvas.get_tk_widget().pack(side='left')


	def show_stroop(self):


		#window message if the experiment wasn't undergone
		if self.controller.stroop_counter == 0:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Stroop Test")
			result_frame.resizable(0, 0)

			result_frame.bind(
				"<Escape>", lambda f: result_frame.destroy(), "+")

			msg_label = tk.Label(
				result_frame, text="You haven't done this test!",
				font=LARGE_FONT)
			msg_label.grid(row=0, column=0, padx=20, pady=20)

			ok_button = ttk.Button(
				result_frame, text="Ok",
				command=lambda: result_frame.destroy())
			ok_button.bind(
				"<Return>", lambda f: result_frame.destroy())
			ok_button.grid(row=1, column=0, padx=20, pady=20)
			ok_button.focus_set()

		else:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Stroop Test")
			result_frame.resizable(0, 0)

			result_frame.bind(
				"<Escape>", lambda f: result_frame.destroy(), "+")

			#frame for stats
			stats_frame = tk.Frame(result_frame)
			stats_frame.grid(row=0, column=0)

			#good and bad answers for whole test
			reformat_good_answ = ("Number of good answers: "
				+str(self.controller.stroop_good_answ))
			good_answers = tk.Label(
				stats_frame, text=reformat_good_answ, anchor='w',
				font=LARGE_FONT)
			good_answers.grid(row=0, column=0, padx=2, pady=2)

			reformat_bad_answ = ("Number of bad answers: "
				+str(self.controller.stroop_bad_answ))
			bad_answers = tk.Label(
				stats_frame, text=reformat_bad_answ, anchor='w',
				font=LARGE_FONT)
			bad_answers.grid(row=1, column=0, padx=2, pady=2)

			#fastest, slowest and average time of reaction
			#for whole test
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

			#fastest, slowest, and average time of reaction
			#for congruent words (e.g. blue word in blue colour)
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

			#fastest, slowest, and average time of reaction
			#for congruent words (e.g. blue word in yellow colour)
			reformat_fast_ncong = ("Fastest time of reaction (noncongruent): "
				+str(round(min(
					self.controller.stroop_time_stamps_noncong), 4))
				+" sec")
			fastest_time_ncong = tk.Label(
				stats_frame, text=reformat_fast_ncong, anchor='w', font=LARGE_FONT)
			fastest_time_ncong.grid(row=0, column=2, padx=5, pady=2)

			reformat_slow_ncong = ("Slowest time of reaction (noncongruent): "
				+str(round(max(
					self.controller.stroop_time_stamps_noncong), 4))
				+" sec")
			slowest_time_ncong = tk.Label(
				stats_frame, text=reformat_slow_ncong, anchor='w', font=LARGE_FONT)
			slowest_time_ncong.grid(row=1, column=2, padx=5, pady=2)

			reformat_avg_ncong = ("Average time of reaction (noncongruent): "
				+str(round(mean(
					self.controller.stroop_time_stamps_noncong), 4))
				+" sec")
			avg_time_ncong = tk.Label(
				stats_frame, text=reformat_avg_ncong, anchor='w', font=LARGE_FONT)
			avg_time_ncong.grid(row=2, column=2, padx=5, pady=2)

			#collect answers and format them for further saving
			self.collect_to_save(
				"Stroop Good Answer", self.controller.stroop_good_answ)

			self.collect_to_save(
				"Stroop Bad Answer", self.controller.stroop_bad_answ)

			self.collect_to_save(
				"Stroop Fastest Reaction All",
				round(min(self.controller.stroop_time_stamps), 4))

			self.collect_to_save(
				"Stroop Slowest Reaction All",
				round(max(self.controller.stroop_time_stamps), 4))

			self.collect_to_save(
				"Stroop Average Reaction All",
				round(mean(self.controller.stroop_time_stamps), 4))

			self.collect_to_save(
				"Stroop Fastest Reaction (Congruent)",
				round(min(self.controller.stroop_time_stamps_cong), 4))

			self.collect_to_save(
				"Stroop Slowest Reaction (Congruent)",
				round(max(self.controller.stroop_time_stamps_cong), 4))

			self.collect_to_save(
				"Stroop Average Reaction (Congruent)",
				round(mean(self.controller.stroop_time_stamps_cong), 4))
				
			self.collect_to_save(
				"Stroop Fastest Reaction (Noncongruent)",
				round(min(self.controller.stroop_time_stamps_noncong), 4))

			self.collect_to_save(
				"Stroop Slowest Reaction (Noncongruent)",
				round(max(self.controller.stroop_time_stamps_noncong), 4))

			if self.controller.rotation.get() == 0:

				self.collect_to_save(
					"Stroop Average Reaction (Noncongruent)",
					round(mean(self.controller.stroop_time_stamps_noncong), 4),
					end_of_line=True)

			else:

				self.collect_to_save(
					"Stroop Average Reaction (Noncongruent)",
					round(mean(self.controller.stroop_time_stamps_noncong), 4))


			#frame for plots
			plot_frame = tk.Frame(result_frame)
			plot_frame.grid(row=1, column=0)

			#plot for alle the answers (congruent and noncongruent)
			line_color_all = "#033192"
			all_results = Figure(
				figsize=(5.25, 4.25), dpi=80, facecolor="#F0F0F0")
			time_stamps = all_results.add_subplot(
				111,
				xlabel="No. of exposition",
				xticks=np.arange(
					0.0,
					float(self.controller.stroop_counter+1.00),
					5.00),
				yticks=np.arange(
					0.00,
					math.ceil(max(self.controller.stroop_time_stamps)+1.0),
					0.25),
				ylabel="Time of reaction",
				facecolor="#CECECE")
			time_stamps.plot(
				range(1, self.controller.stroop_counter+1),
				self.controller.stroop_time_stamps,
				line_color_all,
				linewidth=0.5)
			time_stamps.grid(True)

			canvas1 = FigureCanvasTkAgg(all_results, plot_frame)
			canvas1.show()
			canvas1.get_tk_widget().pack(side='left')

			#plot for congruent answers
			line_color_cong = "#9C353A"
			cong_result = Figure(
				figsize=(5.25, 4.25), dpi=80, facecolor="#F0F0F0")
			time_stamps_cong = cong_result.add_subplot(
				111,
				xticks=np.arange(
					0.0,
					float(len(self.controller.stroop_time_stamps_cong))+1,
					5.00),
				xlabel="No. of exposition",
				yticks=np.arange(
					0.00,
					math.ceil(max(self.controller.stroop_time_stamps_cong)+1),
					0.25),
				ylabel="Time of reaction",
				facecolor="#CECECE")
			time_stamps_cong.plot(
				range(1,(len(self.controller.stroop_time_stamps_cong)+1)),
				self.controller.stroop_time_stamps_cong,
				line_color_cong,
				marker="^",
				linewidth=0.5)
			time_stamps_cong.grid(True)
			
			canvas2 = FigureCanvasTkAgg(cong_result, plot_frame)
			canvas2.show()
			canvas2.get_tk_widget().pack(side='left')

			#plot for noncongruent answers
			line_color_ncong = "#F8CB49"
			non_cong_result = Figure(
				figsize=(5.25, 4.25), dpi=80, facecolor="#F0F0F0")
			time_stamps_ncong = non_cong_result.add_subplot(
				111,
				xticks=np.arange(
					0.00,
					float(len(self.controller.stroop_time_stamps_noncong))+1,
					5.00),
				xlabel="No. of exposition",
				yticks=np.arange(
					0.0,
					math.ceil(max(self.controller.stroop_time_stamps_noncong))+1,
					0.25),
				ylabel="Time of reaction",
				facecolor="#CECECE")
			time_stamps_ncong.plot(
				range(1,(len(self.controller.stroop_time_stamps_noncong)+1)),
				self.controller.stroop_time_stamps_noncong,
				line_color_ncong,
				marker="s",
				linewidth=0.5)
			time_stamps_ncong.grid(True)

			canvas3 = FigureCanvasTkAgg(non_cong_result, plot_frame)
			canvas3.show()
			canvas3.get_tk_widget().pack(side='left')


	def show_rotation(self):


		#window message if the experiment wasn't undergone
		if self.controller.rot_counter == 0:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Mental Rotation")
			result_frame.resizable(0, 0)

			result_frame.bind(
				"<Escape>", lambda f: result_frame.destroy(), "+")

			msg_label = tk.Label(
				result_frame, text="You haven't done this test!",
				font=LARGE_FONT)
			msg_label.grid(row=0, column=0, padx=20, pady=20)

			ok_button = ttk.Button(
				result_frame, text="Ok",
				command=lambda: result_frame.destroy())
			ok_button.bind(
				"<Return>", lambda f: result_frame.destroy())
			ok_button.grid(row=1, column=0, padx=20, pady=20)
			ok_button.focus_set()

		else:

			result_frame = tk.Toplevel()
			result_frame.wm_title("Mental Rotation")
			result_frame.resizable(0, 0)

			result_frame.bind(
				"<Escape>", lambda f: result_frame.destroy(), "+")

			#frame for stats from experiment
			stats_frame = tk.Frame(result_frame)
			stats_frame.grid(row=0, column=0)

			#stats for good and bad reactions of user
			reformat_good_answ = (
				"Number of good answers: "+str(self.controller.rot_good_answ))
			good_answers = tk.Label(
				stats_frame, text=reformat_good_answ, anchor='w',
				font=LARGE_FONT)
			good_answers.grid(row=0, column=0, padx=2, pady=2)

			reformat_bad_answ = (
				"Number of bad answers: "+str(self.controller.rot_bad_answ))
			bad_answers = tk.Label(
				stats_frame, text=reformat_bad_answ, anchor='w',
				font=LARGE_FONT)
			bad_answers.grid(row=1, column=0, padx=2, pady=2)


			#store all the values for non-flipped images
			all_times_non_flip = []

			for value in self.controller.rot_angle_time.values():

				all_times_non_flip.extend(value)

			#stats for fastest, slowest and average time of reaction
			#for non-flipped images
			not_flipped_fast_val = (
				"Fastest reaction for normal images: "
				+str(round(min(all_times_non_flip), 4))
				+" sec")
			not_flipped_fast = tk.Label(
				stats_frame, text=not_flipped_fast_val, anchor='w',
				font=LARGE_FONT)
			not_flipped_fast.grid(row=0, column=1, padx=2, pady=2)

			not_flipped_slow_val = (
				"Slowest reaction for normal images: "
				+str(round(max(all_times_non_flip), 4))
				+" sec")
			not_flipped_slow = tk.Label(
				stats_frame, text=not_flipped_slow_val, anchor='w',
				font=LARGE_FONT)
			not_flipped_slow.grid(row=1, column=1, padx=2, pady=2)

			not_flipped_avg_val = (
				"Average reaction for normal images: "
				+str(round(mean(all_times_non_flip), 4))
				+" sec")
			not_flipped_avg = tk.Label(
				stats_frame, text=not_flipped_avg_val, anchor='w',
				font=LARGE_FONT)
			not_flipped_avg.grid(row=2, column=1, padx=2, pady=2)


			#store all the values for flipped images
			all_times_flip = []

			for value in self.controller.rot_flip_angle_time.values():

				all_times_flip.extend(value)

			#stats for fastest, slowest and average time of reaction
			#for flipped images
			flipped_fast_val = (
				"Fastest reaction for flipped images: "
				+str(round(min(all_times_flip), 4))
				+" sec")
			flipped_fast = tk.Label(
				stats_frame, text=flipped_fast_val, anchor='w',
				font=LARGE_FONT)
			flipped_fast.grid(row=0, column=3, padx=2, pady=2)

			flipped_slow_val = (
				"Slowest reaction for flipped images: "
				+str(round(max(all_times_flip), 4))
				+" sec")
			flipped_slow = tk.Label(
				stats_frame, text=flipped_slow_val, anchor='w',
				font=LARGE_FONT)
			flipped_slow.grid(row=1, column=3, padx=2, pady=2)

			flipped_avg_val = (
				"Average reaction for flipped images: "
				+str(round(mean(all_times_flip), 4))
				+" sec")
			flipped_avg = tk.Label(
				stats_frame, text=flipped_avg_val, anchor='w',
				font=LARGE_FONT)
			flipped_avg.grid(row=2, column=3, padx=2, pady=2)


			#collect answers and format them for further saving
			self.collect_to_save(
				"Rotation Good Answer", self.controller.rot_good_answ)

			self.collect_to_save(
				"Rotation Bad Answer", self.controller.rot_bad_answ)

			self.collect_to_save(
				"Rotation Fastest Reaction (Non-flipped)",
				round(min(all_times_non_flip), 4))

			self.collect_to_save(
				"Rotation Slowest Reaction (Non-flipped)",
				round(max(all_times_non_flip), 4))

			self.collect_to_save(
				"Rotation Average Reaction (Non-flipped)",
				round(mean(all_times_non_flip), 4))

			self.collect_to_save(
				"Rotation Fastest Reaction (Congruent)",
				round(min(all_times_flip), 4))

			self.collect_to_save(
				"Rotation Slowest Reaction (Congruent)",
				round(max(all_times_flip), 4))

			self.collect_to_save(
				"Rotation Average Reaction (Congruent)",
				round(mean(all_times_flip), 4),
				end_of_line=True)

			
			#frame for plotting stats
			plot_frame = tk.Frame(result_frame)
			plot_frame.grid(row=1, column=0)

			#vars to show in plots mean times of reaction
			#for specific angle for non-flipped images
			x_axis1 = []
			y_axis1 = []
			x_labels_nonflip = []
			for key, value in self.controller.rot_angle_time.items():

				if value:

					x_axis1.append(int(key))
					y_axis1.append(mean(value))
					x_labels_nonflip.append(key)			

			#plot for mean reaction times of non-flipped images
			#for specific angles
			line_color_nonflip = "#3297ac"
			nonflip_results = Figure(
				figsize=(5.25, 4.25), dpi=70, facecolor="#F0F0F0")
			time_stamps_nonflip = nonflip_results.add_subplot(
				111,
				xlabel="Degree of rotation",
				ylabel="Time of reaction",
				xticklabels=x_labels_nonflip,
				yticks=np.arange(
					0.0,
					math.ceil(sum(max(self.controller.rot_angle_time.values())))+1,
					0.25),
				facecolor="#CECECE"
				)
			time_stamps_nonflip.grid(True)

			time_stamps_nonflip.plot(
				x_axis1, y_axis1, line_color_nonflip, marker="d", linewidth=0.5)

			canvas1 = FigureCanvasTkAgg(nonflip_results, plot_frame)
			canvas1.show()
			canvas1.get_tk_widget().pack(side='left')

			#vars to show in plots mean times of reaction
			#for specific angle for flipped images
			x_axis2 = []
			y_axis2 = []
			x_labels_flip = []
			for key, value in self.controller.rot_flip_angle_time.items():

				if value:

					x_axis2.append(int(key))
					y_axis2.append(mean(value))
					x_labels_flip.append(key)

			#plot for mean reaction times of flipped images
			#for specific angles
			line_color_flip = "#FBC704"
			flip_results = Figure(
				figsize=(5.25, 4.25), dpi=70, facecolor="#F0F0F0")
			time_stamps_flip = flip_results.add_subplot(
				111,
				xlabel="Degree of rotation",
				ylabel="Time of reaction",
				xticklabels=x_labels_flip,
				yticks=np.arange(
					0.0,
					math.ceil(sum(max(self.controller.rot_flip_angle_time.values())))+1,
					0.25),
				facecolor="#CECECE"
				)
			time_stamps_flip.grid(True)

			time_stamps_flip.plot(
				x_axis2, y_axis2, line_color_flip, marker="*", linewidth=0.5)

			canvas2 = FigureCanvasTkAgg(flip_results, plot_frame)
			canvas2.show()
			canvas2.get_tk_widget().pack(side='left')


			#vars to show in plots mean times of reaction
			#for specific angle for all images
			x_axis3 = []
			y_axis3 = []
			x_labels_merged = []
			for key, value in self.controller.rot_merged_times.items():

				if value:

					x_axis3.append(int(key))
					y_axis3.append(mean(value))
					x_labels_merged.append(key)

			#plot for mean reaction times of all images
			#for specific angles
			line_color_merged = "#59F4F0"
			merged_results = Figure(figsize=(5.25,4.25), dpi=70, facecolor="#F0F0F0")
			time_stamps_merged = merged_results.add_subplot(
				111,
				xlabel="Degree of rotation",
				ylabel="Time of reaction",
				xticklabels=x_labels_merged,
				yticks=np.arange(
					0.0,
					math.ceil(sum(max(self.controller.rot_merged_times.values())))+1,
					0.25),
				facecolor="#CECECE"
				)
			time_stamps_merged.grid(True)

			time_stamps_merged.plot(
				x_axis3, y_axis3, line_color_merged, marker="v", linewidth=0.5)

			canvas3 = FigureCanvasTkAgg(merged_results, plot_frame)
			canvas3.show()
			canvas3.get_tk_widget().pack(side='left')


	def collect_to_save(self, name, value, end_of_line=False):


		#for csv - if false, save in same line
		#else, end line with \n
		if end_of_line == False:

			try:

				name = name+";"
				
				self.values_to_save[name] = str(value)+";"

			except ValueError:

				print("There's no such value!")
				self.values_to_save[name] = "NA;"

		else:

			try:
				name = name+"\n"

				self.values_to_save[name] = str(value)+"\n"

			except ValueError:

				print("There's no such value!")
				self.values_to_save[name] = "NA\n"


	def save_results(self):


		file_to_save = filedialog.asksaveasfilename(
			defaultextension=".csv",
			initialdir=os.path.join(os.environ["HOMEPATH"], "Desktop"),
			confirmoverwrite=True,
			filetypes=[("CSV file", ".csv"), ("All files", "*.*")])

		if file_to_save:

			release = open(file_to_save, "w")

			for key in self.values_to_save.keys():

				release.write(key)


			for value in self.values_to_save.values():

				release.write(value)

			release.close()

