# -*- coding: UTF-8 -*-
# Copyright (C) 2023 Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr <abel.passos@gmail.com>"
# Install tasks module based on the work of Asociación Comunidad Hispanohablante de NVDA <contacto@nvda.es> and Paul Ber <paulber19@laposte.net>
# The purpose is deactivate the feature of clipboard actions announcement of NVDAExtensionGlobalPlugin add-on to avoid conflicts.
# This file is covered by the GNU General Public License.

import gui
import wx
import os
import sys
import globalVars
import addonHandler
addonHandler.initTranslation()



def onInstall():
	for addon in addonHandler.getAvailableAddons():
		if addon.name == "NVDAExtensionGlobalPlugin" and not addon.isDisabled:
			result = gui.messageBox(
				# Translators: message asking the user wether the clipboard announcements feature of NVDAExtensionGlobalPlugin should be disabled or not
				_("NVDAExtensionGlobalPlugin has been detected on your system. In order for Clipspeak to work without conflicts, this feature must be disabled. Otherwise Clipspeake will not work. Would you like to disable this feature now?"),
				# Translators: question title
				_("Running NVDAExtensionGlobalPlugin detected"),
				wx.YES_NO|wx.ICON_QUESTION, gui.mainFrame)
			if result == wx.YES:
				NVGEP_IniFile = os.path.join(globalVars.appArgs.configPath, "NVDAExtensionGlobalPluginAddon.ini")
				with open(NVGEP_IniFile, "r", encoding = "utf-8") as file:
					options = file.readlines()
					newOptions = []
					option = "FakeClipboardAnnouncement"
					for line in options:
						if option in line:
							print(line)
							line = line[0:-2] + "0\n"
							print(line)
						print("linha é " + line)
						newOptions.append(line)
					print(str(len(newOptions)) + str(newOptions))
					file.close()
				with open(NVGEP_IniFile, "w", encoding = "utf-8") as file:
					#file.clear()
					for line in newOptions:
						file.write(line)
					file.close()
			return
