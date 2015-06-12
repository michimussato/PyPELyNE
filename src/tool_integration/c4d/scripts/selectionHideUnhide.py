# selectionHideUnhide.py

import c4d
from c4d import gui

    # object()[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR]=0 (=visible in editor)
    # object()[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR]=1 (=invisible in editor)


    
def main():
    
    doc = c4d.documents.GetActiveDocument()
    
    selectionModel = doc.GetSelection()
    
    print( c4d.GetTypeName( selectionModel ) )
    
    
if __name__=='__main__':
    main()
  
    
'''    
    
class selectionHideUnhide():
    
    def __init__(self):
    
        self.doc = c4d.documents.GetActiveDocument()
        global selectionModel
        
    
    def hideSelected(self):
    
        self.selectionModel = self.doc.GetSelection()
        print( self.selectionModel )
        
        c4d.CallCommand(12187) # Polygons
        
        c4d.CallCommand(200000084) # Rectangle Selection
        #tool()[c4d.MDATA_SELECTION_VISIBLE]=False
        
        
        
        c4d.CallCommand(13323) # Select All
        
        #select = c4d.BaseSelect.__init__()
        
        #select.ToggleAll( 0 )
        
        #c4d.CallCommand(12474) # Hide Unselected
        c4d.CallCommand(12473) # Hide Selected
        
        c4d.CallCommand(12298) # Model
        
        c4d.CallCommand(12475) # Unhide All
        
    def unhideHidden(self):
        c4d.CallCommand(12298) # Model
        self.doc.SetSelection( self.selectionModel, 0 )
        
        c4d.CallCommand(12187) # Polygons
        c4d.CallCommand(200000084) # Rectangle Selection
        #c4d.CallCommand(13323) # Select All
        c4d.CallCommand(12475) # Unhide All

if __name__=='__main__':
    obj = selectionHideUnhide()
    obj.hideSelected()
    obj.unhideHidden()
    #obj.unhide()


'''