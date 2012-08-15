#! /bin/sh

DIR=/path/to
USER=__user__
GROUP=__group__

PIDFILE=$DIR/var/run/production.pid
LOGFILE=$DIR/var/log/console.log
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

do_run()
{
    cd $DIR && . bin/activate && paster serve --pid-file=$PIDFILE --log-file=$LOGFILE --user=$USER --group=$GROUP etc/production.ini
}

case "$1" in
  run)
    do_run
    ;;
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
    echo "Usage: $0 {run|start|stop|status|restart}" >&2
    exit 3
    ;;
esac

exit 0
