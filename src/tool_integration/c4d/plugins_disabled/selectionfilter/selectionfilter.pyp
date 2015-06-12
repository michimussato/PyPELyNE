########################
# Selectionfilter Plugin
# Cathrin Paulsen
# 2014
# www.pixcube.com 
########################


import c4d
import os
import sys
from c4d import gui, utils, documents, bitmaps, plugins


#ID from plugincafe

PLUGIN_ID = 1033775 

GROUP1 = 0000   
GROUP2 = 0001   
BUTTON1= 1001   
BUTTON2 = 1002     
CHECKBOX1 = 1011
CHECKBOX2 = 1012
CHECKBOX3 = 1013
CHECKBOX4 = 1014
CHECKBOX5 = 1015
CHECKBOX6 = 1016
CHECKBOX7 = 1017
CHECKBOX8 = 1018
CHECKBOX9 = 1019
CHECKBOX10 = 1020
CHECKBOX11 = 1021
CHECKBOX12 = 1022
CHECKBOX12 = 102


class MyDialog(gui.GeDialog):
    
    def GetSelectionFilter(self):
        doc = documents.GetActiveDocument()
        bc = doc.GetData()
        selfil = bc.GetLong(c4d.DOCUMENT_SELECTIONFILTER)
        return selfil

    def SetFilter(self, f):
        doc = documents.GetActiveDocument()
        bc = doc.GetData()
        bc.SetLong(c4d.DOCUMENT_SELECTIONFILTER, f)
        doc.SetData(bc)
        c4d.EventAdd()  
    
    def CreateLayout(self):
        self.MenuFlushAll()
        
        self.SetTitle("Selection Filter")
        
        self.GroupBegin(GROUP1, c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT, 3, 0, "filter")
        self.GroupBorder(c4d.BORDER_GROUP_IN)     
        self.GroupBorderSpace(20,5,20,5)
        self.AddCheckbox(CHECKBOX1, c4d.BFH_SCALEFIT, 0, 0, "spline")
        self.AddCheckbox(CHECKBOX2, c4d.BFH_SCALEFIT, 0, 0, "polygon")
        self.AddCheckbox(CHECKBOX3, c4d.BFH_SCALEFIT, 0, 0, "null")
        self.AddCheckbox(CHECKBOX4, c4d.BFH_SCALEFIT, 0, 0, "generator")
        self.AddCheckbox(CHECKBOX5, c4d.BFH_SCALEFIT, 0, 0, "hypernurbs")
        self.AddCheckbox(CHECKBOX6, c4d.BFH_SCALEFIT, 0, 0, "deformer")
        self.AddCheckbox(CHECKBOX7, c4d.BFH_SCALEFIT, 0, 0, "camera")
        self.AddCheckbox(CHECKBOX8, c4d.BFH_SCALEFIT, 0, 0, "light")
        self.AddCheckbox(CHECKBOX9, c4d.BFH_SCALEFIT, 0, 0, "scene")
        self.AddCheckbox(CHECKBOX10, c4d.BFH_SCALEFIT, 0, 0, "particle")
        self.AddCheckbox(CHECKBOX11, c4d.BFH_SCALEFIT, 0, 0, "other")
        self.AddCheckbox(CHECKBOX12, c4d.BFH_SCALEFIT, 0, 0, "joint")
        self.GroupEnd() 
        
        self.GroupBegin(GROUP2, 20, c4d.BFH_SCALEFIT, 3, 0)
        self.GroupBorderSpace(20,5,20,5)
        self.AddButton(BUTTON1, c4d.BFH_SCALEFIT, 0, 0, "all")
        self.AddButton(BUTTON2, c4d.BFH_SCALEFIT, 0, 0, "none")
        self.GroupEnd()
        
        return True
    
    def InitValues (self):
        sf = self.GetSelectionFilter()
        f = sf 
        
        if not(sf & c4d.SELECTIONFILTERBIT_SPLINE):
            self.SetBool(CHECKBOX1, True)
        if not(sf & c4d.SELECTIONFILTERBIT_POLYGON):
            self.SetBool(CHECKBOX2, True)
        if not(sf & c4d.SELECTIONFILTERBIT_NULL):
            self.SetBool(CHECKBOX3, True)
        if not(sf & c4d.SELECTIONFILTERBIT_GENERATOR):
            self.SetBool(CHECKBOX4, True)
        if not(sf & c4d.SELECTIONFILTERBIT_HYPERNURBS):
            self.SetBool(CHECKBOX5, True)
        if not(sf & c4d.SELECTIONFILTERBIT_DEFORMER):
            self.SetBool(CHECKBOX6, True)
        if not(sf & c4d.SELECTIONFILTERBIT_CAMERA):
            self.SetBool(CHECKBOX7, True)
        if not(sf & c4d.SELECTIONFILTERBIT_LIGHT):
            self.SetBool(CHECKBOX8, True)
        if not(sf & c4d.SELECTIONFILTERBIT_SCENE):
            self.SetBool(CHECKBOX9, True)
        if not(sf & c4d.SELECTIONFILTERBIT_PARTICLE):
            self.SetBool(CHECKBOX10, True)
        if not(sf & c4d.SELECTIONFILTERBIT_OTHER):
            self.SetBool(CHECKBOX11, True)
        if not(sf & c4d.SELECTIONFILTERBIT_JOINT):
            self.SetBool(CHECKBOX12, True)        
     
        return True
  
    def Command(self, id, msg):
        sf = self.GetSelectionFilter()
        f = sf

        #SPLINE
        if id==CHECKBOX1:
            if self.GetBool(CHECKBOX1): 
                f = sf &~ c4d.SELECTIONFILTERBIT_SPLINE
            elif not self.GetBool(CHECKBOX1):
                 f = sf | c4d.SELECTIONFILTERBIT_SPLINE
  
        #POLYGON
        elif id==CHECKBOX2:
            if self.GetBool(CHECKBOX2):        
                 f = sf &~ c4d.SELECTIONFILTERBIT_POLYGON
            elif not self.GetBool(CHECKBOX2):
                f = sf | c4d.SELECTIONFILTERBIT_POLYGON
        #NULL
        elif id==CHECKBOX3:
            if self.GetBool(CHECKBOX3):        
                f = sf &~ c4d.SELECTIONFILTERBIT_NULL
            elif not self.GetBool(CHECKBOX3):
                f = sf | c4d.SELECTIONFILTERBIT_NULL
 
        #GENERATOR
        elif id==CHECKBOX4:
            if self.GetBool(CHECKBOX4):        
                f = sf &~ c4d.SELECTIONFILTERBIT_GENERATOR
            elif not self.GetBool(CHECKBOX4):
                f = sf | c4d.SELECTIONFILTERBIT_GENERATOR                      
    
        #HYPERNURBS
        elif id==CHECKBOX5:
            if self.GetBool(CHECKBOX5):        
                f = sf &~ c4d.SELECTIONFILTERBIT_HYPERNURBS
            elif not self.GetBool(CHECKBOX5):
                f = sf | c4d.SELECTIONFILTERBIT_HYPERNURBS         
    
        #DEFORMER
        elif id==CHECKBOX6:
            if self.GetBool(CHECKBOX6):        
                f = sf &~ c4d.SELECTIONFILTERBIT_DEFORMER
            elif not self.GetBool(CHECKBOX6):
                f = sf | c4d.SELECTIONFILTERBIT_DEFORMER

    
        #CAMERA
        elif id==CHECKBOX7:
            if self.GetBool(CHECKBOX7):        
                f = sf &~ c4d.SELECTIONFILTERBIT_CAMERA
            elif not self.GetBool(CHECKBOX7):
                f = sf | c4d.SELECTIONFILTERBIT_CAMERA
        #LIGHT
        elif id==CHECKBOX8:
            if self.GetBool(CHECKBOX8):        
                f = sf &~ c4d.SELECTIONFILTERBIT_LIGHT
            elif not self.GetBool(CHECKBOX8):
                f = sf | c4d.SELECTIONFILTERBIT_LIGHT
    
        #SCENE
        elif id==CHECKBOX9:
            if self.GetBool(CHECKBOX9):        
                f = sf &~ c4d.SELECTIONFILTERBIT_SCENE
            elif not self.GetBool(CHECKBOX9):
                f = sf | c4d.SELECTIONFILTERBIT_SCENE
                        
        #PARTICLE
        elif id==CHECKBOX10:
            if self.GetBool(CHECKBOX10):        
                f = sf &~ c4d.SELECTIONFILTERBIT_PARTICLE
            elif not self.GetBool(CHECKBOX10):
                f = sf | c4d.SELECTIONFILTERBIT_PARTICLE
        #OTHER
        elif id==CHECKBOX11:
            if (sf & c4d.SELECTIONFILTERBIT_OTHER):
                f = sf &~ c4d.SELECTIONFILTERBIT_OTHER
            elif not self.GetBool(CHECKBOX11):
                f = sf | c4d.SELECTIONFILTERBIT_OTHER
    
        #JOINT
        elif id==CHECKBOX12:
            if self.GetBool(CHECKBOX12):        
                f = sf &~ c4d.SELECTIONFILTERBIT_JOINT
            elif not self.GetBool(CHECKBOX12):
                f = sf | c4d.SELECTIONFILTERBIT_JOINT
                        
        elif id==BUTTON1:
            f = 0
            
        elif id==BUTTON2:
            f = -1
            
        self.SetFilter(f)
        
        self.LayoutFlushGroup(GROUP1)
        self.CreateLayout()
        self.InitValues()
        self.LayoutChanged(GROUP1)
         
        return True
    
    
class MyDialog_Main(plugins.CommandData):

    
    dialog = None
    
    def Execute (self, doc):
        if self.dialog is None:
            self.dialog = MyDialog()
        return self.dialog.Open(dlgtype = c4d.DLG_TYPE_ASYNC, pluginid = PLUGIN_ID, defaultw=300, defaulth=50,)
    
    def RestoreLayout (self, sec_ref):
        if self.dialog is None:
            self.dialog = MyDialog()
        return self.dialog.Restore(pluginid=Plugin_ID, secret=sec_ref)
        
if __name__=="__main__":
    path, fn = os.path.split(__file__)
    bmp = bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(path, "res/icon/", "selfil.tif"))
    ok = plugins.RegisterCommandPlugin(PLUGIN_ID, "Selectionfilter",0,bmp,"",MyDialog_Main())
    

