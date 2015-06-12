import os
import maya.cmds as cmds

class computeAbsolutePaths():

	"""
	Maya object
	
	Class: computeReferences()
	Methods:
	- convertFileNodeAbsPaths()
	- convertRefNodesAbsPaths()
	"""

	def __init__( self ):
	
		try:
			import os
			import maya.cmds as cmds
		except:
			print "module import failed"
	
		self.currentWorkspace = cmds.workspace( q=True, rootDirectory=True )
		#self.currentWorkspaceParent = os.path.dirname(os.path.dirname( self.currentWorkspace ) )
		self.projectRoot = os.path.dirname( os.path.dirname( os.path.dirname( os.path.dirname( os.path.dirname( self.currentWorkspace ) ) ) ) )
		#print self.projectRoot
		self.relPrefix = os.path.relpath( self.projectRoot, self.currentWorkspace )

		self.inputRoot = os.path.join( self.currentWorkspace, "input" )
	
		self.allFileNodes = cmds.ls( type="file" )
		self.allReferenceNodes = cmds.ls( type="reference" )



	def convertFileNodeAbsPaths( self ):

		for fileNode in self.allFileNodes:

			#cmds.listAttr( file1 )
	
			cmds.select( fileNode )

			attrValue = cmds.getAttr( '.fileTextureName' )

			#print "attrValue = " + attrValue

			if os.path.isabs( attrValue ):
				try:
					print "isAbs"
					relPathPostfix = os.path.relpath( attrValue, self.projectRoot )
					relPath = self.relPathString = self.relPrefix + os.sep + relPathPostfix
					#print relPath
					print "relPath = " + relPath
					cmds.setAttr( '.fileTextureName', relPath , type='string' )
					#mel: setAttr -type "string" file1.fileTextureName "../../../../../../../../Users/michaelmussato/Desktop/desktop/Screen shot 2013-06-05 at 23.01.26.jpg"
					#python: cmds.setAttr( "file1.fileTextureName", "../../../../../../../../Users/michaelmussato/Desktop/desktop/Screen shot 2013-06-05 at 23.01.26.jpg" , type="string" )
					#proj: /Volumes/pili/projects/2014-05-19___myself___doodle/assets/AST_asset01/MDL_MAY__convertAbsoluteTexturePaths/usr/
				except:
					pass
			else:
				print "file texture path is already relative"
				pass



	def convertRefNodesAbsPaths( self ):

		for referenceNode in self.allReferenceNodes:
		
			try:
				referenceNodePathUnresolved = cmds.referenceQuery( referenceNode, filename=True, unresolvedName=True ) 
				#print "referenceNodePathUnresolved = " + referenceNodePathUnresolved
		
				#eigentlich loest maya auch relative pfade direkt auf.
				#von daher ist der check ob absolut eigenlich ueberfluessig
				#es werden einfach immer alle file-nodes aktualisiert
				#geht auch :)
				if os.path.isabs( referenceNodePathUnresolved ):
					
					relPathPostfix = os.path.relpath( referenceNodePathUnresolved, self.projectRoot )
					relPath = self.relPathString = self.relPrefix + os.sep + relPathPostfix
					print "relPath = " + relPath
		
					try:
						cmds.file( relPath, loadReference=referenceNode, options="v=0;" )
						#http://stackoverflow.com/questions/19677109/script-for-automatically-loading-reference-files-from-different-destinations-in
					except:
						pass
				
				else:
					print "reference path already relative"
				
			except:
				print "maybe we have a sharedReferenceNode here which is not associated with a reference file"
			

if __name__ == '__main__':
	compute = computeAbsolutePaths()
	compute.convertFileNodeAbsPaths()
	compute.convertRefNodesAbsPaths()
	
