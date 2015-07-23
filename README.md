# pypelyne

3D animation pipeline software written in Python and Qt

under development...

Project features:
- versioning
- time tracking
- shot-/asset-based node trees
- single console for all processes with color coded output
- use of central asset library
- automatic screen recording (i. e. for making of's/breakdowns with high compression)
- task locking (when it's in use by someone else)
- data flow visualization (reusable data and dependencies)
- most tools can be integrated (flexible)
- written for OS X and Windows (Windows not fully functional)
- direct job submission to Deadline render farm for Arnold (ASS) and Mantra (IFD)
- meaningful usage of referenced data where possible (Maya, Cinema 4D, Nuke, Premiere etc.)
- maya loads task inputs automatically (always work with latest data)
- double click in task starts the task with the latest project file (i. e. PhotoShop with the latest .psd-file)
- make users stick to a naming convention

Supports:
- Maya
- Houdini
- Cinema4D
- RealFlow
- Nuke
- Fusion
- After Effects
- Premiere
- PhotoShop
- Direct job submission to ThinkBox Deadline
- Possibly any other tool can be integrated

Requires (tested with):
- Mac OS 10.6
- VLC 2.5.1
- Python 2.7.6
- Qt 4.8.5

Windows (not yet functional):
- python-2.7.8.msi
- PyQt4-4.11.3-gpl-Py2.7-Qt4.8.6-x32.exe
- pywin32-219.win32-py2.7.exe
- qt-opensource-windows-x86-mingw482-4.8.6-1.exe
