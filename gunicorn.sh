#!/bin/bash

NAME="bbb"                              #Name of the application (*)
DJANGODIR=~/Documents/Projetos/globo-com/code_challenge_globocom/            # Django project directory (*)
SOCKFILE=~/Documents/Projetos/globo-com/code_challenge_globocom/run/gunicorn.sock        # we will communicate using this unix socket (*)
USER=carlossa                                        # the user to run as (*)
GROUP=www-data                                     # the group to run as (*)
NUM_WORKERS=2                                     # how many worker processes should Gunicorn spawn (*)
DJANGO_SETTINGS_MODULE=bbb.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=bbb.wsgi                     # WSGI module name (*)

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ~/.virtualenvs/bbb/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
# exec /var/www/smopqd/smopqd-env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
