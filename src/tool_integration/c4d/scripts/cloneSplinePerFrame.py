import c4d
import time
from c4d import gui


#####################################
# Set first and last frame to render:
#startFrame=280
#endFrame=285
#deleteQueue='yes'
#####################################




def cloneSplinePerFrame( stepping ):
    
    doc = c4d.documents.GetActiveDocument()
    
    # doc.SetTime(c4d.BaseTime( frame, 25 ) )
    
    # c4d.EventAdd( 2 )
    
    #CurrentTime = doc.GetTime()
    #print(str(CurrentTime))

    # doc = c4d.documents.GetActiveDocument()
    
    activeObjects = doc.GetActiveObjects(0)
    for i in activeObjects:
        print i
    
    #print( activeObjects[ 0 ].GetTags() )
    
    fps = doc.GetFps()
    
    frame = doc.GetTime().GetFrame( fps )
    
    
    print( 'fps =   %d' %fps )
    print( 'frame = %d' %frame )
    
    errors = 0
    
    # for i in activeObjects:
        # if i.CheckType(c4d.Ospline):
            # pass
        # elif i.CheckType(c4d.Ospline):
            # errors = errors + 1
    

    #print( 'errors = %i' %errors )
    if errors == 0:
    
    #if len( activeObjects ) == 1 and activeObjects[ 0 ].CheckType(c4d.Ospline):
    
    
        #activeObject = activeObjects[ 0 ]
            
        #activeObject = activeObjects[ 0 ]
        
        #for i in range( startFrame, endFrame + 1, 1 ):
        
            
        
        # doc.SetTime(c4d.BaseTime( frame, 25 ) )
        
        # frame = doc.GetTime().GetFrame( doc.GetFps() )
        
        # if frame == i:
            # print( 'matches' )
        
        
        
        for activeObject in activeObjects:
            
            
            
            #activeObject = activeObjects[ 0 ]
            
            clone = activeObject.GetClone()
            
            cloneBaseName = str( activeObject.GetName() )
            
            increment = str( frame ).zfill( 4 )
            
            clone.SetName( cloneBaseName + '_' + increment )
            
            tagsList = clone.GetTags()
            
            for tag in tagsList:
                #print tag
                #falls tagType == 5600, dann geh zum naechsten tag
                #tagType 5600 ist PointTag, nötig, damit die curve
                #dargestellt werden kann
                if tag.GetType() == 5600: 
                    continue
                
                tag.Remove()
            
            children = clone.GetChildren()
            
            for i in children:
                #print i
                i.Remove()
            
            cloneUnTagged = doc.InsertObject( clone )
            
            
            
            print( 'object cloned at frame %s' %frame )
        
        
        doc.SetActiveObject( activeObjects[ 0 ], mode=c4d.SELECTION_NEW )


        if len( activeObjects ) > 1:
            iterator = 1
            #print len( activeObjects ) - 1
            for i in range( len( activeObjects ) - 1 ):
                #print( iterator )
                #print( 'select: %s' %activeObjects[ iterator ] )
                doc.SetActiveObject( activeObjects[ iterator ], mode=c4d.SELECTION_ADD )
                iterator = iterator + 1
        
        #Goto Next Frame
        # for i in range( stepping ):
            # c4d.CallCommand(12414)
        
        doc.SetTime( c4d.BaseTime( frame + stepping, fps ) )
        
        c4d.EventAdd( 0 )
        
        # time.sleep( 0.1 )
        
        
        
    else:
        gui.MessageDialog( 'none, too many, or non spline curve.\nselect spline curve itself.\n%i errors found.' %errors )
        print( 'none, too many, or non spline curve' )
        
        
    
    
cloneSplinePerFrame( stepping = 2 )

# doc = c4d.documents.GetActiveDocument()
# for i in range( 1, 20 ):
    # doc.SetTime(c4d.BaseTime( i, 25 ) )
    # c4d.EventAdd( 2 )
    # time.sleep( 0.1 )
