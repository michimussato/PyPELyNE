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
import getLocalIp


class server():
    def __init__( self, host = '', port = 50001, debugLevel = INFO ):

        basicConfig( level = debugLevel )

        self.host = host
        self.port = port
        self.sockets = []
        self.threads = []

        #how many ports should be checked if given port fails?
        self.portRange = 2


        self.projectsRoot = projectsRootServer
        self.projectsRootDarwin = projectsRootServerDarwin
        self.projectsRootWin = projectsRootServerWin
        self.projectsRootLinux = projectsRootServerLinux
        self.tarSep = archiveSeparator

        self.pypelyneRoot = os.getcwd()



        self.launch()
        
    def sendList( self, sock, path, isPath, pathExists, data, addr ):
        try:
            serialized = json.dumps( [ path, isPath, pathExists, data ] )
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

        response = socket.recv( 1024 )

        if response == 'getProjectsRootServerDarwin':
            logging.info( 'client %s:%s requested projectsRootServerDarwin, which is %s' %( addr[ 0 ], add[ 1 ], self.projectsRootDarwin ) )
            self.sendSerialized( socket, self.projectsRootDarwin )

        elif response == 'getProjectsRootServerLinux':
            logging.info( 'client %s:%s requested projectsRootServerLinux, which is %s' %( addr[ 0 ], add[ 1 ], self.projectsRootLinux ) )
            self.sendSerialized( socket, self.projectsRootDarwin )

        elif response == 'getProjectsRootServerWin':
            logging.info( 'client %s:%s requested projectsRootServerWin, which is %s' %( addr[ 0 ], add[ 1 ], self.projectsRootWin ) )
            self.sendSerialized( socket, self.projectsRootWin )

        elif response == 'bye':
            #self.sendSerialized( socket, response )
            logging.info( 'client %s:%s gone' %( addr[ 0 ], add[ 1 ] ) )


        elif os.path.exists( response ):

            logging.info( 'valid path received: %s' %( response ) )
            #sock.send( 'path %s exists' %( path ) )

            content = os.listdir( path )

            #for directory in content:
            self.sendSerialized( socket, response )

        else:
            logging.warning( 'invalid path received: %s' %( response ) )
            #sock.send( 'path %s does not exist' %( path ) )
            self.sendSerialized( socket, 'path %s does not exist' %( response ) )



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
    #server = server( host = ip, port = 50505, debugLevel = INFO )
    server = server( host = ip, debugLevel = INFO )




