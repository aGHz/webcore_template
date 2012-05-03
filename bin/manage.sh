#!/bin/sh

# Point this to the root of the hshapi install (containing all the bin/, src/, etc/ folders)
DIR=/path/to
CMD=$1
DATE=`date +"%Y-%m-%d.%H-%M"`

cd $DIR && . bin/activate && paster manage -v -c etc/manage.ini $CMD > var/log/manage/$CMD.$DATE.log 2>&1 && deactivate
