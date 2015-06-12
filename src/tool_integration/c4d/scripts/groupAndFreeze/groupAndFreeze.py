import c4d
from c4d import gui
#Welcome to the world of Python
#BaseList2D.GetName()
#BaseDocument.SearchObject(name)

def groupAndFreeze():
    #gui.MessageDialog('Hello World!')
    
    padding = 3
    
    increment = 0
    
    stringBase = 'group'
    string = stringBase + '_' + str( increment ).zfill( padding )
    c4d.CallCommand( 100004772 )
    activeObjects = doc.GetActiveObjects( 0 )
    nullObject = activeObjects[ 0 ]
    #for i in activeObjects:
    #   print i
    absPos = nullObject.GetAbsPos()
    nullObject.SetAbsPos( c4d.Vector( 0, 0, 0 ) )
    nullObject.SetFrozenPos( absPos )
    
    nullObject.SetName( string )
    
    
    
    while doc.SearchObject( string ):
        increment = increment + 1
        string = stringBase + '_' + str( increment ).zfill( padding )
    
    
    
    name = gui.RenameDialog( string )
    
    #print name
    
    if name == '':
       nullObject.SetName( 'NullNullSieben' )
    else:
       nullObject.SetName( name )
     
     
    c4d.EventAdd( 0 )

if __name__=='__main__':
    groupAndFreeze()

    
    
    
