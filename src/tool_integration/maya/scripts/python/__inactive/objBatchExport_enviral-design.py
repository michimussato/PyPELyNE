######################################################
## Mass OBJ exporter script (python)                ##
##--------------------------------------------------##
## Script Written by Lucas morgan.                  ##
##--------------------------------------------------##
## Email: lucasm@enviral-design.com                 ##
##--------------------------------------------------##
## Website: www.enviral-design.com                  ##
######################################################

# - Installation
## To run this script, copy all of the text in this
## window into the python tab of your maya script editor.

# - Usage
## 1. Select all polygon mesh objects in scene
## 2. Choose directory
## 3. BAM!

## Note: exporting anything other than polys may result in empty objs, or an error.

####----------------------------------------------####

import maya.cmds as cmds
import maya.mel as mel

#deletes old window and preference, if it still exists
if(cmds.window('uiWindow_objLoopExport', q=1, ex=1)):
     cmds.deleteUI('uiWindow_objLoopExport')
if(cmds.windowPref('uiWindow_objLoopExport', q=1, ex=1)):
     cmds.windowPref('uiWindow_objLoopExport', r=1)
    
def dirPath(filePath, fileType):
     cmds.textFieldButtonGrp('Dir', edit=True, text=str(filePath))
     return 1

def startExport(path):
     curentObjectSelection = cmds.ls(sl=1,fl=1)
     filePathStr = cmds.textFieldButtonGrp('Dir', query = True, text = True)
     filePrfx = cmds.textField('Prfx', query = True, text = True)
     for item in curentObjectSelection:
          finalExportPath = "%s/%s__%s.obj"%(filePathStr, filePrfx, item)
          try:
               cmds.select(item)
               mel.eval('file -force -options "groups=0;ptgroups=0;materials=0;smoothing=1;normals=1" -typ "OBJexport" -pr -es "%s";'%(finalExportPath))
               print finalExportPath
          except:
               print "Ignoring object named: '%s'. Export failed, probably not a polygonal object. "%(item)
     print "Exporting Complete!"

def browseIt():
     cmds.fileBrowserDialog( m=4, fc=dirPath, ft='directory', an='Choose Directory')
     return

def makeGui():
     uiWindow_objLoopExport = cmds.window('uiWindow_objLoopExport', title="Mass OBJ exporter", iconName='uiWindow_objLoopExport', widthHeight=(330, 160) )
     cmds.columnLayout('uiColWrapper', w = 375, adjustableColumn=False, parent = 'uiWindow_objLoopExport' )
     cmds.text( label='Settings', align='left', parent = 'uiColWrapper')
     cmds.textFieldButtonGrp('Dir', label='Directory Path', cw3 = [80,190,50], text='(browse for directory)', buttonLabel='browse', buttonCommand=browseIt, parent = 'uiColWrapper')
     cmds.textField('Prfx', width=330, text='(prefix for export, i.e. set name)', parent = 'uiColWrapper')
     cmds.button('startExport', label = "Export Selected", parent = 'uiColWrapper', width = 322, command = startExport)
     cmds.showWindow( uiWindow_objLoopExport )


makeGui()