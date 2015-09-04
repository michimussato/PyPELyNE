###Global
#files matching items in exclusions get removed!
exclusions                = [ '.mayaSwatches', '.DS_Store', 'Thumbs.db', '.com.apple.timemachine.supported', 'desktop.ini' ]
audioExtensions           = [ '.mp3', '.m4a', '.mp4' ]
imageExtensions           = [ '.jpg', '.exr', '.tga', '.png', '.tiff', '.tif', '.bmp', '.gif' ]
movieExtensions           = [ '.mov', '.avi' ]
archiveSeparator          = '_____'
useServer                 = False
screenCastActive          = True


###Server
serverIP                  = r'192.168.0.22'
serverPort                = r'50001'
serverPortRange           = r'5'
projectsRootServer        = r'/pypelyne/PyPELyNE_projects'
libraryRootServer          = r'/pypelyne/PyPELyNE_assets'
projectsRootServerDarwin  = r'/Volumes/pypelyne/PyPELyNE_projects'
assetsRootServerDarwin    = r'/Volumes/pypelyne/PyPELyNE_library'
projectsRootServerWin     = r''
assetsRootServerWin       = r''
projectsRootServerLinux   = r'/mnt/pypelyne/PyPELyNE_projects'
assetsRootServerLinux     = r'/mnt/pypelyne/PyPELyNE_assets'


###Darwin
fileExplorerDarwin        = r'/usr/bin/open'
projectsRootDarwin        = r'/Volumes/pili/pypelyne_projects'
projectsRootDarwinAlt     = r'/Users/michaelmussato/pypelyne_projects'
libraryRootDarwin          = r'/Volumes/pili/pypelyne_library'
audioFolderDarwin         = r'/Volumes/pili/library/audio'
screenCastExecDarwin      = r'payload/vlc/darwin/VLC'
sequenceExecDarwin        = r'payload/djv/darwin/djv-1.1.0-OSX-64'
sequenceExecRvDarwin      = r'/Applications/RV64.app/Contents/MacOS/RV'
tarExecDarwin             = r'payload/tar/darwin/tar'

###Windows
fileExplorerWin           = r'explorer.exe'
projectsRootWin           = r'C:\pypelyne_projects'
libraryRootWin             = r''
audioFolderWin            = r'C:\audio'
screenCastExecWin         = r'payload\vlc\win64\vlc.exe'
sequenceExecWin           = r''
sequenceExecRvWin         = r''
tarExecWin                = r''

###Linux
fileExplorerLinuxGnome    = r'/usr/bin/nautilus'
fileExplorerLinuxKDE      = r'/usr/bin/dolphin'
projectsRootLinux         = r''
libraryRootLinux           = r''
audioFolderLinux          = r''
screenCastExecLinux       = r''
sequenceExecLinux         = r''
sequenceExecRvLinux       = r''
tarExecLinux              = r''