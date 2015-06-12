# toggleLiveRectSelection.py

import c4d
from c4d import gui

# command toggles live selection and rectangle selection

# c4d.CallCommand(200000083) # Live Selection
# c4d.CallCommand(200000084) # Rectangle Selection



def toggleLiveRectSelection():

    doc = c4d.documents.GetActiveDocument()

    activeAction = doc.GetAction()
    #print( activeAction )
    
    if activeAction != int( 200000083 ) or int( 200000084 ) or int( 200000085 ):
        #print( '0' )
        c4d.CallCommand( 200000084 )
        
    if activeAction == int( 200000084 ):
        #print( '1' )
        c4d.CallCommand( 200000083 )
        
    elif activeAction == int( 200000083 ):
        #print( '2' )
        c4d.CallCommand( 200000085 )
        
    elif activeAction == int( 200000085 ):
        #print( '3' )
        c4d.CallCommand( 200000084 )
        
    else:
        pass
        #print( 'this case is not meant to occur' )


if __name__=='__main__':
    toggleLiveRectSelection()