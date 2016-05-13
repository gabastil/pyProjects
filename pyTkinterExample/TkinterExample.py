#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name: 	TkinterExample.py
# Version: 	1.0.0 
# Author: 	Glenn Abastillas
# Date: 	March 03, 2016
#
# Purpose: Allows the user to:
#           1.) View the main window of an application and navigate to other frames, pages, and windows.
#
# To see the script run, go to the bottom of this page. 
#
# This class is not directly inherited by any other class.
#
# Updates:
# - - - - - - - - - - - - -

"""	sandbox for Tkinter module.
"""
from Tkinter import *
from Tkinter import Tk
from Tkinter import Frame
from Tkinter import Label
from Tkinter import Button

class MainWindow(Tk):

	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)

		SCREEN_WIDTH  = self.winfo_screenwidth()
		SCREEN_HEIGHT = self.winfo_screenheight()
		WINDOW_WIDTH  = 400
		WINDOW_HEIGHT = 600
		CORNER_X	  = (SCREEN_WIDTH/2)-(WINDOW_WIDTH/2)
		CORNER_Y 	  = (SCREEN_HEIGHT/2)-(WINDOW_HEIGHT/2)

		self.geometry("{0}x{1}+{2}+{3}".format(WINDOW_WIDTH, WINDOW_HEIGHT, CORNER_X, CORNER_Y))
		self.title("Main Window")

		container = Frame(self)
		container.pack()

		self.frames = {}

		buttonQuit = Button(container, text="Exit", command=self.destroy)
		buttonQuit.pack(side="bottom")


if __name__=="__main__":
	app = MainWindow()
	app.mainloop()