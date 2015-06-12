#########################################################################
############################# INFORMATIONS ##############################
#########################################################################
#
#    TITLE : helloWorld
#    AUTHOR : Nicolas Koubi
#
#########################################################################
############################### READ-ME #################################
#########################################################################
#
#
# DESCRIPTION:
#
#   Script exemple for the dynamicShelf plugin.
#
#
# DEPENDENCIES:
#
#    maya.cmds
#
#
#########################################################################


#########################################################################
##### MODULES IMPORT
#########################################################################


    ## MAYA.CMDS
try:
    import maya.cmds as cmds
except ImportError: 
    print "maya.cmds import failed"
    
    

#########################################################################
##### FUNCTIONS
#########################################################################

class helloWorld:
    
    #####################################################################
    ## __init__
    #####################################################################
    ##
    ## Launch UI
    ##
    #####################################################################
    ##       
    ##
    #####################################################################
    def __init__(self, getWinName='helloWorldWin'):
        
        self.winTitle = "helloWorld"
        self.winName = getWinName
        
        self.deleteUI()
        self.helloWorldUI()



    #####################################################################
    ## deleteUI
    #####################################################################
    ##
    ## Delete the window if it exist
    ##
    #####################################################################
    ##       
    ##
    #####################################################################       
    def deleteUI(self, *args):
        
        if cmds.window(self.winName, exists=True):
            cmds.deleteUI(self.winName)
        if cmds.windowPref(self.winName, exists=True):
            cmds.windowPref(self.winName, remove=True )
            
    
    
    #####################################################################
    ## helloWorldUI
    #####################################################################
    ##
    ## Main UI Func
    ##
    #####################################################################
    ##       
    ##
    #####################################################################
    def helloWorldUI(self):
        
        ## Create Window
        createWin = cmds.window(self.winName, title=self.winTitle, widthHeight=(230, 20))
        
        ## Create a form layout
        mainForm = cmds.formLayout()
        
        ## helloWorldTXT
        cmds.text(label='Script exemple for the dynamicShelf plugin')
        
        
        cmds.showWindow(self.winName)
                        


helloWorldClass = helloWorld()
