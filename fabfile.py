### -*- coding: utf-8 -*- ##
""" based on 
inspired by http://morethanseven.net/2009/07/27/fabric-django-git-apache-mod_wsgi-virtualenv-and-p/
"""

from fabric.api import env, run, sudo, require, put, local

def production():
    env.hosts = ['yotweets.com']
    env.user = 'root'
    env.postgres_user = 'saaskit'
    env.postgres_password = 'saaskitS3n89mkk'
    env.postgres_db = 'saaskit'

def install_packages():
    """Install system wide packages"""
    require('hosts', provided_by=[production])
    put('./deploy/linode/apt/sources.list', '/etc/apt/sources.list.d/sources.list')
    sudo('apt-get -y update', pty=True)
    sudo('apt-get -y install wget nmap unzip wget csstidy build-essential ant git-core gcc curl python-dev python-egenix-mxdatetime libc6-dev postgresql-8.3 postgresql-client-8.3 nginx apache2 apache2.2-common apache2-mpm-worker apache2-threaded-dev libapache2-mod-wsgi libapache2-mod-rpaf memcached postfix libmemcache-dev tar mc', pty=True)
    
    #locale
    sudo('dpkg-reconfigure locales; apt-get install language-pack-en; locale-gen en_US.UTF-8;')
    
    #Install cmemcache from tarball
    sudo('cd /usr/local/src/; wget http://gijsbert.org/downloads/cmemcache/cmemcache-0.95.tar.bz2; tar xjvf cmemcache-0.95.tar.bz2;', pty=True)
    sudo('cd /usr/local/src/cmemcache-0.95/; python setup.py install; python test.py; rm /usr/local/src/cmemcache-0.95.tar.bz2;', pty=True)

def log_setup():
    """setup log"""
    require('hosts', provided_by=[production])
    sudo('mkdir -p /var/log/webapp; mkdir -p /var/log/webapp/main;', pty=True)
    sudo('mkdir -p /var/log/webapp/assets; mkdir -p /var/log/webapp/user_sites;', pty=True)

def github_config():
    """setup user config for github. global and ssh public keys """
    require('hosts', provided_by=[install_packages, production])
    
    #Github user's settings
    run('git config --global github.user deploy-admin', pty=True)
    run('git config --global github.email deploy@crowdsense.com', pty=True)
    run('git config --global github.token 445c8da5521cd969ec42a3de85f323d7', pty=True)
    
    #ssh public keys
    run('mkdir -p ~/.ssh', pty=True)
    put('./deploy/linode/.ssh/id_rsa', '~/.ssh/id_rsa')
    put('./deploy/linode/.ssh/id_rsa.pub', '~/.ssh/id_rsa.pub')
    #run('ssh git@github.com', pty=True)

def webapp_setup():
    """webapp folder and user """
    require('hosts', provided_by=[production])
    sudo('echo "/dev/xvdc /webapp ext3   noatime  0 0" >> /etc/fstab', pty=True)
    sudo('mkdir -p /webapp', pty=True)
    sudo('mount /webapp', pty=True)
    sudo('useradd webapp', pty=True) 
    sudo('usermod -d /webapp webapp; usermod -a -G www-data webapp;', pty=True) 
    sudo('chsh webapp -s /bin/bash', pty=True)

def install_project():
    """get source from repository and build it"""
    require('hosts', provided_by=[github_config, install_packages, production])
    #TODO: parametrize domain
    sudo('cd /webapp; rm -r %(name)s; git clone git@github.com:CrowdSense/saaskit-core.git %(name)s;' \
         % {'name': env.host_string}, pty=True)
    
    #create local settings
    sudo('echo "DATABASE_ENGINE = \'postgresql_psycopg2\'" > /webapp/%s/src/saaskit/local_settings.py' % env.host_string, pty=True)
    sudo('echo "DATABASE_NAME = \'%s\'" >> /webapp/%s/src/saaskit/local_settings.py' % (env.postgres_db, env.host_string), pty=True)
    sudo('echo "DATABASE_USER = \'%s\'" >> /webapp/%s/src/saaskit/local_settings.py' % (env.postgres_user, env.host_string), pty=True)
    sudo('echo "DATABASE_PASSWORD = \'%s\'" >> /webapp/%s/src/saaskit/local_settings.py' % (env.postgres_password, env.host_string), pty=True)
    sudo('echo "DATABASE_HOST = \'\'" >> /webapp/%s/src/saaskit/local_settings.py' % env.host_string, pty=True)
    sudo('echo "DATABASE_PORT = \'5432\'" >> /webapp/%s/src/saaskit/local_settings.py' % env.host_string, pty=True)

    sudo('cd /webapp/%s; python ./bootstrap.py -c ./production.cfg; ./bin/buildout -c ./production.cfg' % env.host_string, pty=True)
    sudo('chown -R webapp:www-data /webapp', pty=True)

