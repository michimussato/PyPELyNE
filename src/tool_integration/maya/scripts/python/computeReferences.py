import os
import maya.cmds as cmds
import re

class computeReferences():

    def __init__( self ):
        try:
            import os
            import maya.cmds as cmds
            import re
        except:
            print "module import failed"
    
        self.currentWorkspace = cmds.workspace( q=True, rootDirectory=True )
        
        self.currentWorkspaceParent = os.path.dirname(os.path.dirname( self.currentWorkspace ) )
        self.inputRoot = os.path.join( self.currentWorkspace, "input" )
    
        self.allFileNodes = cmds.ls( type="file" )
        self.allReferenceNodes = cmds.ls( type="reference" )
    
        self.filter = [ '.DS_Store', 'sharedReferenceNode' ]
        
        #self.referencesLoadedRN = []
        
        self.referencesToLoad = []
        self.referencesToUnload = []
                        

    def synchronizeReferences( self ):

        print "____self.currentWorkspace = " + self.currentWorkspace

        print "____self.currentWorkspaceParent = " + self.currentWorkspaceParent

        print "____self.inputRoot = " + self.inputRoot
    
        referencesLoadedRN = [ x for x in cmds.ls( type="reference" ) if x not in self.filter ]
        print "____referencesLoadedRN = " + str( referencesLoadedRN )
        referencesLoaded = [ x.replace( "RN", "" ) for x in referencesLoadedRN ]
        print "____referencesLoaded = " + str( referencesLoaded )
    
        referencesPipedFull = [ os.path.join(rootOfFile, inputFile) for rootOfFile, dirs, files in os.walk( self.inputRoot, followlinks=True ) for inputFile in files ]
        print "____referencesPipedFull = " + str( referencesPipedFull )

        referencesPipedFullFiltered = [ x for x in referencesPipedFull if x not in self.filter ]
        #filter function:
        [ ( referencesPipedFullFiltered.remove( x ) ) for y in self.filter for x in referencesPipedFullFiltered if re.search( str( y ), x ) ]
        print "____referencesPipedFullFiltered = " + str( referencesPipedFullFiltered )
    
        referencesPipedPrefix = [ os.path.splitext( x )[0] for x in referencesPipedFullFiltered ]
        print "____referencesPipedPrefix = " + str( referencesPipedPrefix )
        referencesPipedExtension = [ os.path.splitext( x )[1] for x in referencesPipedFullFiltered ]
        print "____referencesPipedExtension = " + str( referencesPipedExtension )
        referencesPipedFileNames = [ a + b for a, b in zip( referencesPipedPrefix, referencesPipedExtension ) ]
        print "____referencesPipedFileNames = " + str( referencesPipedFileNames )
        referencesPipedPrefixBasename = []
        for x in referencesPipedPrefix:
            referencesPipedPrefixBasename.append( os.path.basename( x ) )
        print "____referencesPipedPrefixBasename = " + str( referencesPipedPrefixBasename )
    
    
        referencesToLoad = [ x for x in referencesPipedFileNames if os.path.basename( os.path.splitext( x )[0] ) not in referencesLoaded ]
        print "____referencesToLoad = " + str( referencesToLoad )
    
        referencesToUnload = [ ( s + "RN" ) for s in referencesLoaded if not any(xs in s for xs in referencesPipedPrefixBasename if s == xs) ]
        print "____referencesToUnload = " + str( referencesToUnload )
            

        self.referencesToLoad = referencesToLoad
        self.referencesToUnload = referencesToUnload
        
            
