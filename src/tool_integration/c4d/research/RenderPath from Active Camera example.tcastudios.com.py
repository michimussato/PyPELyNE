'''
from http://forums.cgsociety.org/archive/index.php/t-1083625.html

Each house needs its specific workflow so it's pretty
hard to set up a generic solution.
Python does give pretty much options "for free".

For inspiration, attached is a Save path system
based on a Project Folder with automatic subfolders
for Document name (Scene), active Camera name, image name
as well as a Multipass folder (based on the same criteria).

For use in the ScriptManager.

(As usual, watch out for any formatting errors by the forum text engine)

Cheers
Lennart


# RenderPath from Active Camera example.tcastudios.com � 2012
#
# Paste all into the ScriptManager.
#
# Start with an empty Save path.
# Run the script and select a image Name and Project Folder.
# Each time you run the script the Save path will be set
# to this Project folder and use/create subfolders based on:
# Document Name and Active Camera Name
# where the current render will be rendered into,
# incl. a Multipass folder if Multipass is activated.
#
# Saving the Scene with a new name will make a new
# subfolder structure in your Project folder
# named after the New scene name, again adding subfolders
# based on Active Camera.
#
# To create a new Project folder, empty the Save path in render settings
# and run the script.

'''

import c4d
from c4d import gui, storage as s
import os, errno

DEFAULT_NAME = 'Image Name 01'

def mkdirs(newdir, mode=0777):
    try: 
        os.makedirs(newdir, mode)
    except OSError, err:
        # Reraise the error unless it's about an already existing directory 
        if err.errno != errno.EEXIST or not os.path.isdir(newdir): 
            raise

def main():
    c4d.CallCommand(13957) # Clear Console

adraw = doc.GetActiveBaseDraw()
camname = adraw.GetSceneCamera(doc).GetName()
if camname == 'Camera':
camname = 'Ed_Camera'

docname = doc.GetDocumentName()
docname,ext = os.path.splitext(docname)

current_path = doc.GetActiveRenderData()[c4d.RDATA_PATH]
c_cam, current_image = os.path.split(current_path)
c_scene, current_cam = os.path.split(c_cam)
c_proj, current_scene = os.path.split(c_scene)
c_path, current_project = os.path.split(c_proj)

mpass = doc.GetActiveRenderData()[c4d.RDATA_MULTIPASS_SAVEIMAGE]


print '_CURRENT SETTINGS___________'
print '[Filepath] %s' %(current_path)
if mpass:
print '[MP_path] %s' %(doc.GetActiveRenderData()[c4d.RDATA_MULTIPASS_FILENAME])
print '[Project ] %s' %(current_project)
print '[Scene ] %s' %(current_scene)
print '[Camera] %s' %(current_cam)
print '[Image ] %s' %(current_image)

try: projd = c_proj
except: projd = c4d.DOCUMENT_FILEPATH

folder = c_proj
if not current_path:
# Initially set up a project Save path based on document(Scene), Active camera name
print 'Need to set a New Project Save path'
folder = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select Project Folder',c4d.FILESELECT_DIRECTORY,'',projd)
if not folder: return 

prename = current_image if current_image else DEFAULT_NAME
saveas = c4d.gui.RenameDialog(prename) # Set/Update Image name
if not saveas:
return True

# Set up the Save path based on Project, document(Scene), Active camera names and Image name
if not current_path or current_scene != docname or current_cam != camname or current_image != saveas:
print 'Setting a New Save path'

dpath = os.path.join(folder,docname,camname)
mkdirs(dpath, mode=0777)
newpath = os.path.join(dpath,saveas)
doc.GetActiveRenderData()[c4d.RDATA_PATH] = newpath

# If MultiPass Save is On
if mpass: 
new_mp_path = os.path.join(os.path.split(newpath)[0],saveas+'_mp')
mkdirs(new_mp_path, mode=0777)
multipass = os.path.join(new_mp_path,saveas)
doc.GetActiveRenderData()[c4d.RDATA_MULTIPASS_FILENAME] = multipass

print ' '
print '_NEW SETTINGS_______'
print '[Filepath] %s' %(newpath)
if mpass:
print '[MP_path] %s' %(multipass)
print '[Project ] %s' %(current_project)
print '[Scene ] %s' %(docname)
print '[Camera] %s' %(camname)
print '[Image ] %s' %(saveas)
c4d.EventAdd()
# Optionally do the render from within the script
#(Only if new image name/save path is set)
#c4d.CallCommand(12099) # Render
return True

return True


if __name__=='__main__':
main()












'''
import c4d, os
from c4d import gui
#Welcome to the world of Python


def main():
    docname = doc.GetDocumentName()
    docname,ext = os.path.splitext(docname)
    print( docname )
    print( ext )
    outputRoot = 'C:\Users\render.admin\Desktop\__Michi\previs\'
    outputFile = docname
    output = os.path.join( outputRoot, outputFile )
    print( output )
if __name__=='__main__':
    main()
    
'''









