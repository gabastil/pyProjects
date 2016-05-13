#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Name: 	Web.py
# Version: 	1.0.0 
# Author: 	Glenn Abastillas
# Date: 	April 15 ,2016
#
# Purpose: Allows the user to:
#           1.) Retrieve webpages as with or without mark up
#
# To see the script run, go to the bottom of this page. 
#
# This class is not directly inherited by any other class.

import HTMLStripper
import urllib2

class Web(object):

	def __init__(self):
		pass

	def get(self, url=None, markup=True):
		"""	get a webpage as text
			@param	url: link to webpage
			@return	String text of webpage
		"""
		webpage = urllib2.urlopen(url).read()
		if markup:
			return webpage

		return HTMLStripper.HTMLStripper().strip(webpage)

	def getPages(self, *urls):
		"""	get webpages as text
			@param	*urls: link to webpages
			@return	List of String text of webpages
		"""
		webpages = list()
		append = webpages.append

		for url in urls:
			append(self.get(url))

		return webpages

if __name__=="__main__":
	url = u"http://www.google.com"
	w = Web()
	print w.get(url, markup=False)
	#print w.getPages(*[url, url2])