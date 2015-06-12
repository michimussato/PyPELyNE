import subprocess

from ctypes import windll,c_bool,c_uint
from os import getpid

GetPriorityClass    = windll.kernel32.GetPriorityClass
SetPriorityClass    = windll.kernel32.SetPriorityClass
OpenProcess         = windll.kernel32.OpenProcess
CloseHandle         = windll.kernel32.CloseHandle

job = subprocess.Popen( 'calc' )
print job.pid

windll.kernel32.SetPriorityClass( "IDLE_PRIORITY_CLASS", job.pid )