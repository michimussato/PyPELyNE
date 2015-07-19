# pypelyne

3D animation pipeline software written in Python and Qt

under development...

Project features:
- versioning
- time tracking
- shot-/asset-based node trees
- use of central asset library
- automatic screen recording (i. e. for making of's/breakdowns)
- task locking (when it's in use by someone else)
- data flow visualization (re-useable data and dependencies)
- most tools can be integrated (flexible)
- written for os x and windows (windows not fully functional)
- arnold (ASS) render jobs can be sent directly from the pipeline to deadline render farm manager
- mantra (IFD) render jobs can be sent directly from the pipeline to deadline render farm manager
- meaningful usage of referenced data where possible (Maya, Cinema 4D, Nuke, Premiere etc.)
- maya loads pipeline inputs automatically (always work with latest data)
- double click in task starts the task with the latest project file (i. e. photoshop with the latest .psd-file)
- make users stick to a naming convention

Supports:
- Maya
- Houdini
- Cinema4D
- Realflow
- Nuke
- Fusion
- After Effects
- Premiere
- Photoshop
- Direct job submission to Thinkbox Deadline
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