def nginx_config():
    """setup nginx"""
    require('hosts', provided_by=[install_packages, production])
    sudo('/etc/init.d/nginx stop', pty=True)

    #cp -u ./nginx/assets /etc/nginx/sites-available/assets
    #ln -s /etc/nginx/sites-available/assets /etc/nginx/sites-enabled/assets
    #TODO: parametrize server_name
    put('./deploy/linode/nginx/webapp', '/etc/nginx/sites-available/webapp')
    sudo('ln -f -s /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/webapp', pty=True)
    put('./deploy/linode/nginx/nginx.conf', '/etc/nginx/nginx.conf')
    put('./deploy/linode/nginx/proxy.conf', '/etc/nginx/proxy.conf')
    
    sudo('/etc/init.d/nginx start', pty=True)

def apache2_config():
    require('hosts', provided_by=[install_packages, production])
    sudo('apache2ctl stop', pty=True)
    
    put('./deploy/linode/apache/main', '/etc/apache2/sites-available/main')
    put('./deploy/linode/apache/sites', '/etc/apache2/sites-available/sites')
    sudo('a2ensite main; a2ensite sites;', pty=True)
    put('./deploy/linode/apache/apache2.conf', '/etc/apache2/apache2.conf')
    put('./deploy/linode/apache/ports.conf', '/etc/apache2/ports.conf')
    put('./deploy/linode/apache/security', '/etc/apache2/conf.d/security')
    
    #sudo('a2enmod rewrite')
    sudo('/etc/init.d/apache2 start', pty=True)

def database_mount():
    require('hosts', provided_by=[production])
    sudo('echo "/dev/xvdd /database ext3   noatime  0 0" >> /etc/fstab', pty=True)
    sudo('mkdir -p /database; mount /database;', pty=True)

def postgresql_config():
    require('hosts', provided_by=[install_packages, production])
    
    sudo('/etc/init.d/postgresql-8.3 stop', pty=True)
    
    put('./deploy/linode/db/initial_db.tar', '/database')
    sudo('cd /database; tar xvf initial_db.tar; ', pty=True)
    sudo('chown -R postgres:postgres /database/postgresql', pty=True)
    sudo('rm -rf /database/initial_db.tar', pty=True)
    
    put('./deploy/linode/db/postgresql.conf', '/etc/postgresql/8.3/main/postgresql.conf')
    put('./deploy/linode/db/pg_hba.conf', '/etc/postgresql/8.3/main/pg_hba.conf')
    
    sudo('/etc/init.d/postgresql-8.3 start', pty=True)

def pg_user_db_setup():
    require('hosts', provided_by=[install_packages, production])
    run('sudo -u postgres createuser -S -D -R %s' % env.postgres_user, pty=True)
    run('sudo -u postgres psql -c "alter user %s with password \'%s\';"' \
        % (env.postgres_user, env.postgres_password), pty=True)
    run('sudo -u postgres createdb --owner=%s %s' % (env.postgres_user, env.postgres_db), pty=True)

def postgresql_setup():
    require('hosts', provided_by=[install_packages, production])
    database_mount()
    postgresql_config()
    pg_user_db_setup()

def install_development_tarball():
    "Compress development packages, put them to server, extract."
    require('hosts', provided_by=[production])
    require('path')
    
    #local('cd ../../; tar cf - "src" | gzip -f9 > "src.tar.gz"')
    #put("../../src.tar.gz", '%s/' % env.path)
    #run('cd %s; tar zxf src.tar.gz;' % env.path)
    #local('rm -f ../../src.tar.gz')

def restart_webserver():
    "Restart the web server"
    sudo('/etc/init.d/apache2 restart', pty=True)
    