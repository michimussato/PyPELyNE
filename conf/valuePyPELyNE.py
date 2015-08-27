###Global
#files matching items in exclusions get removed!
exclusions                = [ '.DS_Store', 'Thumbs.db', '.com.apple.timemachine.supported', 'desktop.ini' ]
imageExtensions           = [ '.jpg', '.exr', '.tga', '.png', '.tiff', '.tif' ]
movieExtensions           = [ '.mov', '.avi' ]
archiveSeparator          = '_____'

###Server
projectsRootServer        = r'/pypelyne/PyPELyNE_projects'
projectsRootServerDarwin  = r'/Volumes/pypelyne/PyPELyNE_projects'
projectsRootServerWin     = r''
projectsRootServerLinux   = r'/mnt/pypelyne/PyPELyNE_projects'
assetsRootServer          = r'/pypelyne/PyPELyNE_assets'
assetsRootServerDarwin    = r'/Volumes/pypelyne/PyPELyNE_assets'
assetsRootServerWin       = r''
assetsRootServerLinux     = r'/mnt/pypelyne/PyPELyNE_assets'


###Darwin
fileExplorerDarwin        = r'/usr/bin/open'
projectsRootDarwin        = r'/Volumes/pili/pypelyne_projects'
assetsRootDarwin          = r''
audioFolderDarwin         = r'/Volumes/pili/library/audio'
screenCastExecDarwin      = r'payload/vlc/darwin/VLC'
sequenceExecDarwin        = r'payload/djv/darwin/djv-1.1.0-OSX-64'
sequenceExecRvDarwin      = r'/Applications/RV64.app/Contents/MacOS/RV'
tarExecDarwin             = r'payload/tar/darwin/tar'

###Windows
fileExplorerWin           = r'explorer.exe'
projectsRootWin           = r'C:\pypelyne_projects'
assetsRootWin             = r''
audioFolderWin            = r'C:\audio'
screenCastExecWin         = r'payload\vlc\win64\vlc.exe'
sequenceExecWin           = r''
sequenceExecRvWin         = r''
tarExecWin                = r''

###Linux
fileExplorerLinuxGnome    = r'/usr/bin/nautilus'
fileExplorerLinuxKDE      = r'/usr/bin/dolphin'
projectsRootLinux         = r''
assetsRootLinux           = r''
audioFolderLinux          = r''
screenCastExecLinux       = r''
sequenceExecLinux         = r''
sequenceExecRvLinux       = r''
tarExecLinux              = r''