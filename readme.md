# Clipspeak


## Informations
* Authors: "Rui Fontes, Ângelo Abrantes, Abel Passos Júnior and colaboration of Noelia Ruiz Martínez, based on the work of Damien Sykes-Lindley
* Updated in 16/05/2023
* Download [stable version][1]
* Compatibility: NVDA version 2019.3 and beyond


## Presentation
Clipspeak is an addon that allows NVDA to automatically announce clipboard operations (such as cut, copy and paste), along with other common editing operations such as undo and redo.
In order to prevent announcement in inappropriate situations, Clipspeak performs checks on the control and the clipboard in order to make an informed decision as to whether such an announcement is necessary.
You can choose between only announcing copy/cut/paste or also whats is being copied/cutted/pasted on NVDA, configurations, clipspeak.
By default, Clipspeak's gestures are mapped to those commonly used by English versions of Windows:
* CTRL+Z: Undo
* CTRL+Y: Redo
* CTRL+X: Cut
* CTRL+C: Copy
* CTRL+V: Paste

If these are not the shortcuts commonly used for these tasks on your version of Windows, you will need to remap these gestures in the input gestures configuration under the Clipboard category.


[1]: https://github.com/ruifontes/clipspeak/releases/download/2023.05.16/clipspeak-2023.05.16.nvda-addon
