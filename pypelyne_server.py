#!/bin/python


__author__ = 'michaelmussato'



from conf.valuePyPELyNE import *

import os
import sys
import socket
import threading
import logging
import json



class pypelyneServer():
    def __init__( self, host = '', port = 50001 ):
        #super( pypelyneServer, self ).__init__( parent )

        logging.basicConfig( level = logging.INFO )

        self.projectsRoot = projectsRootServer
        self.projectsRootDarwin = projectsRootServerDarwin
        self.projectsRootWin = projectsRootServerWin
        self.projectsRootLinux = projectsRootServerLinux
        self.tarSep = archiveSeparator

        self.pypelyneRoot = os.getcwd()

        self.running = False
        #self.kill = False

        self.host = host
        self.port = port
        #portAlive = 50000

        #sAlive = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        #sAlive.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        #sAlive.bind( ( host, portAlive ) )
        #sAlive.listen( 5 )




    def start( self ):
        self.socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.socket.bind( ( self.host, self.port ) )

        self.socket.listen( 5 )

        self.running = True

        logging.info( 'server started' )
        #os.system( '/bin/wall PyPELyNE_Server started' )
        self.c, self.addr = self.socket.accept()


        #while self.running == True:
        while True:

            #cAlive, addrAlive = sAlive.accept()
            #logging.info( 'alive connection to client %s' %( str( addrAlive ) ) )
            #tAlive = threading.Thread( target = alive, args = ( 'RetrThread', cAlive ) )
            #tAlive.start()

            #self.c, self.addr = self.socket.accept()
            logging.info( 'serving client %s' %( str( self.addr ) ) )
            self.thread = threading.Thread( target = self.listContent, args = ( 'RetrThread', self.c ) )
            self.thread.start()
    '''
    def stop( self, kill = '' ):

        self.socket.close()
        self.running = False
        logging.info( 'server stopped' )
        print kill
        if kill == 'kill':
            print 'do kill'
            sys.exit()
    '''




    def sendSerialized( self, socket, data ):
        try:
            serialized = json.dumps( data )
        except ( TypeError, ValueError ), e:
            raise Exception( 'You can only send JSON-serializable data' )
        # send the length of the serialized data first
        socket.send( '%d\n' % len( serialized ) )
        # send the serialized data
        socket.sendall( serialized )



    def listContent( self, path, socket ):
        #print sock
        response = socket.recv( 1024 )
        print response
        #if path == 'stop':
        #    #self.kill = True
        #    self.stop( 'kill' )
        #elif path == 'restart':
        #    #self.kill = False
        #    self.stop()
        #    self.start()
        if response == 'getProjectsRootServerDarwin':
            logging.info( 'client %s requested projectsRootServerDarwin, which is %s' %( str( self.addr ), self.projectsRootDarwin ) )
            self.sendSerialized( socket, self.projectsRootDarwin )

        elif response == 'getProjectsRootServerLinux':
            logging.info( 'client %s requested projectsRootServerLinux, which is %s' %( str( self.addr ), self.projectsRootLinux ) )
            self.sendSerialized( socket, self.projectsRootDarwin )

        elif response == 'getProjectsRootServerWin':
            logging.info( 'client %s requested projectsRootServerWin, which is %s' %( str( self.addr ), self.projectsRootWin ) )
            self.sendSerialized( socket, self.projectsRootWin )

        elif response == 'bye':
            #self.sendSerialized( socket, response )
            logging.info( 'client %s gone' %( str( self.addr ) ) )


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

        #logging.info( 'connection closed by server' )
        #sock.close()
    '''
    def alive( value, sock ):
        value = sock.recv( 1024 )

        if value == 'q':
            logging.info( 'closing connection' )
            sock.send( 'closing connection' )
            sock.close()
    '''





if __name__ == '__main__':
    pypelyneServer = pypelyneServer()
    pypelyneServer.start()