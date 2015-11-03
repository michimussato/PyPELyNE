#!/bin/sh
# chkconfig: 123456 90 10
# TTS Server for Speech Synthesis
# https://wolfpaulus.com/journal/software/pythonlauncher/
#
pypelyne_root=/pypelyne/PyPELyNE
logDir=${pypelyne_root}/logs


# Wait for Network to be available.
# https://smartcoding.wordpress.com/2010/11/14/linux-shell-scripting-wait-for-network-to-be-available/
while true
do
    ping -c 1 8.8.8.8
    if [[ $? == 0 ]];
    then
        echo 'Network available.'
        break;
    else
        echo 'Network is not available, waiting..'
        sleep 5
    fi
done
#echo 'If you see this message, then Network was successfully loaded.'


 
start() {
    #cd $workdir
    if [ ! -d ${logDir} ]; then
        mkdir ${logDir}
        chown nobody:nobody ${logDir}
        chmod 777 ${logDir}
        echo 'logDir created'
    fi


    /usr/bin/python ${pypelyne_root}/pypelyne_server.py >> ${logDir}/pypelyne_server.log 2>&1 &
    echo "Server started."
}
 
stop() {
    pid=$(ps -ef | grep "[p]ython ${pypelyne_root}/pypelyne_server.py" | awk '{ print $2 }')
    #pid=`ps -ef | grep '[p]ython ${pypelyne_root}/pypelyne_server.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
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
    echo "Usage: /etc/init.d/pypelyne_server {start|stop|restart}"
    exit 1
esac
exit 0