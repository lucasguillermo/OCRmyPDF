#!/usr/local/bin/python2
# coding: utf-8
##############################################################################
# Copyright (c) 2014: fritz-hh from Github (https://github.com/fritz-hh)
##############################################################################
class HocrCharsCategory():
	"""
	TODO
	"""
	# char list, lower boundary, upper boundary
	def __init__(self, charsstring, low, high):
		self.chars=charsstring
		self.low=low
		self.high=high
		
	def getLow(self):
		return self.low

	def getHigh(self):
		return self.high
	
	def hasCharFromCategory(self, text):
		return any(i in text for i in self.chars)