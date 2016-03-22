#!/usr/bin/python
# coding: utf-8
from datetime import datetime
from fabric.api import *
# from fabric.context_managers import settings as _settings
from os import environ
from os.path import join as __pathjoin, expanduser
import sys
import platform as _platform

sys.path.append('.')


def get_os():
    if _platform == "linux" or _platform == "linux2":
        return 'linux'
    elif _platform == "darwin":
        return 'mac'

env.os = get_os()

"""
Base configuration
"""


def config_envs():
    if env.os == "linux":
        # Linux
        env.path = '%(home)s/sites/%(project_name)s' % env
        env.log_path = '%(home)s/sites/%(project_name)s/logs/' % env
        env.nginx_config_path = '/etc/nginx/conf.d/'
    elif env.os == "darwin":
        # MAC OS X
        env.path = '%(home)s/sites/%(project_name)s' % env
        env.log_path = '%(home)s/newsapps/logs/%(project_name)s' % env
        env.nginx_config_path = '/usr/local/etc/conf.d/'

    env.home = expanduser("~")
    env.project_name = 'bbb'
    env.database_password = 'qw34rt'
    env.env_path = '%(path)s/env' % env
    env.repo_path = '%(path)s/repository' % env
    env.git_repo = 'git@github.com:bailian/code_challenge_globocom.git'
    env.user_dir = 'www-data'
    env.database_username = env.project_name
    env.python = 'python2.7.5'

"""
Environments
"""


def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.hosts = ['$(production_domain)']
    env.user = '$(production_user)'
    env.passwd_admin_mysql = 'qw34rt'
    env.database_host = 'localhost'

def staging():
    """
    Work on stagin environment
    """
    env.settings = 'staging'
    env.hosts = ['$(staging_domain)']
    env.user = '$(staging_user)'
    env.passwd_admin_mysql = 'qw34rt'
    env.database_host = 'localhost'

def local():
    """
    Work on local environment
    """
    env.settings = 'local'
    env.hosts = ['$(local_domain)']
    env.user = '$(local_user)'
    env.passwd_admin_mysql = 'qw34rt'
    env.database_host = 'localhost'




"""
Branches
"""


def stable():
    """
    Work on stable branch.
    """
    env.branch = 'stable'


def master():
    """
    Work on development branch.
    """
    env.branch = 'master'


def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name


def setup():
    config_envs()
    require('settings', provided_by=[production, staging, local])
    require('branch', provided_by=[stable, master, branch])
    setup_directories()
    setup_virtualenv()
    clone_repo()
    checkout_latest()
    install_requirements()
    install_nginx_conf()


def setup_directories():
    """
    Create directories necessary for deployment.
    """
    run('mkdir -p %(path)s' % env)
    run('mkdir -p %(env_path)s' % env)
    run('mkdir -p %(log_path)s;' % env)
    sudo(
        'chgrp -R %(user_dir)s %(log_path)s; chmod -R g+w %(log_path)s;' % env
    )
    run('ln -s %(log_path)s %(path)s/logs' % env)


def setup_virtualenv():
    """
    Setup a fresh virtualenv.
    """
    run('virtualenv -p %(python)s --no-site-packages %(env_path)s;' % env)
    run('source %(env_path)s/bin/activate; easy_install -U setuptools; '
        'easy_install pip;' % env)


def clone_repo():
    """
    Do initial clone of the git repository.
    """
    run('git clone %(git_repo)s %(repo_path)s' % env)


def checkout_latest():
    """
    Pull the latest code on the specified branch.
    """
    run('cd %(repo_path)s; git checkout %(branch)s; '
        'git pull origin %(branch)s' % env)


def install_requirements():
    """
    Install the required packages using pip.
    """
    run('source %(env_path)s/bin/activate; pip install -E %(env_path)s -r '
        '%(repo_path)s/requirements.txt' % env)


