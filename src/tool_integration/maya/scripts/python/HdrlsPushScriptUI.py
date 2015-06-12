###################################################################################
# (c) Lightmap Ltd 2012
#
# Script to export scene to HDR Light Studio
# Scene is pushed to HDR Light Studio via named or temporary .dae or .mi file.
###################################################################################
import maya.cmds as cmds
import tempfile
import socket
import maya.mel as mel
import sys
import HdrlsVersion
import lightmap.HDRLightStudioLive as hdrls
reload(HdrlsVersion)

#debugging support
#import wingdbstub
#wingdbstub.Ensure()

gErrorCodes = {	0x10000000 : 'HDRLS_FAILED',
                   0x10000001 : 'HDRLS_NOT_INTIALISED',
                   0x10000002 : 'HDRLS_NO_INTERFACE',
                   0x10000003 : 'HDRLS_PARAM_ERROR',
                   0x10000004 : 'HDRLS_STRING_TOO_LONG',
                   0x10000005 : 'HDRLS_BUFFER_TOO_SHORT',
                   0x10000006 : 'HDRLS_UNSUPPORTED_VERSION',
                   0x10000007 : 'HDRLS_OUTOFMEMORY',
                   0x10000008 : 'HDRLS_UNKNOWN_MESSAGE',
                   0x10000009 : 'HDRLS_CRITICAL_INTERNAL_ERR',
                   0x1000000A : 'HDRLS_BAD_SETTINGS',
                   0x1000000B : 'HDRLS_CANNOT_DO_FUNCTION_NOW',
                   0x1000000C : 'HDRLS_UNLICENSED',
                   0x1000000D : 'HDRLS_FILE_NOT_FOUND',
                   0x1000000E : 'HDRLS_INVALID_FILE_FORMAT',
                   0x1000000F : 'HDRLS_COMMS_TIMEOUT',
                   0x10000010 : 'HDRLS_INVALID_PROJECT_ASSET',
                   0x10000011 : 'HDRLS_FAILED_TO_LOAD_ASSET',
                   0x10000012 : 'HDRLS_NO_NODE_SELECTED',
                   0x10000013 : 'HDRLS_NO_COMMS',
                   0x10000014 : 'HDRLS_BAD_COMMS_REPLY',
                   0x10000015 : 'HDRLS_COMMS_ERROR',
                   0x10000016 : 'HDRLS_CANNOT_START_PROCESS',
                   0x10000017 : 'HDRLS_ALREADY_INITIALISED',
                   0x10000018 : 'HDRLS_UNKNOWN_HOSTRENDERER',
                   0x100000ff : 'HDRLS_UNKNOWN_ERROR'}

##############################################################################
#Error handling
##############################################################################
def checkForHdrlsError(errCode, strCallingFunction):
	if(errCode == hdrls.HDRLS_OK):
		return

	errString = gErrorCodes[errCode]		
	print "HDRLS Error Code :" + hex(errCode) + " - " + errString + " From hdrls interface function [" + strCallingFunction + "]"
	

