# -*- coding: UTF-8 -*-
# Module for clipspeak settings panel
# written by Rui Fontes <rui.fontes@tiflotecnia.com>, Ângelo Abrantes <ampa4374@gmail.com> and Abel Passos do Nascimento Jr. <abel.passos@gmail.com>
# Copyright (C) 2023 Rui Fontes <rui.fontes@tiflotecnia.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Import the necessary modules
import os
import gui
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper
import wx
import globalVars
import config
from configobj import ConfigObj
import addonHandler

# To start translation process
addonHandler.initTranslation()

def initConfiguration():
	confspec = {
		"announce": "boolean(default=true)",
	}
	config.conf.spec["clipspeak"] = confspec

initConfiguration()


class ClipSpeakSettingsPanel(gui.SettingsPanel):
	# Translators: Title of the ClipSpeak settings dialog in the NVDA settings.
	title = _("ClipSpeak")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer = settingsSizer)

		# Translators: Checkbox name in the configuration dialog
		self.announceWnd = sHelper.addItem(wx.CheckBox(self, label=_("Announce only copy/cut/paste")))
		self.announceWnd.SetValue(config.conf["clipspeak"]["announce"])

	def onSave (self):
		config.conf["clipspeak"]["announce"] = self.announceWnd.GetValue()

	def onPanelActivated(self):
		# Deactivate all profile triggers and active profiles
		config.conf.disableProfileTriggers()
		self.Show()

	def onPanelDeactivated(self):
		# Reactivate profiles triggers
		config.conf.enableProfileTriggers()
		self.Hide()
