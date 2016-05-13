#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     CommandLineArguments.py
# Version:  1.0.0
# Author:   Glenn Abastillas
# Date:     April 29, 2016
#
# Purpose: Allows the user to:
#           1.) Show a progress bar given location in a process
#
# To see the script run, go to the bottom of this page.
#
# This class is used in the following classes:
#	FindDebrid
#	Analyze
# - - - - - - - - - - - - -
import sys

class CommandLineArguments(object):

	def __init__(self):
		"""	initialize object with arguments from command line
		"""
		arguments = sys.argv
		self.argHashTable = dict()
		self.argList = list()
		#print arguments

		iteration_index = 1
		arguments_length = len(arguments)

		# Loop through the arguments to get optional and ordinal arguments
		for arg in arguments[1:]:
			
			# Assign a previous argument if there is one
			prevArg=None
			if iteration_index > 1:
				prevArg=arguments[iteration_index-1]

			# Assign a next argument if not at end of list
			nextArg=None
			if iteration_index < arguments_length-1:
				nextArg=arguments[iteration_index+1]

			# If this arg is a flag (i.e., begins with '-'), map to nextArg
			if arg[0]=='-':
				self.argHashTable[arg]=nextArg

			# If the prevArg is not an option, save this arg as a positional argument
			elif prevArg[0]!='-':
				self.argList.append(arg)

			prevArg=None
			nextArg=None
			iteration_index += 1

	def getopt(self, option):
		"""	return argument for flag
			@param	option:	argument flag
			@return	String of argument
		"""
		try:
			return self.argHashTable[option]
		except(KeyError):
			return None

	def get(self, index):
		""" return positional argument
			@param	index: argument index in command line excluding script name
			@return	String of argument
		"""
		try:
			return self.argList[index]
		except(IndexError):
			return None

if __name__=="__main__":
	cla = CommandLineArguments()
	print cla.getopt("-i")
	print cla.getopt("-o")
	print cla.getopt("-m")
	print cla.get(5)
