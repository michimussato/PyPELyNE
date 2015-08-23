# PyPELyNE

3D animation pipeline software written in Python and Qt

under development...

I'm not a programmer, so the code structure might be a complete turn off for you...
Use it, but I'd be happy to get credited if you finish a project using PyPELyNE ;)

Project features:
- versioning
- quick cleanup of a project (i.e. removal of versions that are not being used anymore) (not yet fully functional)
- time tracking
- project traceability
- project documentation
- project achiving/unarchiving
- task check-in/check-out (i.e. to send tasks to home office freelancers) (not yet functional)
- connecting individual tools
- shot-/asset-based node trees
- single console for all processes with color coded output
- use of central asset library (not yet functional)
- automatic screen recording (i. e. for making of's/breakdowns with high compression)
- task locking (when it's in use by someone else)
- data flow visualization (reusable data and dependencies)
- most tools (with different version) can be integrated (flexible)
- written for OS X and Windows (Windows not yet functional)
- direct job submission to Deadline render farm for Arnold (ASS) and Mantra (IFD)
- meaningful usage of referenced data where possible (Maya, Cinema 4D, Nuke, Premiere etc.)
- maya loads task inputs automatically (always work with latest data)
- double click in task starts the task with the latest project file (i. e. PhotoShop with the latest .psd-file)
- make users stick to a naming convention
- create custom default scene/project files for each application version
- one button MP3 player (play, skip, stop, choose track out of a mp3 library)

Supports:
- Maya
- Mudbox
- Houdini
- Blender
- Cinema4D
- RealFlow
- Headus UVLayout
- Nuke
- ZBrush
- Fusion
- After Effects
- Premiere
- PhotoShop
- Direct job submission to ThinkBox Deadline
- Possibly any other tool can be integrated
- Different tool versions at the same time

Requires (tested with):
- Mac OS 10.6
- VLC 2.1.5 (included)
- Python 2.7.6
- Qt 4.8.5
- RV 4.0
- Thinkbox Deadline 5.2

Windows (not yet functional):
- python-2.7.8.msi
- PyQt4-4.11.3-gpl-Py2.7-Qt4.8.6-x32.exe
- pywin32-219.win32-py2.7.exe
- qt-opensource-windows-x86-mingw482-4.8.6-1.exe

Documentation:
- To do :(

Images:
Overview
![Overview](/gitImg/overview.png)

A node example with some in- and outputs
![Node](/gitImg/node.png)

A dialog of a nodes' output port
![dialog](/gitImg/dialog.png)

A completed asset (model, textures, shaders, rigs).
The yellow node is the asset output
![Asset](/gitImg/asset.png)

Above asset is being imported into another asset/shot i. e. for animation.
The yellow loader node is the output node from above asset (yellow saver).
Re-usable data.
![Re-used asset](/gitImg/reusedAsset.png)

A simple example of per process color coded output
i. e. if you're running several tasks/applications simultaneously
![console](/gitImg/console.png)

Deadline (render management software by Thinkbox) submitter.
Arnold and Mantra jobs are supported (automatic detection).
Automatic frame range detection.
All fields are filled in automatically, but can be altered if desired.
![deadlineSubmitter](/gitImg/deadlineSubmitter.png)

Youtube Preview:
[![Demo](/gitImg/demo.png)](https://www.youtube.com/watch?v=E1eQKEq-fcQ)

My demo reel:
[Reel](https://www.dropbox.com/s/lrhukj3f9l35c7a/MussatoMichael_DemoReel.mov?dl=0)