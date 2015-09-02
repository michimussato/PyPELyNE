#!/bin/python

#v103_server

__author__ = 'michaelmussato'



from conf.valuePyPELyNE import *

import os
import sys
import socket
import threading
from logging import *
import signal
import json
import src.getLocalIp as getLocalIp

from conf.valuePyPELyNE import *


class server():
    def __init__( self, host = '', debugLevel = INFO ):

        basicConfig( level = debugLevel )

        self.host = host
        self.port = serverPort
        self.sockets = []
        self.threads = []

        #how many ports should be checked if given port fails?
        self.portRange = int( serverPortRange )


        self.projectsRoot = projectsRootServer
        self.projectsRootDarwin = projectsRootServerDarwin
        self.projectsRootWin = projectsRootServerWin
        self.projectsRootLinux = projectsRootServerLinux
        self.tarSep = archiveSeparator

        self.pypelyneRoot = os.getcwd()

        self.sockets = []

        self.launch()
        
    def sendList( self, sock, path, addr, data = None ):
        try:
            serialized = json.dumps( [ path, addr, data ] )
            # send the length of the serialized data first
            sock.send( '%d\n' %( len( serialized ) ) )
            # send the serialized data
            sock.sendall( serialized )
            info( ' server %s:%s | JSON serialized data successfully sent to %s:%s' %( self.host, self.port, addr[ 0 ], addr[ 1 ] ) )
        except:
            try:
                #raise Exception( 'You can only send JSON-serializable data' )
                # send the length of the serialized data first
                #sock.send( '%d\n' %( len( serialized ) ) )
                # send the serialized data
                sock.sendall( data )
                info( ' server:%s | non serialized data successfully sent %s:%s' %( self.port, addr[ 0 ], addr[ 1 ] ) )
            except ( TypeError, ValueError ), e:
                warning( ' server:%s | data could not be sent to %s:%s. don\'t know how to handle yet.' %( self.port, addr[ 0 ], addr[ 1 ] ) )
                #return 0
                #raise Exception( 'sending data not possible' )
    
    def listContent( self, path, sock, addr ):
        self.sockets.append( sock )
        # syntax: ( socket, isPath, pathExists, content, receiver )
        info( ' server %s:%s | connection to %s:%s established' %( self.host, self.port, addr[ 0 ], addr[ 1 ] ) )
        #while True:
        while sock:

            response = sock.recv( 1024 )

            if response == 'getProjectsRootServerDarwin':
                info( 'client %s:%s requested projectsRootServerDarwin, which is %s' %( addr[ 0 ], addr[ 1 ], self.projectsRootDarwin ) )
                #data = os.listdir( self.projectsRootDarwin )
                self.sendList( sock, self.projectsRootDarwin, addr )

            elif response == 'getProjectsRootServerLinux':
                info( 'client %s:%s requested projectsRootServerLinux, which is %s' %( addr[ 0 ], addr[ 1 ], self.projectsRootLinux ) )
                self.sendList( sock, self.projectsRootDarwin, addr )

            elif response == 'getProjectsRootServerWin':
                info( 'client %s:%s requested projectsRootServerWin, which is %s' %( addr[ 0 ], addr[ 1 ], self.projectsRootWin ) )
                self.sendList( sock, self.projectsRootWin, addr )

            elif response == 'addProjectsServer':
                projects = os.listdir( self.projectsRoot )
                self.sendList( sock, self.projectsRoot, addr, projects )
                info( 'client %s:%s requested projects list, which is %s' %( addr[ 0 ], addr[ 1 ], projects ) )

            elif response == 'bye':
                #self.sendSerialized( socket, response )
                info( 'client %s:%s sent bye bye' %( addr[ 0 ], addr[ 1 ] ) )
                #self.sendList( sock, 'bye', None )
                self.sockets.remove( sock )
                sock.close()
                info( '%s connections left open' %( len( self.sockets ) ) )
                break


            elif os.path.exists( response ):

                info( 'valid path received: %s' %( response ) )
                #sock.send( 'path %s exists' %( path ) )

                content = os.listdir( path )

                #for directory in content:
                self.sendList( sock, response )

            else:
                warning( 'invalid path received: %s' %( response ) )
                #sock.send( 'path %s does not exist' %( path ) )
                self.sendList( sock, 'path %s does not exist' %( response ) )



            #info( 'connection closed by server' )
            #sock.close()




    def launch( self ):

        info( 'server starting' )
        info( 'server ip is %s' %( self.host ) )
        counter = 1

        while True:
            try:
                info( 'trying port %s' %( self.port ) )

                sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
                #s.setsockopt( socket.SOCK_STREAM, socket.SO_REUSEADDR, 1 )
                #s.setsockopt( socket.SO_REUSEADDR, 1 )
                sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
                #s.setblocking( 0 )
                sock.bind( ( self.host, self.port ) )
            
                #connections = []

                sock.listen( 5 )
                info( 'port succeeded' )
                break

            except socket.error:
                info( 'port failed' )

                if counter < self.portRange:
                
                    #warning( 'port %s in use' %( self.port ) )
                    counter += 1
                    self.port += 1
                else:
                    warning( 'tried %s port(s) without success. server failed to start.' %( counter ) )
                    sys.exit()


        info( 'server listening at %s:%s' %( self.host, self.port ) )

        while True:
            try:
                conn, addr = sock.accept()
                #info( 'client connection from %s' %( str( addr ) ) )
                thread = threading.Thread( target = self.listContent, args = ( 'RetrThread', conn, addr ) )
                thread.start()
                #self.threads.append( t )
            
            except KeyboardInterrupt:
                print len( self.sockets )
                #for i in self.connections:
                #    i.close()
                #for i in self.threads:
                #    i.stop()
                sys.exit()
        #s.close()
        #info( 'connection closed by server' )


if __name__ == '__main__':

    try:
        ip = getLocalIp.getIp()
    except:
        ip = '127.0.0.1'
    #server = server( host = ip, debugLevel = INFO )
    server = server( host = ip, debugLevel = INFO )




