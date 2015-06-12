import os, win32file


#http://stackoverflow.com/questions/1447575/symlinks-on-windows
#fileSrc = folder
#fileTarget = link

directory = os.chdir( r'C:\Users\michael.mussato.SCHERRERMEDIEN\Desktop\TestDir\folder' )


fileSrc = ( r'..\otherFolder\link' )
fileTarget = ( r'.\src' )

win32file.CreateSymbolicLink( fileSrc, fileTarget, 1 )