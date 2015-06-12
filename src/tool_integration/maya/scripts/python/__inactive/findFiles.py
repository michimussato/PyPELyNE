import os

sourceDir1 = "/Volumes/pili/projects/2009-01-10___myself___mazda787b/assets/AST_mazda/MDL_MAY__mazda_midres/output"
sourceDir2 = "/Volumes/pili/projects/2009-01-10___myself___mazda787b/assets/AST_mazda/MDL_MAY__test/input"

for rootOfFile, dirs, files in os.walk( sourceDir2, followlinks=True ): 
# 	for dir in dirs:
# 		print dir
# 		print "hallo"
	for file in files: 
		if file.lower().endswith( '.obj' ) or file.lower().endswith( '.ma' ): 
			print rootOfFile
			print file