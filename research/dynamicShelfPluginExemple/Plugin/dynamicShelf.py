# -*- coding: utf-8 -*-
#########################################################################
############################# INFORMATIONS ##############################
#########################################################################
#
#    TITLE : dynamicShelf
#    AUTHOR : Nicolas Koubi
#
#########################################################################
############################### READ-ME #################################
#########################################################################
#
#
# DESCRIPTION:
#
#   Dynamic shelf plug-in for Maya.
#
#
# DEPENDENCIES:
#
#    maya.cmds, maya.mel, sys, os, minidom
#
#
#########################################################################


#########################################################################
##### MODULES IMPORT
#########################################################################


    ## SYS
try:
    import sys
except ImportError: 
    print "sys import failed"
    
    
    ## OS
try:
    import os
except ImportError: 
    print "os import failed"

    
    ## MAYA.MEL
try:
    import maya.mel
except ImportError: 
    print "maya.mel import failed"
    
    
    ## MAYA.CMDS
try:
    import maya.cmds as cmds
except ImportError: 
    print "maya.cmds import failed"
    
    
    ## MINIDOM
try:
    from xml.dom import minidom
except ImportError: 
    print "minidom import failed"


    
#########################################################################
##### PATHS
#########################################################################


## Get icons path from the Maya.env ICONS_PATH variable
iconsPath = os.environ.get('ICONS_PATH', None)

## Get scripts path from the Maya.env SCRIPTS_PATH variable
scriptsPath = os.environ.get('SCRIPTS_PATH', None)

## Get project name from the Maya.env PRJ_NAME variable
prjName = os.environ.get('PRJ_NAME', None)

## Get the CONFIGS_PATH from the Maya.env file and get the configuration files for the specified project
configsPath = os.environ.get('CONFIGS_PATH', None)
prjConfFiles = os.path.join(configsPath, prjName)

## Append the scriptsPath
sys.path.append(scriptsPath)
    
    
    
#####################################################################
## initializePlugin
#####################################################################
##
## Initialize plug-in and create shelf.
##
#####################################################################
def initializePlugin(mobject):
    
    ## Get the shelf configuration file
    shelfConfFile = os.path.join(prjConfFiles, 'dynamicShelfConf.xml')
    
    ## Check if the file exist befor continuing
    if os.path.exists(shelfConfFile) == True :
        

        ## This is a fix for the automatically saved shelf function
        ## It will delete a previously shelf created with the plugin if any exist
        maya.mel.eval('if (`shelfLayout -exists scriptsShelf `) deleteUI scriptsShelf;')
        
        ## Declare the $gShelfTopLevel variable as a python variable
        ## The $gShelfTopLevel mel variable is the Maya default variable for the shelves bar UI
        shelfTab = maya.mel.eval('global string $gShelfTopLevel;')
        ## Declare the $scriptsShelf (the shelfLayout) as a global variable in order to unload it after
        maya.mel.eval('global string $scriptsShelf;')
        ## Create a new shelfLayout in $gShelfTopLevel
        maya.mel.eval('$scriptsShelf = `shelfLayout -cellWidth 33 -cellHeight 33 -p $gShelfTopLevel scriptsShelf`;')
        
        

        ## Parse the menuConfFile
        xmlMenuDoc = minidom.parse(shelfConfFile)
        
        ## Loop trough each shelfItem entry in the shelfConfFile
        for eachShelfItem in xmlMenuDoc.getElementsByTagName("shelfItem") :
	    ## Get the icon name
            getIcon = eachShelfItem.attributes['icon'].value
            ## Join the icon name to the icons path in order to get the full path of the icon
            shelfBtnIcon = os.path.join(iconsPath, getIcon)
            ## Get the annotation
            getAnnotation = eachShelfItem.attributes['ann'].value
            ## Get the command to launch
            getCommand = eachShelfItem.attributes['cmds'].value

	    ## Create the actual shelf button with the above parameters
            cmds.shelfButton(command=getCommand, annotation=getAnnotation, image=shelfBtnIcon)
            
            
        ## Rename the shelfLayout with the prjName
        maya.mel.eval('tabLayout -edit -tabLabel $scriptsShelf "'+prjName+'" $gShelfTopLevel;')
        
     
        print "//-- "+prjName+" shelf successfully loaded --//"
    
    
    
#####################################################################
## uninitializePlugin
#####################################################################
##
## Un-Initialize plug-in and delete shelf.
##
#####################################################################
def uninitializePlugin(mobject):
    ## Delete the scriptsShelf if it exist
    maya.mel.eval('if (`shelfLayout -exists scriptsShelf `) deleteUI scriptsShelf;')
