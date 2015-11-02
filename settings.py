###Global
#files matching items in exclusions get removed!
CONTENT_TABS              = [{'content': 'assets', 'abbreviation': 'AST', 'loader_color': '#FFFF00', 'saver_color': '#FFFF33'},
                             {'content': 'shots', 'abbreviation': 'SHT', 'loader_color': '#0000FF', 'saver_color': '#3333FF'},
                             {'content': 'sequences', 'abbreviation': 'SEQ', 'loader_color': '#00FFFF', 'saver_color': '#33FFFF'}]
EXCLUSIONS                = [ '.mayaSwatches', '.DS_Store', 'Thumbs.db', '.com.apple.timemachine.supported', 'desktop.ini' ]
AUDIO_EXTENSIONS          = [ '.mp3', '.m4a', '.mp4' ]
IMAGE_EXTENSIONS          = [ '.jpg', '.exr', '.tga', '.png', '.tiff', '.tif', '.bmp', '.gif' ]
MOVIE_EXTENSIONS          = [ '.mov', '.avi' ]
ARCHIVE_SEPARATOR         = '_____'
USE_SERVER                = False
USE_SCREEN_CAST           = True
DEFAULT_TASK_COLOR        = '#FF00FF'


###Server
SERVER_IP                 = r'192.168.0.22'
SERVER_PORT               = r'50001'
SERVER_PORT_RANGE         = r'5'
PROJECT_ROOT_SERVER       = r'/pypelyne/PyPELyNE_projects'
LIBRARY_ROOT_SERVER        = r'/pypelyne/PyPELyNE_assets'
PROJECTS_ROOT_SERVER_DARWIN  = r'/Volumes/pypelyne/PyPELyNE_projects'
ASSETS_ROOT_SERVER_DARWIN    = r'/Volumes/pypelyne/PyPELyNE_library'
PROJECTS_ROOT_SERVER_WIN     = r''
ASSETS_ROOT_SERVER_WIN      = r''
PROJECTS_ROOT_SERVER_LINUX  = r'/mnt/pypelyne/PyPELyNE_projects'
ASSETS_ROOT_SERVER_LINUX    = r'/mnt/pypelyne/PyPELyNE_assets'


###Darwin
FILE_EXPLORER_DARWIN       = r'/usr/bin/open'
PROJECTS_ROOT_DARWIN       = r'/Volumes/pili/pypelyne_projects'
PROJECTS_ROOT_DARWIN_ALT = r'/Users/michaelmussato/pypelyne_projects'
LIBRARY_ROOT_DARWIN         = r'/Volumes/pili/pypelyne_library'
AUDIO_FOLDER_DARWIN       = r'/Volumes/pili/library/audio'
SCREEN_CAST_EXEC_DARWIN    = r'payload/vlc/darwin/VLC'
SEQUENCE_EXEC_DARWIN      = r'payload/djv/darwin/djv-1.1.0-OSX-64'
SEQUENCE_EXEC_RV_DARWIN    = r'/Applications/RV64.app/Contents/MacOS/RV'
TAR_EXEC_DARWIN          = r'payload/tar/darwin/tar'

###Windows
FILE_EXPLORER_WIN          = r'explorer.exe'
PROJECTS_ROOT_WIN         = r'C:\pypelyne_projects'
LIBRARY_ROOT_WIN           = r''
AUDIO_FOLDER_WIN          = r'C:\audio'
SCREEN_CAST_EXEC_WIN        = r'payload\vlc\win64\vlc.exe'
SEQUENCE_EXEC_WIN         = r''
SEQUENCE_EXEC_RV_WIN       = r''
TAR_EXEC_WIN             = r''

###Linux
FILE_EXPLORER_LINUX_GNOME  = r'/usr/bin/nautilus'
FILE_EXPLORER_LINUX_KDE    = r'/usr/bin/dolphin'
PROJECTS_ROOT_LINUX       = r''
LIBRARY_ROOT_LINUX        = r''
AUDIO_FOLDER_LINUX        = r''
SCREEN_CAST_EXEC_LINUX     = r''
SEQUENCE_EXEC_LINUX       = r''
SEQUENCE_EXEC_RV_LINUX     = r''
TAR_EXEC_LINUX           = r''