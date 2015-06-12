import c4d
from c4d import gui
import os, getpass, sys

#Welcome to the world of fucking c4d Python
###############
MA_path = r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\src\tool_integration\c4d\scripts'
###############

#import downloads.MA_saveIncremental as si


# as for now, padding MUST BE 4 (filename_0000.c4d)

#TODO:
#- padding should be recognized automatically
#- if save-checkbox in "render settings/save/ is unchecked: skip rData[c4d.RDATA_PATH]incrementation
#- if "render settings/save/file" has no numbering/padding: give warning
#- if "render settings/save/file" is empty: give warning
#- maybe get the basename of rData[c4d.RDATA_PATH], take the filename, join it and use it as rData[c4d.RDATA_PATH] path

try:
    
    #sys.path.append( 'C:\\Users\\michael.mussato.SCHERRERMEDIEN\\Dropbox\\development\\workspace\\PyPELyNE\\src\\tool_integration\\c4d\\scripts\\downloads' )
    sys.path.append( MA_path )
    #sys.path.append( '\\downloads' )
    import MA_saveIncremental as si
except:
    print( 'unable to load module MA_saveIncremental. terminated.' )
    

def saveIncrementalAndUpdateOutputPath():
    
    docName = doc.GetDocumentName()
    docFile = os.path.basename( doc[c4d.DOCUMENT_FILEPATH] )
    docFilePath = os.path.dirname( os.path.realpath( doc[c4d.DOCUMENT_FILEPATH] ) )
    projectRoot = os.path.dirname( docFilePath )
    print projectRoot
    docName,ext = os.path.splitext( docName )
    base,increment = docName[ :-4 ],docName[ -4: ]
    
    #increment = int( increment ) + 1
    increment = str( int( increment ) + 1 ).zfill( len( increment ) )
    
    print( 'docName = %s' %docName )
    #print( 'increment = %s' %increment )
    
    rDataList = doc.GetFirstRenderData()
    
    while rDataList:
        #print( 'renderData = %s' %rDataList.GetData() )
        
        
    
        #rData = doc.GetActiveRenderData()
        rData = rDataList
        
        rDataName = rData.GetName()
        
        #print( 'rDataName = %s' %rDataName )
        
        saveActive = rData[c4d.RDATA_SAVEIMAGE]
        saveActiveMP = rData[c4d.RDATA_MULTIPASS_SAVEIMAGE]
        
        print( 'saveActive = %s' %saveActive )
        print( 'saveActiveMP = %s' %saveActiveMP )
        
        outputPath = rData[c4d.RDATA_PATH][ :-4 ]
        outputPathParent = os.path.dirname( outputPath )
        outputIncrement = rData[c4d.RDATA_PATH][ -4: ]
        
        
        
        #print( 'outputPath = %s' %outputPath )
        #print( 'outputPathParent = %s' %outputPathParent )
        #print( 'outputIncrement = %s' %outputIncrement )
        
        outputPathMP = rData[c4d.RDATA_MULTIPASS_FILENAME][ :-4 ]
        outputPathParentMP = os.path.dirname( outputPathMP )
        outputIncrementMP = rData[c4d.RDATA_MULTIPASS_FILENAME][ -4: ]
        
        #print( 'outputPathMP = %s' %outputPathMP )
        #print( 'outputPathParentMP = %s' %outputPathParentMP )
        #print( 'outputIncrementMP = %s' %outputIncrementMP )
        



        rDataStripIncrement = outputPath
        
        rDataStripIncrementMP = outputPathMP
        
        
        rDataNewIncrement = str( docName[ :-4 ] ) + str( increment ) + '__' + rDataName
        rDataNewPath = os.path.join( outputPathParent, rDataNewIncrement )
        rDataNewPathFull = os.path.join( projectRoot, 'output', rDataNewPath )
        if not os.path.exists( rDataNewPathFull ) and not saveActive == 0:
            os.makedirs( rDataNewPathFull, mode=0777 )
        print rDataNewPathFull
        
        rDataNewIncrementMP = str( docName[ :-4 ] ) + str( increment ) + '__' + rDataName + '_' + 'mp'
        rDataNewPathMP = os.path.join( outputPathParentMP, rDataNewIncrementMP )
        rDataNewPathFullMP = os.path.join( projectRoot, 'output', rDataNewPathMP )
        if not os.path.exists( rDataNewPathFullMP ) and not saveActiveMP == 0:
            os.makedirs( rDataNewPathFullMP, mode=0777 )
        print rDataNewPathFullMP
        
        #print( 'rDataNewPath = %s' %rDataNewPath )

        #print( 'rDataStripIncrement = %s' %rDataStripIncrement )
        #print( 'rDataNewIncrement = %s' %rDataNewIncrement )
        #print( 'rDataNewPath = %s' %rDataNewPath )

        #outputDir = os.path.splitext( docName )
        rData[c4d.RDATA_PATH] = rDataNewPathFull
        
        rData[c4d.RDATA_MULTIPASS_FILENAME] = rDataNewPathFullMP
        
        #print rData[c4d.RDATA_FORMAT]
        #ID 1016606 = OpenEXR
        rData[c4d.RDATA_MULTIPASS_SAVEFORMAT] = 1016606
        rData[c4d.RDATA_NAMEFORMAT] = 6
        rData[c4d.RDATA_MULTIPASS_SAVEONEFILE] = 1
        rData[c4d.RDATA_MULTIPASS_SUFFIX] = 0
        
        
        
        rDataList = rDataList.GetNext()
    
    

    
    
    currentUser = getpass.getuser()
    doc[c4d.DOCUMENT_INFO_AUTHOR] = currentUser
    
    print( 'author information updated with value: %s' %currentUser )
    
    si.saveIncremental( doc )
    
    #c4d.CallCommand( 600000072 ) # Save Incremental...
    
    c4d.EventAdd()

    
    
if __name__=='__main__':
    saveIncrementalAndUpdateOutputPath()
