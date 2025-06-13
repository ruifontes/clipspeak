# -*- coding: utf-8 -*-
# clipboardMonitor.py
# A clipspeak module to monitor for clipboard content using wxPython
# By: Rui Fontes and Ângelo Abrantes, with cooperation of ChatGPT from OpenAI
# Thanks to Dalen <dbernaca@gmail.com> for alerting to WX capacity of handling clipboard...
# Copyright (C) 2024 Rui Fontes <rui.fontes@tiflotecnia.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Import the necessary modules
import wx
import os
from time import sleep
from datetime import datetime
import addonHandler
# Starting translation process
addonHandler.initTranslation()

textContent = ""
tempContent = ""


class clipboardMonitor(object):
	#def __init__(self):
		#self.getClipboard()

	def getClipboard(self):
		clipboard = wx.Clipboard.Get()
		try:
			clipboard.Open()
		except Exception:
			sleep(0.10)
			clipboard.Open()
		try:
			if clipboard.IsSupported(wx.DataFormat(wx.DF_FILENAME)):
				file_data = wx.FileDataObject()
				clipboard.GetData(file_data)
				paths = file_data.GetFilenames()
				return paths
			elif clipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
				text_data = wx.TextDataObject()
				clipboard.GetData(text_data)
				text = text_data.GetText()
				return text
			return None
		finally:
			clipboard.Close()

	def validClipboardData(self):
#		sleep(0.09)
		comparison = self.getClipboard()
		if comparison is None:
			return 0, None

		if isinstance(comparison, list):  # Assuming list of file paths
			if len(comparison) == 1:
				text = _("file/folder ") + os.path.basename(comparison[0])
			elif len(comparison) <= 3:
				file_names = [os.path.basename(path) for path in comparison]
				names = "; ".join(file_names)
				text = _("files/folders: ") + names
			else:
				text = str(len(comparison)) + _(" files/folders")
			return 1, text
		elif isinstance(comparison, str):
			if len(comparison) < 1024:
				text = comparison
			else:
				text = "%s characters" % len(comparison)
			return 2, text

	def clipboardHasChanged(self):
		global textContent, tempContent
		tempContent = str(self.getClipboard()) + datetime.now().strftime("%H:%M:%S.%f")
		if tempContent != textContent:
			self.resetTextContent()
			return True
		else:
			return False

	def resetTextContent(self):
		global textContent, tempContent
		textContent = tempContent
