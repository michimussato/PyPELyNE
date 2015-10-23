###################################################################################
# (c) Lightmap Ltd 2012
#
# Script to support HDR Light Studio Live
###################################################################################
import maya.cmds as cmds
import maya.utils
import lightmap.HDRLightStudioLive as hdrls
import HdrlsVersion
reload(HdrlsVersion)

#debugging support
#import wingdbstub
#wingdbstub.Ensure()

gRendererItems = []
gEnvHookItems = []
gEnvHookDisplayMap = {}
gShowingHdrls = False
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

###################################################################################
# Attribute encoding/decoding
###################################################################################
def encodeAttribute(strAttrib):
	strEncoded = strAttrib.replace(".", "__DOT__")
	strEncoded = strEncoded.replace("[", "__OB__")
	strEncoded = strEncoded.replace("]", "__CB__")
	return strEncoded

def decodeAttribute(strAttrib):
	strDecoded = strAttrib.replace("__DOT__", ".")
	strDecoded = strDecoded.replace("__OB__", "[")
	strDecoded = strDecoded.replace("__CB__", "]")
	return strDecoded

###################################################################################
# Project related functionality
###################################################################################
def SetHdrlsProjectData(iblNode, strProjectData):
	EnsureHdrlsProjectContainsIblDataSlot(iblNode)

	#encode attribute for storing.
	iblNodeAttr = encodeAttribute(iblNode)
	cmds.setAttr("HdrlsProjectData." + iblNodeAttr, strProjectData, type="string")

def GetHdrlsProjectData(iblNode):
	#decode attribute for storing.
	iblNodeAttr = encodeAttribute(iblNode)
	if(cmds.attributeQuery(iblNodeAttr, node="HdrlsProjectData", exists=True)):
		rawAttrib = cmds.getAttr("HdrlsProjectData." + iblNodeAttr)
		decodedAttrib = decodeAttribute(rawAttrib)
		return decodedAttrib
	return None

def EnsureHdrlsNodePresentInProject():
	strNode = "HdrlsProjectData"
	if(cmds.objExists(strNode) == False):
		cmds.group(empty=True, name=strNode)

def EnsureHdrlsProjectContainsIblDataSlot(iblNode):
	#encode attribute for storing.
	iblNodeAttr = encodeAttribute(iblNode)
	if(cmds.attributeQuery(iblNodeAttr, node="HdrlsProjectData", exists=True) == False):
		cmds.addAttr("HdrlsProjectData", ln=iblNodeAttr, nn="ProjectData", dt="string", storable=True)

def LoadEnvHookProjectData():
	global gEnvHookDisplayMap

	selected = GetSelectedEnvironmentHook()
	if(selected == None):
		loadHdrlsProjectData("") # Reset project
		return

	mayaTexture, mayaNode = gEnvHookDisplayMap[selected]

	projectData = GetHdrlsProjectData(mayaNode)
	loadHdrlsProjectData(projectData)

def SaveEnvHookProjectData():
	selected = GetSelectedEnvironmentHook()
	if(selected == None):
		return

	strProjectData = saveHdrlsProjectData()

	if(strProjectData == None or len(strProjectData) == 0):
		return

	mayaTexture, mayaNode = gEnvHookDisplayMap[selected]

	SetHdrlsProjectData(mayaNode, strProjectData)

###################################################################################
#Node location functionlity for creating hooks
###################################################################################
def LocateNodesOfType(nodeType, textureAttribute):
	#default behaviour is just to display the node name
	nodes = []
	for node in cmds.ls(type=nodeType):
		entry = node+textureAttribute, node, node
		nodes.append(entry)
	return nodes

def LocateAllMentalRayIblNodes():
	return LocateNodesOfType("mentalrayIblShape", ".texture")

