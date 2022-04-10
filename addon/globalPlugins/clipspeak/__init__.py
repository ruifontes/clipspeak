# -*- coding: utf-8 -*-
# Clipspeak
# An addon to monitor and speak messages relating to clipboard operations
# By: Damien Lindley Created: 19th April 2017
# Modified by Rui Fontes, Ângelo Miguel and Abel Júnior in 26/03/2022
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import globalPluginHandler
import globalVars
import ui
import api
import inputCore
import scriptHandler
from scriptHandler import script
from logHandler import log
import controlTypes
if hasattr(controlTypes, "Role"):
	for r in controlTypes.Role: setattr(controlTypes, r.__str__().replace("Role.", "ROLE_"), r)
else:
	setattr(controlTypes, "Role", type('Enum', (), dict([(x.split("ROLE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("ROLE_")])))

if hasattr(controlTypes, "State"):
	for r in controlTypes.State: setattr(controlTypes, r.__str__().replace("State.", "STATE_"), r)
else:
	setattr(controlTypes, "State", type('Enum', (), dict([(x.split("STATE_")[1], getattr(controlTypes, x)) for x in dir(controlTypes) if x.startswith("STATE_")])))

from . import clipboard_monitor
# For update process
from .update import *
import addonHandler
addonHandler.initTranslation()

# Constants:

# Clipboard content: What are we working with?
cc_none=0
cc_text=1
cc_read_only_text=2
cc_file=3
cc_list=4
cc_other=5
cc_file1=6

# Clipboard mode: What are we doing?
cm_none=0
cm_cut=1
cm_copy=2
cm_paste=3

# Not strictly clipboard, but...
cm_undo=4
cm_redo=5

cc_last_flag = ""
cc_last_flag_1 = ""


class GlobalPlugin(globalPluginHandler.GlobalPlugin):	
	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self):
		# Call of the constructor of the parent class.
		super(globalPluginHandler.GlobalPlugin, self).__init__()

		# Adding a NVDA configurations section
		gui.NVDASettingsDialog.categoryClasses.append(ClipSpeakSettingsPanel)

		# To allow waiting end of network tasks
		core.postNvdaStartup.register(self.networkTasks)

	def networkTasks(self):
		# Calling the update process...
		_MainWindows = Initialize()
		_MainWindows.start()

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		core.postNvdaStartup.unregister(self.networkTasks)
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(ClipSpeakSettingsPanel)

	# Script functions:

	@script( 
	# For translators: Message to be announced during Keyboard Help 
	description = _("Cut selected item to clipboard, if appropriate."), 
	# For translators: Name of the section in "Input gestures" dialog. 
	category = _("Clipboard"), 
	gesture = "kb:Control+X")
	def script_cut(self, gesture):
		log.debug("Script activated: Cut.")
		log.debug("Processing input gesture.")
		if self.process_input(gesture):
			return
		log.debug("Speaking message.")
		self.speak_appropriate_message(cm_cut)

	@script( 
	# For translators: Message to be announced during Keyboard Help 
	description = _("Copy selected item to clipboard, if appropriate."), 
	# For translators: Name of the section in "Input gestures" dialog. 
	category = _("Clipboard"), 
	gesture = "kb:Control+C")
	def script_copy(self, gesture):
		log.debug("Script activated: Copy.")
		log.debug("Processing input gesture.")
		if self.process_input(gesture):
			return
		log.debug("Speaking message.")
		self.speak_appropriate_message(cm_copy)

	@script( 
	# For translators: Message to be announced during Keyboard Help 
	description = _("Paste item from clipboard, if appropriate."), 
	# For translators: Name of the section in "Input gestures" dialog. 
	category = _("Clipboard"), 
	gesture = "kb:Control+V")
	def script_paste(self, gesture):
		log.debug("Script activated: Paste.")
		log.debug("Processing input gesture.")
		if self.process_input(gesture):
			return
		log.debug("Speaking message.")
		self.speak_appropriate_message(cm_paste)

	@script( 
	# For translators: Message to be announced during Keyboard Help 
	description = _("Undo operation."),
	# For translators: Name of the section in "Input gestures" dialog. 
	category = _("Clipboard"), 
	gesture = "kb:Control+Z")
	def script_undo(self, gesture):
		log.debug("Script activated: Undo.")
		log.debug("Processing input gesture.")
		if self.process_input(gesture):
			return
		log.debug("Speaking message.")
		self.speak_appropriate_message(cm_undo)

	@script( 
	# For translators: Message to be announced during Keyboard Help 
	description = _("Redo operation."),
	# For translators: Name of the section in "Input gestures" dialog.
	category = _("Clipboard"), 
	gesture = "kb:Control+Y")
	def script_redo(self, gesture):
		log.debug("Script activated: Redo.")
		log.debug("Processing input gesture.")
		if self.process_input(gesture):
			return
		log.debug("Speaking message.")
		self.speak_appropriate_message(cm_redo)

	# Internal functions: Examines our environment so we can speak the appropriate message.
	def process_input(self, gesture):
		log.debug("Evaluating possible gestures.")
		scripts=[]
		maps=[inputCore.manager.userGestureMap, inputCore.manager.localeGestureMap]

		log.debug("Found gesture mapping: \r"%maps)
		log.debug("Enumerating scripts for these maps.")
		for map in maps:
			log.debug("Enumerating gestures for map %r"%map)
			for identifier in gesture.identifiers:
				log.debug("Enumerating scripts for gesture %r"%identifier)
				scripts.extend(map.getScriptsForGesture(identifier))

		log.debug("Found scripts: %r"%scripts)

		focus=api.getFocusObject()
		log.debug("Examining focus: %r"%focus)
		tree=focus.treeInterceptor
		log.debug("Examining tree interceptor: %r"%tree)

		log.debug("Checking tree interceptor state.")
		if tree and tree.isReady:

			log.debug("Tree interceptor in use. Retrieving scripts for the interceptor.")
			func=scriptHandler._getObjScript(tree, gesture, scripts)
			log.debug("Examining object: %r"%func)

			log.debug("Examining function attributes.")
			if func and (not tree.passThrough or getattr(func,"ignoreTreeInterceptorPassThrough",False)):

				log.debug("This gesture is already handled elsewhere. Executing associated function.")
				func(tree)
				return True

		log.debug("Nothing associated here. Pass straight to the system.")
		gesture.send()
		return False

	def speak_appropriate_message(self, cm_flag):
		cc_flag = self.examine_focus()
		# Todo: If we can validate whether or not a control can work with the clipboard, we can return an invalid message here.
		log.debug("Finding appropriate message for clipboard content type: %r"%cc_flag)
		if cc_flag==cc_none:
			return
		if cc_flag == cc_text:
			# Pick a word suitable to the content.
			try:
				text = api.getClipData()
				if len(text) < 500:
					text = text
				else:
					text = _("%s characters")%len(text)
				word1 = _(text)
			except:
				pass #text = ""
		elif cc_flag==cc_file:
			# Translators: A single word representing a file.
			word=_("file")

		elif cc_flag==cc_list:
			# Translators: A single word representing an item in a list.
			word=_("item")

		# Decide what will be announced...
		if config.conf[ourAddon.name]["announce"]:
			word = word1 = ""

		# Validate and speak.
		log.debug("Validating clipboard mode: %r"%cm_flag)

		if cm_flag==cm_undo and self.can_undo(cc_flag):
			# Translators: Message to speak when undoing.
			ui.message(_("Undo"))

		if cm_flag==cm_redo and self.can_redo(cc_flag):
			# Translators: A message spoken when redoing a previously undone operation.
			ui.message(_("Redo"))

		if cm_flag==cm_cut and self.can_cut(cc_flag):
			if cc_flag == cc_text:
				# Translators: A message to speak when cutting text to the clipboard.
				ui.message(_("Cut: %s")%word1)
			else:
				# Translators: A message to speak when cutting an item to the clipboard.
				ui.message(_("Cut %s")%word)
			if cc_flag == cc_file1:
				pass

		if cm_flag==cm_copy and self.can_copy(cc_flag):
			if cc_flag == cc_text:
				# Translators: A message spoken when copying text to the clipboard.
				ui.message(_("Copy: %s")%word1)
			else:
				# Translators: A message spoken when copying to the clipboard.
				ui.message(_("Copy %s")%word)
			if cc_flag == cc_file1:
				pass

		if cm_flag==cm_paste and self.can_paste(cc_flag):
			if cc_flag == cc_text:
				# Translators: A message spoken when pasting text from the clipboard.
				ui.message(_("Pasted: %s")%word1)
			else:
				# Translators: A message spoken when pasting from the clipboard.
				ui.message(_("Pasted %s")%word)

	def examine_focus(self):
		global cc_last_flag, cc_last_flag_1
		cc_last_flag_1 = cc_last_flag
		focus=api.getFocusObject()
		if not focus:
			cc_last_flag = cc_none
			return cc_none
		log.debug("Examining focus object: %r"%focus)
		# Retrieve the control's states and roles.
		states=focus.states

		# Check for an explorer/file browser window.
		# Todo: Is this an accurate method?
		if (focus.windowClassName == "DirectUIHWND"):
			if  controlTypes.STATE_SELECTED in states:
				cc_last_flag = cc_file
				return cc_file
			elif  controlTypes.STATE_SELECTABLE in states:
				cc_last_flag = cc_file1
				return cc_file1

		# Check for a list item.
		elif (focus.role == controlTypes.ROLE_LISTITEM or controlTypes.ROLE_TABLEROW) and controlTypes.STATE_SELECTED in states:
			cc_last_flag = cc_list
			return cc_list

		# Check if we're looking at text.
		elif (controlTypes.STATE_EDITABLE or controlTypes.STATE_MULTILINE) in states:
			if controlTypes.STATE_READONLY in states:
				cc_last_flag = cc_read_only_text
				return cc_read_only_text
			else:
				# Otherwise, we're just an ordinary text field.
				log.debug("Field seems to be editable.")
				cc_last_flag = cc_text
				return cc_text

		# For some reason, not all controls have an editable state, even when they clearly are.
		elif focus.role==controlTypes.ROLE_EDITABLETEXT:
			if controlTypes.STATE_READONLY in states:
				cc_last_flag = cc_read_only_text
				return cc_read_only_text
			else:
				# Otherwise, we're just an ordinary text field.
				log.debug("Field seems to be editable.")
				cc_last_flag = cc_text
				return cc_text
		elif focus.windowClassName == "RichEditD2DPT":
			cc_last_flag = cc_text
			return cc_text
		# Todo: Other control types we need to check?
		else:
			log.debug("Control type would not suggest clipboard operations.")
			cc_last_flag = cc_none
			return cc_none

	# Validation functions: In case we need to extend the script to allow more control/window types etc.
	# Todo: Can we check a control to see if it enables these operations? For instance whether a list enables copy or a text field allows select all?
	def can_undo(self, cc_flag):
		if cc_flag==cc_read_only_text:
			return False
		return True

	def can_redo(self, cc_flag):
		if cc_flag==cc_read_only_text:
			return False
		return True

	def can_cut(self, cc_flag):
		if cc_flag==cc_read_only_text:
			return False
		# Todo: Validate the control and make sure there is something that could potentially be cut.
		if cc_last_flag == cc_file1:
			return False
		return True

	def can_copy(self, cc_flag):
		# Todo: Validate the control and make sure there is something that could potentially be copied.
		if cc_last_flag == cc_file1:
			return False
		return True

	def can_paste(self, cc_flag):
		global cc_last_flag, cc_last_flag_1
		focus=api.getFocusObject()
		states=focus.states
		if cc_last_flag_1 == cc_none:
			cc_flag = cc_none
			return False
		elif cc_last_flag_1 == cc_text:
			cc_flag = cc_text
			# Check if we're looking at text.
			if (controlTypes.STATE_EDITABLE or controlTypes.STATE_MULTILINE) in states:
				if controlTypes.STATE_READONLY in states:
					return False
				else:
					# Otherwise, we're just an ordinary text field.
					log.debug("Field seems to be editable.")
					return True
			# For some reason, not all controls have an editable state, even when they clearly are.
			elif focus.role==controlTypes.ROLE_EDITABLETEXT:
				return True
			elif controlTypes.STATE_READONLY in states:
				return False
			elif focus.windowClassName == "RichEditD2DPT":
				return True

		elif cc_last_flag_1 == (cc_file or cc_file1):
			cc_flag = cc_file
			# Check for an explorer/file browser window.
			# Todo: Is this an accurate method?
			if focus.windowClassName == "DirectUIHWND":
				if  (focus.role==controlTypes.ROLE_LISTITEM) and controlTypes.STATE_SELECTABLE in states:
					return True
				return False
			return False

		elif cc_last_flag_1 == cc_list:
			# Check for a list item.
			if (focus.role == controlTypes.ROLE_LISTITEM or controlTypes.ROLE_TABLEROW) and controlTypes.STATE_SELECTED in states:
				cc_flag = cc_list
				return True

	# Define an object of type clipboard_monitor that will keep track of the clipboard for us.
	__clipboard = clipboard_monitor.clipboard_monitor()


if globalVars.appArgs.secure:
	# Override the global plugin to disable it.
	GlobalPlugin = globalPluginHandler.GlobalPlugin


class ClipSpeakSettingsPanel(gui.SettingsPanel):
	# Translators: Title of the ClipSpeak settings dialog in the NVDA settings.
	title = _("ClipSpeak")

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer = settingsSizer)

		# Translators: Checkbox name in the configuration dialog
		self.announceWnd = sHelper.addItem(wx.CheckBox(self, label=_("Announce only copy/cut/paste")))
		self.announceWnd.SetValue(config.conf[ourAddon.name]["announce"])

		# Translators: Checkbox name in the configuration dialog
		self.shouldUpdateChk = sHelper.addItem(wx.CheckBox(self, label=_("Check for updates at startup")))
		self.shouldUpdateChk.SetValue(config.conf[ourAddon.name]["isUpgrade"])
		if config.conf.profiles[-1].name:
			self.shouldUpdateChk.Disable()

	def onSave (self):
		config.conf[ourAddon.name]["announce"] = self.announceWnd.GetValue()
		if not config.conf.profiles[-1].name:
			config.conf[ourAddon.name]["isUpgrade"] = self.shouldUpdateChk.GetValue()

