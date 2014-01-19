#!/usr/local/bin/python2
# coding: utf-8
##############################################################################
# Copyright (c) 2014: fritz-hh from Github (https://github.com/fritz-hh)
##############################################################################
from reportlab.pdfgen.canvas import Canvas
from HocrCharsCategory import HocrCharsCategory

class HocrTextElement():
	"""
	A class representing a text element (ocr_line and ocrx_word) from the hOCR format.
	For details of the hOCR format, see:
	http://docs.google.com/View?docid=dfxcv4vc_67g844kf
	"""
	
	# initialize the character categories
	cat1=HocrCharsCategory(u"acemnorsuvwxz:", 0, 0.5)
	cat2=HocrCharsCategory(u"bdfhikltABCDEFGHIJLKMNOPQRSTUVWXYZâàéèêîôù0123456789!/%?\ß€#", 0, 0.75)
	cat3=HocrCharsCategory(u"gpqyµ", -0.25, 0.75)
	cat4=HocrCharsCategory(u"j§{([)]}|@", -0.25, 1)
	cat5=HocrCharsCategory(u"üöä", 0, 0.7)
	cat6=HocrCharsCategory(u"ÉÈÊÔÎ", 0, 1)
	cat7=HocrCharsCategory(u",", -0.15, 0.05)
	
	
	def __init__(self, pdf, text, x1, y1, x2, y2):
		self.fontname="Helvetica"
		self.pdf=pdf
		self.x1=x1		# position in pt
		self.y1=y1
		self.x2=x2
		self.y2=y2
		self.textClean = HocrTextElement.cleanText(text)
		
	def getText(self):
		text = self.pdf.beginText()

		# Compute string vertical boundaries
		lowBound=+0.5
		highBound=-0.5
		boundaries=HocrTextElement.cat7.getNewBoundaries(self.textClean, HocrTextElement.cat4.getNewBoundaries(self.textClean, HocrTextElement.cat3.getNewBoundaries(self.textClean, HocrTextElement.cat2.getNewBoundaries(self.textClean,HocrTextElement.cat1.getNewBoundaries(self.textClean,(lowBound, highBound))))))
		lowBound=boundaries[0]
		highBound=boundaries[1]
		
		# set font size
		fontsize=abs(self.y2 - self.y1) / abs(highBound-lowBound)
		text.setFont(self.fontname, fontsize)
		
		# set cursor to bottom left corner of bbox (adjust for dpi)
		text.setTextOrigin(self.x1, self.y1 - lowBound * fontsize)

		# scale the width of the text to fill accurately the width of the bbox
		text.setHorizScale(100*(self.x2-self.x1)/self.pdf.stringWidth(self.textClean, self.fontname, fontsize))

		# write the text to the page
		text.textLine(self.textClean)
	
		return text
	
	@staticmethod
	def cleanText(str):
		"""
		Given an input string, returns the corresponding string that:
		- is available in the helvetica facetype
		- does not contain any ligature (to allow easy search in the PDF file)
		"""		
		# The 'u' before the character to replace indicates that it is a unicode character
		str=str.replace(u"ﬂ","fl")
		str=str.replace(u"ﬁ","fi")
		return str
