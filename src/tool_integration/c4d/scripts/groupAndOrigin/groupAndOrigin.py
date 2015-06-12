import c4d
from c4d import gui

'''
@author: michael mussato
@date:   2015-04-16
'''

'''
installation:
- copy directory content to c4d scripts folder
- restart c4d
- create shelf icon
- create shortcut

description:
groups a selection of objects and assigns a unique or custom name to the group (cancel aborts the action)
the group pivot will always be @ 0,0,0
if the items selected have an identical (direct) parent, the new group will be created as a child of this parent (and only then),
otherwise it will be created at the scene root

usage:
- change "stringBase", "stringSeparator" and "padding" to a value of your convenience
- add shortcut/add script to shelf
- select objects to be added to the group
- press shortcut/click shelf button
- use suggested name or enter custom name
'''

def allSame( list ):
    return all( x == list[ 0 ] for x in list )


def groupAndFreeze():
    
    stringBase = 'group'
    stringSeparator = '_'
    padding = 3
    
    increment = 1
    string = stringBase + '_' + str( increment ).zfill( padding )
    
    objList = doc.GetActiveObjects( True )
    
    doc.StartUndo()
    
    nullObject = c4d.BaseObject( c4d.Onull )
    doc.AddUndo( c4d.UNDOTYPE_NEW, nullObject )
    activeObject = doc.SetActiveObject( nullObject, mode=0 )
    
    doc.InsertObject( nullObject )
    
    parentList = []
    
    for obj in objList:
        parent = obj.GetUp()
        print parent
        parentList.append( parent )
        doc.AddUndo( c4d.UNDOTYPE_CHANGE, obj )
        obj.InsertUnder( nullObject )
        
    if allSame( parentList ) and not parentList[ 0 ] == None:
        nullObject.InsertUnder( parentList[ 0 ] )
    
    while doc.SearchObject( string ):
        increment = increment + 1
        string = stringBase + '_' + str( increment ).zfill( padding )
        
    nullObject.SetName( string )
    
    name = gui.RenameDialog( string )

    if name == '':
        nullObject.SetName( 'NullNullSieben' )
    elif name == None:
        print 'aborted...'
        doc.EndUndo()
        doc.DoUndo( multiple=0 )
        return
    else:
        nullObject.SetName( name )
    
    
     
     
    c4d.EventAdd( 0 )
    doc.EndUndo()

if __name__=='__main__':
    groupAndFreeze()

    
    
    
