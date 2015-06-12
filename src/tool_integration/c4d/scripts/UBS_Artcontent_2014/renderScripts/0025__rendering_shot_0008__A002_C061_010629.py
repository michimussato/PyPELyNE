import os
import subprocess
import datetime
#import platform

start = 352
end = 452

increments = [ '0110', '0111' ]


executable = '\"C:\\Program Files\\MAXON\\CINEMA 4D R14\\CINEMA 4D 64 Bit.exe\"'


subprocess.call( "cls", shell=True )
#subprocess.call( "cls" if platform.system() == "Windows" else "clear", shell=True )
startTimeJob = datetime.datetime.now().replace( microsecond=0 )

for increment in increments:
    scene = '\"\\\smsrv-001\\Allgemein\\Kunden\\UBS\\UBS_Artcontent_2014\\tasks\\0025__rendering\\shot_0008__A002_C061_010629\\project\\0025__rendering_shot_0008__A002_C061_010629_%s.c4d\"' %increment
    
    print 'working on %s' %scene

    for frame in range( start, end + 1 ):

        startTimeFrame = datetime.datetime.now().replace( microsecond=0 )
        
        print '\nworking hard on frame %s of %s...' %( str( frame ), str( end ) )
        
        cmd = [ executable, '-nogui', '-render', scene, '-frame', str( frame ), str( frame ) ]
        
        job = subprocess.call( ' '.join( cmd ) )
        
        if job == 0:
            endTimeFrame = datetime.datetime.now().replace( microsecond=0 )
            durationFrame = endTimeFrame - startTimeFrame
            durationJob = endTimeFrame - startTimeJob
            
            print 'DONE. took me %s. in total %s so far.' %( durationFrame, durationJob )
            success = True
        else:
            print 'failed at frame %s' %str( frame )
            success = False
            break
    

endTimeJob = datetime.datetime.now().replace( microsecond=0 )
durationJob = endTimeJob - startTimeJob
    
if success == True:
    print 'master, i succeeded. took me %s' %durationJob
elif success == False:
    print 'gave up after %s. it was not my fault, i swear...' %durationJob