def LocateAllVRayIblNodes():
	#VRay nodes need to be treated differently. A VRay dome can be linked to a regular file node (or rather, this is all we support)
	#so we must follow this node to get the texture path to change
	nodes = []
	for node in cmds.ls(type="VRayLightDomeShape"):
		linkedNode = cmds.defaultNavigation(destination=node + ".domeTex", defaultTraversal=True)

		if(linkedNode == None):
			continue

		#if no file texture is linked to the domeTex, then create one and link it up
		if(linkedNode == []):
			fileNode = cmds.shadingNode('file', asTexture=True)
			cmds.defaultNavigation(connectToExisting=True, source=fileNode, destination=node + ".domeTex", force=True)
			linkedNode = cmds.defaultNavigation(destination=node + ".domeTex", defaultTraversal=True)

			if(linkedNode == None or linkedNode == []):
				cmds.scrollField("rendererErrorText", edit=True, text="Could not create and link texture node to VRay Light Dome domeTex attribute slot.")
				continue

			if cmds.getAttr("%s.useDomeTex" % node) == 0:
				cmds.setAttr("%s.useDomeTex" % node, 1)		

		#break out of the array the first entry
		linkedNode = linkedNode[0]
		if(cmds.nodeType(linkedNode) != "file"):
			continue

		#we have a texture, but check to see that linked to a VRayPlaceEnvTex that is set for Spherical maps.
		vrayTexNode = cmds.listConnections(linkedNode, s=True, d=False, t="VRayPlaceEnvTex")
		validTexNode = False
		if(vrayTexNode != None):
			texNode = vrayTexNode[0]
			if(cmds.attributeQuery("mappingType", node=str(texNode), exists=True)):
				mappingType = cmds.getAttr(texNode+".mappingType")
				if(mappingType != 2):
					cmds.scrollField("rendererErrorText", edit=True, text="Selected VRay Light Dome is mapped to use non-spherical mapping.")
					continue

		#everything look valid
		strAttribute = str(linkedNode) + ".fileTextureName"

		#craft an entry for the node list
		entry = strAttribute, node, linkedNode
		nodes.append(entry)

	return nodes        

def LocateAllRendermanIblNodes():
	#There are different names for different versions of Renderman, so support them all.
	compatibleNodes = LocateNodesOfType("RenderManEnvLightShape", ".rman__EnvMap")
	compatibleNodes += LocateNodesOfType("RMSEnvLight", ".rman__EnvMap")
	return compatibleNodes

def LocateAllArnoldIblNodes():
	#Arnold nodes are like VRay nodes in that it can be linked to a regular file node (or rather, this is all we support)
	#so we must follow this node to get the texture path to change
	nodes = []
	for node in cmds.ls(type="aiSkyDomeLight"):
		linkedNode = cmds.defaultNavigation(destination=node + ".color", defaultTraversal=True)
		if(linkedNode == None):
			continue

		#if no file texture is linked to the domeTex, then create one and link it up
		if(linkedNode == []):
			fileNode = cmds.shadingNode('file', asTexture=True)
			cmds.defaultNavigation(connectToExisting=True, source=fileNode, destination=node + ".color", force=True)
			linkedNode = cmds.defaultNavigation(destination=node + ".color", defaultTraversal=True)

			if(linkedNode == None or linkedNode == []):
				cmds.scrollField("rendererErrorText", edit=True, text="Could not create and link texture node to Arnold aiSkyDomeLight color attribute slot.")
				continue

		#break out of the array the first entry
		linkedNode = linkedNode[0]
		if(cmds.nodeType(linkedNode) != "file"):
			continue

		#we have a texture, but check to see that it's lat/long mapped.
		if(cmds.attributeQuery("format", node=str(node), exists=True)):
			mappingType = cmds.getAttr(node+".format")
			if(mappingType != 2):
				cmds.scrollField("rendererErrorText", edit=True, text="Selected Arnold SkyDomeLight is mapped to use non-spherical mapping.")
				continue

		#everything look valid
		strAttribute = str(linkedNode) + ".fileTextureName"

		#craft an entry for the node list
		entry = strAttribute, node, linkedNode
		nodes.append(entry)

	return nodes       

