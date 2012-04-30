#!/bin/sh

DIR=/path/to
CMD=$1
DATE=`date +"%Y-%m-%d.%H-%M"`

cd $DIR && . bin/activate && paster manage -v -c etc/management.ini $CMD > var/log/manage/$CMD.$DATE.log 2>&1 && deactivate