def HdrlsPushScriptUI():
	if cmds.window("HdrLightStudio", exists=True):
		cmds.deleteUI("HdrLightStudio")

	window = cmds.window("HdrLightStudio", w=300, h=350, mnb=False, mxb=False, sizeable=False, title="HDR Light Studio 4 Push System")

	#gfx that we need
	iconsPath = cmds.internalVar(upd=True) + "icons/"
	imageLogo = iconsPath + "HdrlsLogo.png"
	imageFolderIcon = iconsPath + "FolderIcon.png"    

	#create main layout
	mainLayout = cmds.columnLayout(w=300, h=350, columnOffset=["both", 5])

	#image logo location and image control
	cmds.separator(h=5)
	cmds.image(w=300, h=35, image=imageLogo)

	#export option menu
	cmds.separator(h=10)
	cmds.text(" Export Format")
	cmds.separator(h=2)
	exportFormatMenu = cmds.optionMenu("exportFormatMenu", w=300, changeCommand=exportFormatChanged)
	cmds.menuItem(label="COLLADA (dae)")
	cmds.menuItem(label="MentalImage (mi)")

	#selection only checkbox
	cmds.separator(h=5)
	selectionCheck = cmds.checkBox("selectionCheck", label="Export Selection Only")

	#specify file checkbox
	tempFileCheck = cmds.checkBox("tempFileCheck", label="Use Temporary File", value=True, changeCommand=tempFileToggle)

	#create field and browse buttons in sub row-column layout (initially disabled)
	cmds.separator(h=5)
	cmds.rowColumnLayout(nc=2, cw=[(1, 270), (2, 30)], columnOffset=[(1, "right", 5), (2, "left", 0)])

	#input field
	specifiedFile = cmds.textField("specifiedFile", w=270, editable=False, vis=False)
	browseButton = cmds.symbolButton("browseButton", w=30, h=30, image=imageFolderIcon, c=browseForFilePath, vis=False)

	#export button
	cmds.separator(h=10,parent=mainLayout)
	cmds.rowColumnLayout(nc=2, cw=[(1, 150), (2, 150)], columnOffset=[(1, "right", 15), (2, "left", 15)], parent=mainLayout)
	cmds.button(label="Select Camera", w=125, c=pushViaCameraSelection)
	cmds.button(label="Current Views Camera", w=125, c=pushViaCurrentView)
	cmds.separator(h=10,parent=mainLayout)
	logLine = cmds.textField("logLine", w=300, editable=False, parent=mainLayout)
	cmds.separator(h=10,parent=mainLayout)
	
	#Version information
	cmds.text(HdrlsVersion.GetHdrlsScriptVersion(), parent=mainLayout, w=300, align="right", font="smallObliqueLabelFont")
	
	#show window
	cmds.showWindow(window)

def tempFileToggle(*args):
	# Toggle the state of the temp file fields.
	useTempFile = cmds.checkBox("tempFileCheck", q=True, v=True)
	enableFields = True
	if(useTempFile == True):
		enableFields = False

	#if temp file, hide the file selection field and browse button
	cmds.textField("specifiedFile", edit=True, vis=enableFields)
	cmds.symbolButton("browseButton", edit=True, vis=enableFields)    

def isExportFormatCollada():
	selectedFormat = cmds.optionMenu("exportFormatMenu", q=True, v=True)
	return (selectedFormat == "COLLADA (dae)")

def isExportFormatMentalImage():
	selectedFormat = cmds.optionMenu("exportFormatMenu", q=True, v=True)
	return (selectedFormat == "MentalImage (mi)")

def exportFormatChanged(*args):
	# Update the current file extension (if present) with current selection.
	currentFile = cmds.textField("specifiedFile", q=True, text=True)
	selectedFormat = cmds.optionMenu("exportFormatMenu", q=True, v=True)

	#if we have     
	if(len(currentFile)>0):
		if(isExportFormatCollada()):
			print "changing to dae"
			currentFile = currentFile.rpartition(".")[0] + ".dae"
		else:
			print "changing to mi"
			currentFile = currentFile.rpartition(".")[0] + ".mi"

	print "Result: " + currentFile            
	cmds.textField("specifiedFile", edit=True, text=currentFile)

def browseForFilePath(*args): # *args as we will get args as it's a callback. We just ignore it!
	fileFilter = "*.dae"
	selectedFormat = cmds.optionMenu("exportFormatMenu", q=True, v=True)
	if(isExportFormatMentalImage()):
		fileFilter = "*.mi"

	returnFile = cmds.fileDialog2(ds=2, cap="Select Export Filename", fm=0, ff=fileFilter)[0]

	cmds.textField("specifiedFile", edit=True, text=returnFile)