def LocateAllMaxwellIblNodes():
	maps = []
	#Maxwell options are not initialised/created until the renderer is selected as the output renderer in maya
	if(cmds.objExists("maxwellRenderOptions")):
		if(cmds.attributeQuery("environment", node="maxwellRenderOptions", exists=True)):

			#is maxwell set to use environments?
			if(cmds.attributeQuery("useEnvironment", node="maxwellRenderOptions", exists=True)):
				mapCount = cmds.getAttr("maxwellRenderOptions.environment", s=True)

				#map attributes may not yet been created/initialised if user has not been into settings (prob. not poss now we check useEnv flag)
				if(mapCount>0):
					for map in range(0, mapCount):
						strNode = "maxwellRenderOptions.environment["+str(map)+"]"

						#explicitally name the first 4 to what Maxwell uses as "freindly names".
						if map == 0:
							maps.append([strNode+".envTexture", "Background", strNode])
						elif map == 1:
							maps.append([strNode+".envTexture", "Reflection", strNode])
						elif map == 2:
							maps.append([strNode+".envTexture", "Refraction", strNode])
						elif map == 3:
							maps.append([strNode+".envTexture", "Illumination", strNode])
						else:
							maps.append([strNode+".envTexture", strNode, strNode])
				else:
					cmds.scrollField("rendererErrorText", edit=True, text="Maxwell environment not initialised until render options set to use IBL environment")
			else:
				cmds.scrollField("rendererErrorText", edit=True, text="Maxwell not set to use image based environment")
		else:
			cmds.scrollField("rendererErrorText", edit=True, text="Maxwell environment not initialised until the Use Image Based Lighting option is set in Render Settings under the Maxwell Render->Image Based tab")
	else:
		cmds.scrollField("rendererErrorText", edit=True, text="Maxwell not yet initialised - set to use Maxwell in Render Settings & select Maxwell Render tab to enable")
	return maps

def LocateAllModoIblNodes():
	nodes = []
	for node in cmds.ls(type="modoEnvironment"):
		linkedNode = cmds.defaultNavigation(destination=node + ".environmentColor", defaultTraversal=True)

		#check if there's a file node plugged in and create one if there's not
		if linkedNode == []:
			fileNode = cmds.shadingNode('file', asTexture=True)
			linkedNode = cmds.defaultNavigation(connectToExisting=True, source=fileNode, destination="%s.environmentColor" % node, force=True)

		if(linkedNode == None):
			continue

		#break out of the array the first entry
		linkedNode = linkedNode[0]
		if(cmds.nodeType(linkedNode) != "file"):
			continue

		#we have a texture, but check to see that it's lat/long mapped.
		if(cmds.attributeQuery("format", node=str(node), exists=True)):
			mappingType = cmds.getAttr(node+".format")
			if(mappingType != 2):
				cmds.scrollField("rendererErrorText", edit=True, text="Selected modo Environment node is mapped to use non-spherical mapping.")
				continue

		#everything look valid
		strAttribute = str(linkedNode) + ".fileTextureName"

		#craft an entry for the node list
		entry = strAttribute, node, linkedNode
		nodes.append(entry)

	return nodes

def getPluginName():
	strPlugin = ""
	if(isHostRendererMentalRay()):
		strPlugin = "Mayatomr"
	elif(isHostRendererMaxwell()):
		strPlugin = "maxwell"
	elif(isHostRendererVRay()):
		strPlugin = "vrayformaya"
	elif(isHostRendererRenderMan()):
		strPlugin = "RenderMan_for_Maya"
	elif(isHostRendererArnold()):
		strPlugin = "mtoa"
	elif(isHostRendererModo()):
		strPlugin = "ModoRender"

	return strPlugin

def getPluginVersion():
	strPlugin = getPluginName()
	if(len(strPlugin) == 0):
		return 0

	return cmds.pluginInfo(strPlugin, q=True, v=True)

def validateRenderer():
	strPlugin = getPluginName()
	if(len(strPlugin) == 0):
		return False

	# Most renderers are in plugins, so by locating that we indentify that the renderer is valid.
	pluginLoaded = cmds.pluginInfo(strPlugin, q=True, l=True)

	# Modo is not a plugin, so check separatly for that if we failed above.
	if(pluginLoaded == False):
		if cmds.getAttr('defaultRenderGlobals.ren') == 'modoRender':
			pluginLoaded = True

	if(pluginLoaded == False):
		# Craft the error string (watching for modo special case).
		if strPlugin == "ModoRender":
			strError = strPlugin + " is not selected or registered - cannot support this renderer at this time"
		else:
			strError = strPlugin + ".mll plugin is not loaded - cannot support this renderer at this time"        

		cmds.scrollField("rendererErrorText", edit=True, text=strError)
		return False

	cmds.scrollField("rendererErrorText", edit=True, text="Maya plugin for Host Renderer detected")
	return True

