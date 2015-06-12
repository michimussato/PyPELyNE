# toggleScaleLocalGlobal.py

import c4d
from c4d import gui


# c4d.CallCommand(200000088) # Move
# c4d.CallCommand(200000089) # Scale
# c4d.CallCommand(200000090) # Rotate
# c4d.CallCommand(12156) # Coordinate System



def toggleScaleLocalGlobal():

	doc = c4d.documents.GetActiveDocument()

	activeAction = doc.GetAction()
	print( activeAction )
	
	if activeAction == int( '200000089' ):
		c4d.CallCommand(12156)
		print( 'move already active, toggling local/global' )
		
	else:
		c4d.CallCommand(200000089)
		globalChecked = c4d.IsCommandChecked(12156)
		if globalChecked == True:
			print( 'move tool activated with global already active' )
			
		elif globalChecked == False:
			c4d.CallCommand(12156)
			c4d.CallCommand(200000089)
			print( 'move tool activated and global set' )

if __name__=='__main__':
	toggleScaleLocalGlobal()