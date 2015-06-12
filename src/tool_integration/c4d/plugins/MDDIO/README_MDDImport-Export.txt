INSTALLATION
---------------------
Copy this folder to your plugins directory.

MDD EXPORT
-------------------
1. Use the Powerslider in C4D to set the loop start and loop end points to the range of frames you wish to export.
2. Select the object who's point-level changes you wish to export
3. Select Plugins -> MDDIO -> MDDExport
4. Choose the file for the MDD Data--filename defaults to the objects name plus ".mdd"

MDD IMPORT
-------------------
1. Position the play head on the frame where you want the imported frames to begin
2. Select the object to receive the imported animation.  It must match the point order and number of points of the recorded animation in the MDD file.
3. Select Plugins -> User Scripts -> MDDImport
4. Choose the file containing the MDD data to import.   PLA keyframes will be created for each imported frame.


MDD CONFIG
-------------------
1. You can set the scale factor for import/export (useful for scaling up/down .obj's into C4D's preferred space.)   Default is 1000.
2. For exporting a mesh's point deformations, the baking algorithm uses temporary objects with the name "MDDIOBakedObject999".   In the unlikely event that this name conflicts with an object name in your file, you can change it.   :)



NOTES
-------------------------------
1. If you plan to use .obj format, you will need Keith Young's Riptide plugin, due to C4D's baffling inability to maintain a proper point order.
    Riptide can be found here: http://skinprops.com/riptide.php


Copyright (c) 2007 by Kerwin Rabbitroo.
All Rights Reserved.

Enjoy!
-Kerwin
rabbitroo@mac.com