def install_nginx_conf():
    """
    Install the nginx site config file.
    """
    sudo('cp %(repo_path)s/%(project_name)s/nginx-bbb.conf '
         '%(nginx_config_path)s' % env)


"""
Commands - deployment
"""


def deploy():
    """
    Deploy the latest version of the site to the server and restart Nginx.

    Does not perform the functions of load_new_data().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])

    with settings(warn_only=True):
        maintenance_up()

    checkout_latest()
    gzip_assets()
    deploy_to_s3()
    refresh_widgets()



def maintenance_up():
    """
    Install the Nginx maintenance configuration.
    """
    sudo('ln -s %(apache_config_path)s/sites-available/maintenance.conf '
         '%(apache_config_path)s/sites-enabled/maintenance.conf')
    sudo('rm -f /etc/nginx/sites-enabled/nginx-bbb.conf')
    reboot()


def reboot():
    """
    Restart the Nginx server.
    """
    if env.os == 'linux':
        sudo('service nginx stop')
        sudo('service nginx start')
    elif env.os == 'mac':
        sudo('nginx')

    run("kill -9 `ps aux | grep gunicorn |grep %(project_name)s | awk "
        "'{ print $2 }'`" % env)
    put('%(env_path)s/gunicorn.sh', mode=0755)
    sudo('./%(env_path)s/gunicorn.sh')



def maintenance_down():
    """
    Reinstall the normal site configuration.
    """
    install_nginx_conf()
    reboot()


"""
Commands - rollback
"""


def rollback(commit_id):
    """
    Rolls back to specified git commit hash or tag.

    There is NO guarantee we have committed a valid dataset for an arbitrary
    commit hash.
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])

    maintenance_up()
    checkout_latest()
    git_reset(commit_id)
    maintenance_down()


def git_reset(commit_id):
    """
    Reset the git repository to an arbitrary commit hash or tag.
    """
    env.commit_id = commit_id
    run("cd %(repo_path)s; git reset --hard %(commit_id)s" % env)


"""
Commands - data
"""


def load_new_data():
    """
    Erase the current database and load new data from the SQL dump file.
    """
    require('settings', provided_by=[production, staging])

    maintenance_up()
    mysql_down()
    destroy_database()
    create_database()
    load_data()
    mysql_up()
    maintenance_down()


def create_database():
    """
    Creates the user and database for this project.
    """
    run('echo "CREATE USER \'%(database_username)s\'@\'%(database_host)s\' '
        'IDENTIFIED BY \'%(database_password)s\';" |  mysql -u root '
        '--password=%(passwd_admin_mysql)s' % env)
    run('echo "CREATE DATABASE %(project_name)s" CHARACTER SET utf8; |  '
        'mysql -u root --password=%(passwd_admin_mysql)s' % env)
    run('echo "GRANT ALL PRIVILEGES ON %(database_name)s.* TO '
        '\'%(database_username)s\'@\'%(database_host)s\' WITH GRANT OPTION;" '
        '|  mysql -u root --password=%(passwd_admin_mysql)s'
        % env)


def destroy_database():
    """
    Destroys the user and database for this project.

    Will not cause the fab to fail if they do not exist.
    """
    with settings(warn_only=True):
        run('echo "DROP DATABASE %(project_name)s;" |  mysql -u root '
            '--password=%(passwd_admin_mysql)s' % env)
        run('echo "DROP USER \'%(database_username)s\'@\'%(database_host)s\';"'
            ' |  mysql -u root --password=%(passwd_admin_mysql)s' % env)


def load_data():
    """
    Loads data from the repository into database.
    """
    run('mysql -u %(database_username)s --password=%(passwd_admin_mysql)s '
        '%(project_name)s < %(path)s/repository/data/mysql/dump.sql' % env)


def mysql_down():
    """
    Stop mysql so that it won't prevent the database from being rebuilt.
    """
    sudo('/etc/init.d/mysql stop')


def mysql_up():
    """
    Start mysql.
    """
    sudo('/etc/init.d/mysql start')