###################################################################################
#UI helper functions.
###################################################################################
def isHostRendererMentalRay():
	return (cmds.optionMenu("hostRendererMenu", q=True, v=True) == "Mental Ray")

def isHostRendererVRay():
	return (cmds.optionMenu("hostRendererMenu", q=True, v=True) == "VRay")

def isHostRendererRenderMan():
	return (cmds.optionMenu("hostRendererMenu", q=True, v=True) == "RenderMan")

def isHostRendererMaxwell():
	return (cmds.optionMenu("hostRendererMenu", q=True, v=True) == "Maxwell")

def isHostRendererArnold():
	return (cmds.optionMenu("hostRendererMenu", q=True, v=True) == "Arnold")

def isHostRendererModo():
	return (cmds.optionMenu("hostRendererMenu", q=True, v=True) == "Modo")

def getHostString():
	if(cmds.optionMenu("hostRendererMenu", q=True, ni=True) == 0):
		return None
	return cmds.optionMenu("hostRendererMenu", q=True, v=True)

def getRendererId():
	menuItem = cmds.optionMenu("hostRendererMenu", q=True, v=True)
	for menu, name, rendererId in gRendererItems:
		if name == menuItem:
			return rendererId
	return ""

def getLiveTextureDst():
	global gEnvHookDisplayMap

	selected = GetSelectedEnvironmentHook()
	if(selected == None):
		return None

	mayaTexture, mayaNode = gEnvHookDisplayMap[selected]
	if(mayaTexture == ""):
		return None
	return mayaTexture

def GetSelectedEnvironmentHook():
	if(maya.cmds.optionMenu('envHooksMenu', exists=True) == False):
		return None

	if(cmds.optionMenu("envHooksMenu", q=True, ni=True) > 0):
		return cmds.optionMenu("envHooksMenu", q=True, v=True)

	return None

###################################################################################
# UI Creation
###################################################################################
def populateHostRendererList():
	global gRendererItems

	gRendererItems.append([cmds.menuItem(label="Mental Ray", parent="hostRendererMenu"), "Mental Ray", "MentalRay"])
	gRendererItems.append([cmds.menuItem(label="Maxwell", parent="hostRendererMenu"), "Maxwell", "Maxwell"])
	gRendererItems.append([cmds.menuItem(label="VRay", parent="hostRendererMenu"), "VRay", "VRay"])
	gRendererItems.append([cmds.menuItem(label="RenderMan", parent="hostRendererMenu"), "RenderMan", "RenderMan"])
	gRendererItems.append([cmds.menuItem(label="Arnold", parent="hostRendererMenu"), "Arnold", "Arnold"])
	gRendererItems.append([cmds.menuItem(label="Modo", parent="hostRendererMenu"), "modo", "modo"])

	if(len(gRendererItems) > 0):
		cmds.optionMenu("hostRendererMenu", edit=True, select=1)    

	hostRendererChanged()

def clearEnvHookList():
	global gEnvHookItems
	global gEnvHookDisplayMap

	for item in gEnvHookItems:
		cmds.deleteUI(item)    
	del gEnvHookItems[0:len(gEnvHookItems)]
	gEnvHookDisplayMap.clear()

