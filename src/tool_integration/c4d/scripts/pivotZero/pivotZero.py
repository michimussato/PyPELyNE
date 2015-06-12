import c4d
from c4d import gui

# credits: http://forums.cgsociety.org/archive/index.php/t-1052433.html

zero = c4d.Vector( 0,0,0 )
normScale = c4d.Vector( 1,1,1 )

def main():
    objList=doc.GetActiveObjects( True )# get the selected objects
    for obj in objList:
        #print obj.GetTypeName()
        #if not obj.GetTypeName() == 'Null':
        try:
            
            oldm = obj.GetMg()
            #print oldm
            points = obj.GetAllPoints()
            #print obj.GetAllPoints()
            pcount = obj.GetPointCount()
            #print pcount
            doc.StartUndo()
            doc.AddUndo( c4d.UNDOTYPE_CHANGE, obj )
            obj.SetAbsPos( zero )
            obj.SetAbsRot( zero )
            obj.SetAbsScale( normScale )
            newm = obj.GetMg()
            for p in xrange( pcount ):
                #print ~newm*oldm*points[ p ]
                obj.SetPoint( p,~newm*oldm*points[ p ] )
        except:
            print '%s (of type %s) skipped' %( obj.GetName(), obj.GetTypeName() )

        obj.Message( c4d.MSG_UPDATE ) #Update the changes made to the object
        c4d.EventAdd()
        doc.EndUndo()
        
if __name__=='__main__':
    main()