def pushViaCameraSelection(*args):
	#list all cameara available for this export format and let the user choose which to use.
	cameraList = getAllValidCameras()
	if(len(cameraList)==0):
		strMessage = "There are no valid cameras in this scene to view in HDR Light Studio"
		if(isExportFormatCollada()):
			strMessage += "\nNote that COLLADA files do not support the export of the default Maya views (top, persp etc)."
		if(isExportFormatMentalImage()):
			strMessage += "\nNote that MentalImage files only support cameras that are are set to be renderable."            
		cmds.confirmDialog(title='Info', message=strMessage, button=['Ok'])
		return

	#get the users selection.
	camera = cmds.layoutDialog(ui=createDlgLayoutForCameraList, t="Select available camera")
	if(len(camera) == 0 or camera == "dismiss"):
		return

	pushToHdrls(camera)

def pushViaCurrentView(*args):
	camera = getCurrentCamera().encode()
	if(len(camera)==0):
		cmds.confirmDialog(title='Error', message="No cameras are present in the current view", button=['Ok'])
		return

	if(camera == "<ambiguous>"):
		cmds.confirmDialog(title='Error', message="Please ensure camera view to use is selected", button=['Ok'])
		return    

	validCameras = getAllValidCameras()
	if(camera in validCameras):
		pushToHdrls(camera)
	else:
		strMessage = "The camera for the currently selected view [" + camera + "] cannot be exported with the current file type.\n\n"
		if(isExportFormatCollada()):
			strMessage += "Note that COLLADA files do not support the export of the default Maya views (top, persp etc)."
		if(isExportFormatMentalImage()):
			strMessage += "Note that MentalImage files only support cameras that are are set to be renderable."            
		cmds.confirmDialog(title='Info', message=strMessage, button=['Ok'])        

def pushToHdrls(camera):
	selectionOnly = cmds.checkBox("selectionCheck", q=True, v=True)
	useTempFile = cmds.checkBox("tempFileCheck", q=True, v=True)
	exportFile = cmds.textField("specifiedFile", q=True, text=True)

	#correct for temp file.
	if(useTempFile):
		exportFile = getTempFilename()

	#make sure we are working with ascii encoding
	exportFile = exportFile.encode()

	#catch name errors
	if(len(exportFile) == 0):
		cmds.confirmDialog(title='Error', message="No export filename set", button=['Ok'])
		return

	#add the correct file extension
	fileType = exportFile.rpartition(".")[2]

	#if we are exporting a selection only, we need to make sure that the camera we want is also selected
	#as well as all children of selected nodes.
	originalSel = cmds.ls(sl=True)
	newSel = cmds.ls(sl=True)
	if(selectionOnly):
		cmds.select(camera, add=True)
		newSel = cmds.ls(sl=True)
		cmds.select(newSel, hi=True)
		newSel = cmds.ls(sl=True)

	#perform the export
	exportedOk = False;
	if(fileType == "dae"):
		exportedOk = exportSceneCollada(exportFile.encode(), selectionOnly)
	else:
		exportedOk = exportSceneMi(exportFile.encode(), selectionOnly)    

	#revert to the original selection - it can be lost by the fbx exporter.
	if(selectionOnly):
		cmds.select(newSel)

	if(exportedOk == False):
		return

	#create payload
	payload = "HDRLS"
	if(useTempFile):
		payload += "LTS_"
	else:
		payload += "LS__"
	payload += "!" + exportFile
	payload += "!" + camera

	#add up axis for MI files
	if(isExportFormatMentalImage()):
		upAxis = cmds.upAxis(q=True, axis=True)
		if(upAxis == "y"):
			payload += "!WUY_"
		else:
			payload += "!WUZ_"
			
	#ensure LiveLight is open.
	state = hdrls.LoadScene("", True)
	checkForHdrlsError(state, "LoadScene")
	if(state != hdrls.HDRLS_OK):
		cmds.confirmDialog(title='Error', message="No connection present for HDR Light Studio Live for Maya.\nPlease start a new live session of HDR Light Studio Live for Maya from your HDR Light Studio shelf.", button=['Ok'])
		return		

	#send to hdrls
	try:
		s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(("127.0.0.1", 9002))
		s.sendall(payload)
		s.close()

		#update log line
		strLogText = "Selected Camera: " + camera
		cmds.textField("logLine", edit=True, text=strLogText)        

	except socket.error as e:
		strError = "Cannot send command to HDR Light Studio\n\n"
		strError += "Socket Error({0})\n{1}\n\n".format(e.errno, e.strerror)
		strError += "Please ensure HDR Light Studio is running"
		cmds.confirmDialog(title='Error', message=strError, button=['Ok'])

	except:
		strError = "Cannot send command to HDR Light Studio\n\n"
		strError += "Unexpected error(" + str(sys.exc_info()[0]) + ")\n\n"
		strError += "Please ensure HDR Light Studio is running"
		cmds.confirmDialog(title='Error', message=strError, button=['Ok'])

