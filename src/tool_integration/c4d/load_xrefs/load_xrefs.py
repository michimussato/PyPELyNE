#load xrefs

import os

try:
    import c4d
    from c4d import gui
except:
    print '---------------------------------------------------------------------'
    print 'could not load modules.'
    print 'this script must be run in cinema 4d.'

def getFiles():
    
    # Windows paths as rawstring! r'<string>'
    xrefPath = r'C:\Users\render.admin\Desktop\test\xrefs'

    xrefFiles = os.listdir( xrefPath )
    xrefSuffix = r'.c4d'
    
    if len( xrefFiles ) == '0':
        print 'no files in folder found'
    else:
        print '---------------------------------------------------------------------'
        print 'c4d-files in folder:'
        for i in xrefFiles:
            fullPath = os.path.join( xrefPath, i )
            if i.endswith( xrefSuffix ) and os.path.isfile( fullPath ):
                print 'full path    = %s' %fullPath
                print 'filename     = %s' %i
                print 'without ext  = %s' %os.path.splitext( i )[ 0 ]
            else:
                print 'has either no c4d-suffix or it is not a file: %s' %( fullPath )
                

            
def getXrefs():
    # from http://frenchcinema4d.fr/archive/index.php/t-75532.html
    try:
        objects = doc.GetObjects()
        for obj in objects:
            if obj.CheckType( c4d.Oxref ):
                print obj

                print 'ID_CA_XREF_PIVOT_GROUP = %s' %obj[c4d.ID_CA_XREF_PIVOT_GROUP]
                print 'ID_CA_XREF_ANIM_GROUP = %s' %obj[c4d.ID_CA_XREF_ANIM_GROUP]
                print 'ID_CA_XREF_SHOWOBJECTS = %s' %obj[c4d.ID_CA_XREF_SHOWOBJECTS]
                print 'ID_CA_XREF_FILE = %s' %obj[c4d.ID_CA_XREF_FILE]
                print 'ID_CA_XREF_PROXY_FILE = %s' %obj[c4d.ID_CA_XREF_PROXY_FILE]
                print 'ID_CA_XREF_SWAP = %s' %obj[c4d.ID_CA_XREF_SWAP]
                print 'ID_CA_XREF_REFRESH = %s' %obj[c4d.ID_CA_XREF_REFRESH]
                print 'ID_CA_XREF_OPTIONS = %s' %obj[c4d.ID_CA_XREF_OPTIONS]
                print 'ID_CA_XREF_LOADED = %s' %obj[c4d.ID_CA_XREF_LOADED]
                print 'ID_CA_XREF_NAMESPACE = %s' %obj[c4d.ID_CA_XREF_NAMESPACE]
                print 'ID_CA_XREF_EDIT = %s' %obj[c4d.ID_CA_XREF_EDIT]
                print 'ID_CA_XREF_FILE_SELECT = %s' %obj[c4d.ID_CA_XREF_FILE_SELECT]
                print 'ID_CA_XREF_PROXY_FILE_SELECT = %s' %obj[c4d.ID_CA_XREF_PROXY_FILE_SELECT]
                print 'ID_CA_XREF_ANIMATE = %s' %obj[c4d.ID_CA_XREF_ANIMATE]
                print 'ID_CA_XREF_TIME = %s' %obj[c4d.ID_CA_XREF_TIME]
                print 'ID_CA_XREF_OFFSET = %s' %obj[c4d.ID_CA_XREF_OFFSET]
                print 'ID_CA_XREF_SCALE = %s' %obj[c4d.ID_CA_XREF_SCALE]
                print 'ID_CA_XREF_GENERATOR = %s' %obj[c4d.ID_CA_XREF_GENERATOR]
                print 'ID_CA_XREF_PIVOT_POS = %s' %obj[c4d.ID_CA_XREF_PIVOT_POS]
                print 'ID_CA_XREF_PIVOT_SCL = %s' %obj[c4d.ID_CA_XREF_PIVOT_SCL]
                print 'ID_CA_XREF_PIVOT_ROT = %s' %obj[c4d.ID_CA_XREF_PIVOT_ROT]
                print 'ID_CA_XREF_REFID = %s' %obj[c4d.ID_CA_XREF_REFID]
                print 'ID_CA_XREF_REF_NAME = %s' %obj[c4d.ID_CA_XREF_REF_NAME]
                print 'ID_CA_XREF_RELATIVE = %s' %obj[c4d.ID_CA_XREF_RELATIVE]
                print 'ID_CA_XREF_SWAP_STATE = %s' %obj[c4d.ID_CA_XREF_SWAP_STATE]
                print 'ID_CA_XREF_REF_REV = %s' %obj[c4d.ID_CA_XREF_REF_REV]
                print 'ID_CA_XREF_FLAGS = %s' %obj[c4d.ID_CA_XREF_FLAGS]
                print 'ID_CA_XREF_REF_STATEFILE = %s' %obj[c4d.ID_CA_XREF_REF_STATEFILE]
                print 'ID_CA_XREF_COPYID = %s' %obj[c4d.ID_CA_XREF_COPYID]
                print 'ID_CA_XREF_DATA_CONTAINER = %s' %obj[c4d.ID_CA_XREF_DATA_CONTAINER]


                '''
                # from C:\Program Files\MAXON\CINEMA 4D R14\resource\modules\ca\res\description\oxref.h
                ID_CA_XREF_PIVOT_GROUP = 5000,
                ID_CA_XREF_ANIM_GROUP,
                ID_CA_XREF_SHOWOBJECTS = 1000,
                ID_CA_XREF_FILE,
                ID_CA_XREF_PROXY_FILE,
                ID_CA_XREF_SWAP,
                ID_CA_XREF_REFRESH,
                ID_CA_XREF_OPTIONS,
                ID_CA_XREF_LOADED,
                ID_CA_XREF_NAMESPACE,
                ID_CA_XREF_EDIT,
                ID_CA_XREF_FILE_SELECT,
                ID_CA_XREF_PROXY_FILE_SELECT,
                ID_CA_XREF_ANIMATE,
                ID_CA_XREF_TIME,
                ID_CA_XREF_OFFSET,
                ID_CA_XREF_SCALE,
                ID_CA_XREF_GENERATOR,
                ID_CA_XREF_PIVOT_POS,
                ID_CA_XREF_PIVOT_SCL,
                ID_CA_XREF_PIVOT_ROT,

                ID_CA_XREF_REFID = 10000,
                ID_CA_XREF_REF_NAME,
                ID_CA_XREF_RELATIVE,
                ID_CA_XREF_SWAP_STATE,
                ID_CA_XREF_REF_REV,
                ID_CA_XREF_FLAGS,
                ID_CA_XREF_REF_STATEFILE,
                ID_CA_XREF_COPYID,
                ID_CA_XREF_DATA_CONTAINER,
                '''

                objects.extend(obj.GetChildren())

                # to try out stuff

                obj[c4d.ID_CA_XREF_SHOWOBJECTS] = False
                obj[c4d.ID_CA_XREF_LOADED] = False
                obj[c4d.ID_CA_XREF_FILE] = r'C:\Users\render.admin\Desktop\test\xrefs\model.c4d'
                obj[c4d.ID_CA_XREF_GENERATOR] = True

                c4d.EventAdd()

            else:
                print 'obj %s is not xref' %obj
    except:
        print 'this procedure is meant to be run in c4d'
    
if __name__ == '__main__':
    getFiles()
    getXrefs()