def populateEnvHookList():
	global gEnvHookItems
	global gEnvHookDisplayMap

	#Clear existing items
	clearEnvHookList()

	#Get list of what is to go into the envhook list
	if isHostRendererMentalRay():
		envHooks = LocateAllMentalRayIblNodes()
	elif isHostRendererVRay():
		envHooks = LocateAllVRayIblNodes()
	elif isHostRendererRenderMan():
		envHooks = LocateAllRendermanIblNodes()
	elif isHostRendererMaxwell():
		envHooks = LocateAllMaxwellIblNodes()
	elif isHostRendererArnold():
		envHooks = LocateAllArnoldIblNodes()
	elif isHostRendererModo():
		envHooks = LocateAllModoIblNodes()

	#populate envhook list
	if(envHooks != None):
		for hook in envHooks:
			mayaIblNodeTextureName = hook[0]
			niceName = hook[1]
			mayaIblNodeToReveal = hook[2]
			gEnvHookDisplayMap[niceName] = [mayaIblNodeTextureName, mayaIblNodeToReveal]
			newItem = cmds.menuItem(label=hook[1], parent="envHooksMenu")
			gEnvHookItems.append(newItem)

		if(len(gEnvHookItems) > 0):
			cmds.optionMenu("envHooksMenu", edit=True, select=1)

			#If we are maxwell, disable the "Show Hook" button as it doesn't take you to the render settings where you want to be.
			if(isHostRendererMaxwell() == True):
				cmds.button("syncToMaya", edit=True, enable=False)
			else:
				cmds.button("syncToMaya", edit=True, enable=True)
		else:
			cmds.button("syncToMaya", edit=True, enable=False)

	return

##############################################################################
# UI Layout
##############################################################################
def HdrlsLiveUI():	
	if cmds.window("HdrLightStudioLive", exists=True):
		cmds.deleteUI("HdrLightStudioLive")

	window = cmds.window("HdrLightStudioLive", w=300, h=350, mnb=False, mxb=False, sizeable=False, title="HDR Light Studio 4 Live")
	job1 = cmds.scriptJob(uiDeleted=[window, stopLiveSession])
	job2 = cmds.scriptJob(event=["quitApplication", stopLiveSession])

	#gfx that we need
	iconsPath = cmds.internalVar(upd=True) + "icons/"
	imageLogo = iconsPath + "HdrlsLogo.png"

	#create main layout
	mainLayout = cmds.columnLayout(w=300, h=350, columnOffset=["both", 5])

	#image logo location and image control
	cmds.separator(h=5)
	cmds.image(w=300, h=35, image=imageLogo)

	#renderer list
	cmds.separator(h=10)
	cmds.text(" Host Renderer")
	cmds.separator(h=2)
	exportFormatMenu = cmds.optionMenu("hostRendererMenu", w=300, changeCommand=hostRendererChanged)

	#text field for unavailable renderers
	cmds.separator(h=5)
	cmds.scrollField('rendererErrorText', text="Error will go here", w=300, h=70, visible=True, enable=False, ww=True)

	#environment hooks list
	cmds.separator(h=10)
	cmds.text(" Environment Hooks")
	cmds.separator(h=2)
	exportFormatMenu = cmds.optionMenu("envHooksMenu", w=300, changeCommand=envHookChanged)

	#refresh button for env hooks and sync to maya button to show in attribute editor
	cmds.separator(h=10)
	cmds.rowColumnLayout(nc=2, cw=[(1, 150), (2, 150)], columnOffset=[(1, "left", 15), (2, "right", 15)], parent=mainLayout)
	cmds.button(label="Refresh Env-Hooks", w=130, c=pushRefreshEnvHooks)
	cmds.button("syncToMaya", label="Show Hook In Maya", w=130, c=pushSyncMayaToEnvHooks)

	#Start/Stop Live Session
	cmds.separator(h=25)
	cmds.separator(h=25)
	cmds.button("initHdrls", label="Start Live", w=100, enable=True,c=pushStartLiveSession)
	cmds.button("exitHdrls", label="Stop Live", w=100, enable=True, c=pushExitLiveSession)
	cmds.separator(h=10, parent=mainLayout)

	#Version information
	cmds.text(HdrlsVersion.GetHdrlsScriptVersion(), parent=mainLayout, w=300, align="right", font="smallObliqueLabelFont")

	#populate initial lists
	populateHostRendererList()

	#show window
	cmds.showWindow(window)

##############################################################################
#UI handlers
##############################################################################
def hostRendererChanged(*args):
	EnsureHdrlsNodePresentInProject()
	if(validateRenderer()):
		populateEnvHookList()
		setLiveHostRendererInUse()
		LoadEnvHookProjectData()		
	else:
		clearEnvHookList()

def envHookChanged(*args):
	LoadEnvHookProjectData()
	return

