#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Name:     ProgressBar.py
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

class ProgressBar(object):

	def printProgress(self, iteration, total, prefix="", suffix="", sign=u'\u2588', blank=u'\u2591', decimals=2, barLength=20):
		"""	print a progress bar to the console
			@param	iteration: index of current task
			@param	total: total number of tasks
			@param	prefix: Left title of progress bar
			@param	suffix: Right title of progress bar
			@param	sign: indicator for completed work
			@param	blank: indicator for incomplete work
			@param	decimals: significant digits to round off to
			@param	barLength: total length of progress bar
			@param	appearance: appearance of progress bar
		"""
		prefix = prefix.ljust(15, '.')
		prefix = prefix[:15]

		appearance=u"   {0} {1} {2}% {3}\r"
		fillLength = int(round(barLength*iteration/float(total)))
		percent = round(100.00*(iteration/float(total)))
		bar = sign * fillLength + blank * (barLength - fillLength)
		#print int(percent) %3
		#if int(percent)%2==0:
		sys.stdout.write(appearance.format(prefix, bar, str(percent), suffix))
		sys.stdout.flush()

		if iteration==total:
			print appearance.format(prefix, sign*barLength, str(percent), "Process Completed!")
			print '\n'

if __name__=="__main__":
	items = range(10000)
	i = 0
	l = len(items)

	for item in items:
		ProgressBar().printProgress(i,l)
		i+=1