def createDlgLayoutForCameraList():        
	#create form ready for using as a modal dialog template
	cameraList = getAllValidCameras()

	#create a form layout.
	form = cmds.setParent(q=True)
	cmds.formLayout(form, e=True, width=300)

	#create objects to put into modal dialog.
	cmds.columnLayout(w=300, h=100, columnOffset=["left", 5])
	cmds.separator(h=5)

	strPrompt = ""
	if(isExportFormatCollada()):
		strPrompt += "Note that COLLADA files do not support the export of the default Maya views (top, persp etc)."
	if(isExportFormatMentalImage()):
		strPrompt += "Note that MentalImage files only support cameras that are are set to be renderable."                

	cmds.text(strPrompt, w=290, ww=True)
	cmds.separator(h=5)
	cmds.optionMenu("cameraMenu", w=290)
	for camera in cameraList:
		cmds.menuItem(label=camera)

	#attempt to set the current selection
	lastCamera = cmds.textField("logLine", q=True, text=True)
	if(len(lastCamera) > 0):
		lastCameraName = lastCamera.rpartition(': ')[2]
		index = 0
		for cam in cameraList:
			index = index + 1
			if(cam == lastCameraName):
				cmds.optionMenu("cameraMenu", edit=True, sl=index)
				break

	cmds.separator(h=20)
	cmds.rowColumnLayout(nc=2, cw=[(1, 150), (2, 150)], columnOffset=[(1, "right", 50), (2, "left", 40)])
	cmds.button("Select", w=100, h=20, c=selectCameraForExport)
	cmds.button("Cancel", w=100, h=20, c=cancelCameraForExport)
	cmds.separator(h=5)

def cancelCameraForExport(*args):
	cmds.layoutDialog(dismiss="")

def selectCameraForExport(*args):
	selectedCamera = cmds.optionMenu("cameraMenu", q=True, v=True)
	cmds.layoutDialog(dismiss=selectedCamera)

def getTempFilename():
	# Generate a temporaty filename with the correct extension.
	tempFile = tempfile.NamedTemporaryFile()
	tempFilename = tempFile.name
	selectedFormat = cmds.optionMenu("exportFormatMenu", q=True, v=True)
	if(isExportFormatCollada()):
		tempFilename += ".dae"
	else:
		tempFilename += ".mi"
	return tempFilename

# Export the current scene to a Collada file
def exportSceneCollada(exportFilename, selectionOnly):
	#determine if the fbxmaya plugin is loaded.
	pluginLoaded = cmds.pluginInfo('fbxmaya', q=True, l=True)
	if(pluginLoaded == False):
		cmds.confirmDialog(title='Error', message="FBX Maya plugin must be loaded to export a COLLADA file", button=['Ok'])
		return False

	#get command set up ready to work
	exportCommand = "FBXExport -f \"" + exportFilename + "\""
	if(selectionOnly):
		exportCommand += "-s"
	exportCommand += ";"
	exportCommand = exportCommand.replace("\\", "/")

	mel.eval("FBXResetExport;")
	mel.eval("FBXExportCameras -v true;")
	mel.eval("FBXExportLights -v false;")
	mel.eval("FBXExportUpAxis z;")
	mel.eval("FBXProperty \"Export|IncludeGrp|Geometry|GeometryNurbsSurfaceAs\" -v \"Software Render Mesh\"")
	mel.eval(exportCommand)

	return True

