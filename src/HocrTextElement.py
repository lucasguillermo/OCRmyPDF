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
	
	# initialize the character categories assuming helvetica font
	hocrCharsCategories=[HocrCharsCategory(u"acemnorsuvwxz:", 0, 0.55), 
				HocrCharsCategory(u"bdfhikltABCDEFGHIJLKMNOPQRSTUVWXYZâàéèêîôù0123456789!/%?\ß€#", 0, 0.75),
				HocrCharsCategory(u"gpqyµ", -0.25, 0.55),
				HocrCharsCategory(u"j§{([)]}|@", -0.25, 0.75),
				HocrCharsCategory(u"üöä", 0, 0.7),
				HocrCharsCategory(u"ÉÈÊÔÎ", 0, 1),
				HocrCharsCategory(u",", -0.15, 0.05)]
				
	
	def __init__(self, pdf, text, x1, y1, x2, y2):
		self.fontname="Helvetica"
		self.pdf=pdf
		self.x1=x1		# position in pt
		self.y1=y1
		self.x2=x2
		self.y2=y2
		self.textClean = HocrTextElement.cleanText(text)
		
	def getText(self):
		# Compute string vertical boundaries
		allCharsUnknown=1
		lowBound=+0.5
		highBound=-0.5
		for cat in HocrTextElement.hocrCharsCategories:
			if cat.hasCharFromCategory(self.textClean):
				allCharsUnknown=0
				lowBound=min(cat.getLow(), lowBound)
				highBound=max(cat.getHigh(), highBound)
				
		text = self.pdf.beginText()				
		# Compute font size
		# fine tune according to the characters contained in the current text element
		fontsize=abs(self.y2 - self.y1) / abs(highBound-lowBound)
		text.setFont(self.fontname, fontsize)
		
		# Set cursor to bottom left corner of bbox
		# fine tune according to the characters contained in the current text element
		text.setTextOrigin(self.x1, self.y1 - lowBound * fontsize)

		# Scale the width of the text to fill accurately the width of the bbox
		text.setHorizScale(100*(self.x2-self.x1)/self.pdf.stringWidth(self.textClean, self.fontname, fontsize))

		# Write the text into the text element
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
