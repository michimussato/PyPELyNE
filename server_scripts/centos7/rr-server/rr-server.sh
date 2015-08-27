#!/bin/sh
# chkconfig: 123456 90 10
# TTS Server for Speech Synthesis
# https://wolfpaulus.com/journal/software/pythonlauncher/
#
workdir='/pypelyne/royalrender_repository/'
 
start() {
    if [ -z ${RR_ROOT} ]; 
        then {
        export RR_ROOT="/pypelyne/royalrender_repository"
        echo 'RR_ROOT successfully exported'
        }
    fi
    cd $workdir
    ${workdir}/bin/lx64/rrServerconsole >> /pypelyne/log/rr-server.log 2>&1 &
    echo "Server started."
}
 
stop() {
    pid=`ps -ef | grep 'rrServerconsole' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 10
    echo "Server killed."
}
 
case "$1" in
  start)
    start
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: /etc/init.d/rr-server {start|stop|restart}"
    exit 1
esac
exit 0