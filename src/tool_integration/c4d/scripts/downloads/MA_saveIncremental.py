import c4d
import os
from c4d import gui

# Saves the current document with incremented version number
# accepts also text after number:
# i.e.: "test_script_0103this_can_be_the_artist_name.c4d"



def increaseVersion( fullPath ):
    
    fn, ext = os.path.splitext( fullPath )
    fnreverse = fn[::-1]  # reverse string

    versionString = ""
    versionNumber = 0
    beginVersionString = False
    for letter in fnreverse:
        if letter.isdigit() is True:
            beginVersionString = True
            versionString += letter
            #print( "Digit: {0}" ).format( letter )
        else:
            #print( "Non-Digit: {0}" ).format( letter )
            if beginVersionString is True:
                versionString = versionString[ ::-1 ]  # reverse string
                versionNumber = int( versionString )
                break  # first non-digit ends version string

    versionNumber += 1
    versionStringNew = str( versionNumber ).zfill( len( versionString ) )

    fnreverse = fnreverse.replace( versionString[ ::-1 ], versionStringNew[ ::-1 ], 1 )
    fullPathNew = fnreverse[ ::-1 ] + ext

    print( "Increased version {0} to {1}" ).format( versionString, versionStringNew )
    #print( "Changed path {0} to {1}" ).format( fullPath, fullPathNew )
    return fullPathNew


def saveIncremental( doc ):
    #print( 'fuck' )
    currentPath = doc.GetDocumentPath()
    currentName = doc.GetDocumentName()
    fullPathNew = increaseVersion( currentPath + os.sep + currentName )
    newPath, newName = os.path.split( fullPathNew )

    doc.SetDocumentPath( newPath )
    doc.SetDocumentName( newName )
    if c4d.documents.SaveDocument( doc, fullPathNew, saveflags=c4d.SAVEDOCUMENTFLAGS_0, format=c4d.FORMAT_C4DEXPORT ):
        print( "Saved as {0}" ).format( fullPathNew )

    else:
        print "Error whilst saving." + newPath
        gui.MessageDialog( 'Error whilst saving to ' + newPath )
        doc.SetDocumentPath( currentPath )
        doc.SetDocumentName( currentName )


if __name__=='__main__':
    saveIncremental()