#        return referencesToLoad
        
        
    def referencesLoad( self ):
        
        for reference in self.referencesToLoad:
            if os.path.isabs( reference ):
                reference = os.path.relpath( reference, self.currentWorkspace )
                print "need to load %s" %reference

                if reference.lower().endswith( '.ma' ):

                    print "____MA found"
                    print "____reference = " + reference

                    try:
                        cmds.file( reference, reference=True, type="mayaAscii", loadReferenceDepth="all", mergeNamespacesOnClash=True, namespace=":", options="v=0;" )
                        #cmds.file( fullReferenceFilePath, type="mayaAscii", loadReferenceDepth="all", mergeNamespacesOnClash=True, options="v=0;" )
                        #mel for mayaAscii reference import:
                        #file -r -type "mayaAscii" -gl -loadReferenceDepth "all" -mergeNamespacesOnClash true -namespace ":" -options "v=0;" "/Volumes/pili/projects/2009-01-10___myself___mazda787b/assets/AST_mazda/SHD_MAY__mazda_shading_copy/input/AST_mazda__MDL_MAY__mazda_midres__MDL_mazda_ma/MDL_mazda_ma.ma";
                        #cmds.file( "/Volumes/pili/projects/2009-01-10___myself___mazda787b/assets/AST_mazda/SHD_MAY__mazda_shading_copy/input/AST_mazda__MDL_MAY__mazda_midres__MDL_mazda_ma/MDL_mazda_ma.ma", reference=True, type="mayaAscii", loadReferenceDepth="all", mergeNamespacesOnClash=True, namespace=":", options="v=0;" )
                        print "reference %s loaded" %reference

                    except:
                        print "cannot reference MA... dunno why."


                elif reference.lower().endswith( '.obj' ):

                    pluginLoaded = cmds.pluginInfo( 'objExport', query=True, loaded=True )

                    if pluginLoaded == False:

                        try:
                            cmds.loadPlugin( 'objExport' )
                        except:
                            print "cannot load objExport plugin"

                    print "____OBJ found"
                    print "____reference = " + reference

                    try:
                        cmds.file( reference, reference=True, type="OBJ", loadReferenceDepth="all", mergeNamespacesOnClash=False, namespace=( os.path.basename( reference ).split(os.extsep, 1)[0] ), options="mo=1;" )
                        #mel for OBJ reference import:
                        #file -r -type "OBJ" -gl -loadReferenceDepth "all" -mergeNamespacesOnClash false -namespace "MDL_mazda_obj__MSH__mazda_BOLT_wingSocket" -options "mo=1" "/Volumes/pili/projects/2009-01-10___myself___mazda787b/assets/AST_mazda/RIG_MAY__mazda_rig_copy/input/AST_mazda__MDL_MAY__mazda_midres__MDL_mazda_obj/MDL_mazda_obj__MSH__mazda_BOLT_wingSocket.obj";
                        print "reference %s loaded" %reference


                    except:
                        print "cannot reference OBJ... dunno why."

                elif reference.lower().endswith( '.abc' ):

                    pluginLoaded = cmds.pluginInfo( 'AbcImport', query=True, loaded=True )

                    if pluginLoaded == False:

                        try:
                            cmds.loadPlugin( 'AbcImport' )
                        except:
                            print "cannot load AbcImport plugin"

                    print "ABC found"
                    print "____pipeline cache = " + reference

                    try:
                        cmds.AbcImport( os.path.join( self.currentWorkspace, reference ), mode="import" )
                        print "pipeline cache %s imported" %reference

                    except:
                        print "cannot import ABC... dunno why."


                elif reference.lower().endswith( '.fbx' ):

                    pluginLoaded = cmds.pluginInfo( 'fbxmaya', query=True, loaded=True )

                    if pluginLoaded == False:

                        try:
                            cmds.loadPlugin( 'fbxmaya' )
                        except:
                            print "cannot load fbxmaya plugin"

                    print "FBX found"
                    print "____fbx = " + reference

                    try:
                        cmds.file( reference, reference=True, type="FBX", loadReferenceDepth="all", mergeNamespacesOnClash=False, namespace=( os.path.basename( reference ).split(os.extsep, 1)[0] ), options="mo=1;" )
                        #mel for OBJ reference import:
                        #file -r -type "OBJ" -gl -loadReferenceDepth "all" -mergeNamespacesOnClash false -namespace "MDL_mazda_obj__MSH__mazda_BOLT_wingSocket" -options "mo=1" "/Volumes/pili/projects/2009-01-10___myself___mazda787b/assets/AST_mazda/RIG_MAY__mazda_rig_copy/input/AST_mazda__MDL_MAY__mazda_midres__MDL_mazda_obj/MDL_mazda_obj__MSH__mazda_BOLT_wingSocket.obj";
                        print "reference %s loaded" %reference
                    except:
                        print "cannot load FBX... dunno why."

                else:
                    print "some not fitting shit found. input probably not live."
                    print "____shit = " + reference

        

            
            
    def referencesUnload( self ):
    
        for reference in self.referencesToUnload:
            print "need to unload %s" %reference
            try:
                #TODO: maybe choice between unload or remove would be good...
                cmds.file( removeReference=True, referenceNode=reference )
                print "reference %s removed" %reference
            except:
                print 'could not unload reference:', reference

    def referencesReload ( self ):
        for reference in self.allReferenceNodes:
            try:
                cmds.file( unloadReference=reference )
                cmds.file( loadReference=reference )
            except:
                print 'could not reload reference:', reference

    def doItAll( self ):
        self.synchronizeReferences()
        self.synchronizeReferences()
        self.referencesLoad()
        self.referencesUnload()
        self.referencesReload()
        
        
if __name__ == "__main__":
    compute = computeReferences()
    compute.synchronizeReferences()
    compute.referencesLoad()
    compute.referencesUnload()
    compute.referencesReload()
