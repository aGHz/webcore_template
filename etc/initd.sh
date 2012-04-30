#! /bin/sh

# Copy this file to the app's bin/ directory, change $DIR and symlink it from /etc/init.d/<name>
# Run `update-rc.d <name> defaults` to install in /etc/rc*.d/
# Run `update-rc.d -f <name> remove` to uninstall from /etc/rc*.d/ but keep the init.d script

# Point this to the root of the hshapi install (containing all the bin/, src/, etc/ folders)
DIR=/path/to
USER=user
GROUP=group

PIDFILE=$DIR/var/run/production.pid
LOGFILE=$DIR/var/log/paster-production.log
PROJECT=`basename $DIR`

do_start()
{
    cd $DIR && . bin/activate && paster serve --pid-file=$PIDFILE --log-file=$LOGFILE --user=$USER --group=$GROUP etc/production.ini start
}

do_stop()
{
    cd $DIR && . bin/activate && paster serve --pid-file=$PIDFILE --log-file=$LOGFILE --user=$USER --group=$GROUP etc/production.ini stop
}

do_restart()
{
    cd $DIR && . bin/activate && paster serve --pid-file=$PIDFILE --log-file=$LOGFILE --user=$USER --group=$GROUP etc/production.ini restart
}

do_status()
{
    cd $DIR && . bin/activate && paster serve --pid-file=$PIDFILE --log-file=$LOGFILE --user=$USER --group=$GROUP --daemon etc/production.ini status
}

case "$1" in
  start)
    echo "Starting $PROJECT"
    do_start
    ;;
  stop)
    echo "Stopping $PROJECT"
    do_stop
    ;;
  status)
    do_status
    ;;
  restart)
    echo "Restarting $PROJECT"
    do_restart
    ;;
  *)
    echo "Usage: $0 {start|stop|status|restart}" >&2
    exit 3
    ;;
esac

exit 0