def pushRefreshEnvHooks(*args):
	global gEnvHookItems

	selected = GetSelectedEnvironmentHook()

	populateEnvHookList()

	#attempt to set the current selection
	if(selected != None and len(selected) > 0):
		index = 0
		for hook in gEnvHookItems:
			index = index + 1
			displayedText = cmds.menuItem(hook, q=True, label=True)
			if(selected == displayedText):
				cmds.optionMenu("envHooksMenu", edit=True, sl=index)
				break

def pushSyncMayaToEnvHooks(*args):
	global gEnvHookDisplayMap

	selected = GetSelectedEnvironmentHook()
	if(selected == None):
		return

	mayaTexture, mayaNode = gEnvHookDisplayMap[selected]
	cmds.select(mayaNode)

def pushStartLiveSession(*args):
	running = startLiveSession()
	return

def pushExitLiveSession(*args):
	stopLiveSession()
	return

##############################################################################
#Error handling
##############################################################################
def checkForHdrlsError(errCode, strCallingFunction):
	if(errCode == hdrls.HDRLS_OK):
		return

	errString = gErrorCodes[errCode]		
	print "HDRLS Error Code :" + hex(errCode) + " - " + errString + " From hdrls interface function [" + strCallingFunction + "]"

##############################################################################
#Live functionality
##############################################################################
def rawFileUpdate(strFilename):
	textureDst = getLiveTextureDst()
	if(textureDst == None or len(textureDst) == 0):
		return

	maya.cmds.setAttr(textureDst, strFilename, type="string")
	SaveEnvHookProjectData()

def cbRawFileUpdate(strFilename):
	#Ensure we handle the UI changes on main thread and not the callback thread    
	maya.utils.executeInMainThreadWithResult(rawFileUpdate, strFilename)

def loadHdrlsProjectData(data):
	global gShowingHdrls

	if(gShowingHdrls == False):
		return	

	#if no data present, pass on as empty string as this indicates a new project.
	if(data == None):
		data = ""

	state = hdrls.LoadProject(str(data))
	checkForHdrlsError(state, "LoadProject")
	if(state != hdrls.HDRLS_OK):    
		return False
	return True

def saveHdrlsProjectData():
	global gShowingHdrls

	if(gShowingHdrls == False):
		return None

	state, strProjectData = hdrls.SaveProject()

	if(state != hdrls.HDRLS_OK):
		return None	

	return strProjectData

def startLiveSession():
	global gShowingHdrls

	state = hdrls.InitialiseHdrLightStudio(9, str("Maya"))
	checkForHdrlsError(state, "InitialiseHdrLightStudio")
	if(state != hdrls.HDRLS_OK):
		return False

	checkForHdrlsError(hdrls.SetRawHdrFileUpdateCb(cbRawFileUpdate),"SetRawHdrFileUpdateCb")
	checkForHdrlsError(hdrls.SetProductionRenderFileUpdateCb(cbRawFileUpdate),"SetProductionRenderFileUpdateCb")
	#checkForHdrlsError(hdrls.SetSettings('<?xml version="1.0"?><HDRLSSettings><HDRLSSetting>live_tempdir,\\\\LIGHTMAPNAS\Lightmap</HDRLSSetting></HDRLSSettings>'), "SetSettings")

	state = hdrls.ShowMainInterface()
	checkForHdrlsError(state, "ShowMainInterface")
	if(state != hdrls.HDRLS_OK):    
		return False

	gShowingHdrls = True
	setLiveHostRendererInUse()

	#Ensure that we have hdrls node in this project.
	EnsureHdrlsNodePresentInProject()
	LoadEnvHookProjectData()

	return True

def setLiveHostRendererInUse():
	global gShowingHdrls

	if(gShowingHdrls == False):
		return

	rendererId = getRendererId()
	if(len(rendererId) > 0):
		checkForHdrlsError(hdrls.SetHostRenderer("Maya", rendererId), "SetHostRenderer")

def stopLiveSession():
	global gShowingHdrls

	if(gShowingHdrls == False):
		return	

	checkForHdrlsError(hdrls.Exit(), "Exit")
	gShowingHdrls = False
	return True