# Export the current scene to a mental images file
def exportSceneMi(exportFilename, selectiononly):
	#determine if the fbxmaya plugin is loaded.
	pluginLoaded = cmds.pluginInfo('Mayatomr', q=True, l=True)
	if(pluginLoaded == False):
		cmds.confirmDialog(title='Error', message="MayaToMR plugin must be loaded to export a MentalImage file", button=['Ok'])
		return False

	cmds.Mayatomr(mi=True, file=exportFilename, active=selectiononly)

	return True

def getAllValidCameras():
	if(isExportFormatCollada()):
		return getAllValidColladaCameras()
	return getAllValidMentalImageCameras()

def getAllValidColladaCameras():
	validCameras = []
	cameraShapes = cmds.ls(cameras=True)
	for camera in cameraShapes:
		relatives = cmds.listRelatives(camera, p=True, c=False, pa=True)
		for relative in relatives:
			if(cmds.nodeType(relative) == "transform"):
				if(isExportableColladaCamera(relative)):
					validCameras.append(relative)

	return validCameras

def getAllValidMentalImageCameras():
	validCameras = []
	cameraShapes = cmds.ls(cameras=True)
	for camera in cameraShapes:
		if(isExportableMiCamera(camera)):
			relatives = cmds.listRelatives(camera, p=True, c=False, pa=True)
			for relative in relatives:
				if(cmds.nodeType(relative) == "transform"):
					validCameras.append(relative)

	return validCameras

#See if valid camera to use
def isExportableMiCamera(cameraShape): 
	if(len(cameraShape)==0):
		return False

	#When using mental ray, only renderable cameras are exportable.
	attribute = cameraShape + ".renderable"
	return cmds.getAttr(attribute)

def isExportableColladaCamera(camera):
	if(len(camera)==0):
		return False

	if(camera == "persp" or camera == "top" or camera == "front" or camera == "side"):
		return False
	if(camera == "stereoCameraLeft" or camera == "stereoCameraRight"):
		return False
	return True; 

# Get the camera from the currently selected view
def getCurrentCamera():
	strCam = ""
	strPanel = cmds.getPanel(withFocus=True)
	strPane = cmds.getPanel(typeOf=strPanel)
	print "Panel: " + strPanel + "\nPane: " + strPane,

	if(strPane == "modelPanel"):
		#model panel should always have a camera attached.
		strCam = cmds.modelEditor(strPanel, query=True, camera=True)
		print "\nFound: [" + strCam + "]",

	if(strCam == ""):
		#no camera found in currently selected panel. If there is only *ONE* panel
		#visible, then use the camera in that - we assume that the user is looking
		#at the panel they want to use.
		panelsVisible = cmds.getPanel(vis=True)
		panelsValue = cmds.getPanel(typ='modelPanel')
		possibleCameras = []
		for panel in panelsVisible:
			if(panel in panelsValue):
				possibleCameras.append(cmds.modelEditor(panel, query=True, camera=True))

		if(len(possibleCameras) == 1):
			return possibleCameras[0]
		elif(len(possibleCameras) > 1):
			return "<ambiguous>"

		print "\n<No Cam found>"
		return ""    

	if(cmds.nodeType(strCam) != "camera"):
		print "\n<Hit Camera Node>"
		return strCam

	print "\n<Evaluating Relatives>",
	strRelatives = cmds.listRelatives(parent=strCam, pa=True)
	return strRelatives[0]
