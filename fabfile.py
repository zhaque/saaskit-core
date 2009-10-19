### -*- coding: utf-8 -*- ##

#python 2.5 backward compatibility
from __future__ import with_statement
import os

from fabric.api import env, run, sudo, require, local, prompt, put as put_origin

TEMP_FILE = 'tempfile'

def parametrize_file(filename, params, tempfile):
    with open(filename) as f:
        data = f.read()
        for n, v in filter(lambda i: isinstance(i[1], (str, unicode)), env.items()):
            data = data.replace("$%s" % n, v)
        
        open(tempfile, 'w').write(data)
    
    return tempfile

def put(source, dest, mode=None):
    new_source = parametrize_file(source, env, TEMP_FILE)
    put_origin(new_source, dest, mode)
    os.remove(new_source)

def production():
    #env.hosts = ['yotweets.com']
    
    if not env.hosts:
        prompt("No hosts found. Please specify (single) host string for connection", 'host_string', 'yotweets.com')
    
    #env.user = 'root'
    prompt("SSH User", 'user', 'root')
    
    #env.postgres_user = 'saaskit'
    prompt("Postgresql username", 'POSTGRES_USER', 'saaskit')
    
    #env.postgres_password = 'saaskitS3n89mkk'
    prompt("Postgresql user's password", 'POSTGRES_PASSWORD', 'saaskitS3n89mkk')
    
    #env.postgres_db = 'saaskit'
    prompt("Postgresql DATABASE", 'POSTGRES_DB', 'saaskit')
    
    prompt("Django admin username", 'DJANGO_ADMIN', 'admin')
    prompt("Django admin password", 'DJANGO_ADMIN_PASSWORD', 'password')

def install_packages():
    """Install system wide packages"""
    require('hosts',provided_by=[production])
    
    put_origin('./deploy/linode/apt/sources.list', '/etc/apt/sources.list.d/sources.list')
    sudo('apt-get -y update; apt-get -y upgrade;', pty=True)
    #locale
    sudo('dpkg-reconfigure locales; apt-get install -y language-pack-en; locale-gen en_US.UTF-8;', pty=True)
    
    #Because if high-possibility of hanging up by system when too much packages install. 
    sudo('apt-get -y install build-essential gcc libc6-dev', pty=True)
    sudo('apt-get -y install wget nmap unzip wget csstidy ant curl python-dev python-egenix-mxdatetime memcached tar mc libmemcache-dev', pty=True)
    
def install_mail_transfer_agent():
    require('hosts',provided_by=[production])
    sudo('apt-get -y install sendmail;', pty=True)
    
def log_setup():
    """setup log"""
    require('hosts', provided_by=[production])
    sudo('mkdir -p /var/log/webapp; mkdir -p /var/log/webapp/main;', pty=True)
    sudo('mkdir -p /var/log/webapp/assets; mkdir -p /var/log/webapp/user_sites;', pty=True)

def github_config():
    """setup user config for github. global and ssh public keys """
    require('hosts', provided_by=[production])
    sudo('apt-get -y install git-core', pty=True)
    
    #Github user's settings
    run('git config --global github.user deploy-admin', pty=True)
    run('git config --global github.email deploy@crowdsense.com', pty=True)
    run('git config --global github.token 445c8da5521cd969ec42a3de85f323d7', pty=True)
    
    #ssh public keys
    run('mkdir -p ~/.ssh', pty=True)
    put_origin('./deploy/linode/.ssh/id_rsa', '~/.ssh/id_rsa')
    put_origin('./deploy/linode/.ssh/id_rsa.pub', '~/.ssh/id_rsa.pub')
    put_origin('./deploy/linode/.ssh/known_hosts', '~/.ssh/known_hosts')

def postgresql_setup():
    require('hosts',provided_by=[production])
    require('POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', provided_by=[production])
    
    sudo('apt-get -y install postgresql-8.3 postgresql-client-8.3 libpq-dev', pty=True)
    
    put_origin('./deploy/linode/postgresql/pg_hba.conf', '/etc/postgresql/8.3/main/pg_hba.conf')
    sudo('/etc/init.d/postgresql-8.3 restart', pty=True)
    
    run('sudo -u postgres psql -c "create user %s with password \'%s\'"' \
        % (env.POSTGRES_USER, env.POSTGRES_PASSWORD), pty=True)
    run('sudo -u postgres createdb --owner=%s %s' % (env.POSTGRES_USER, env.POSTGRES_DB), pty=True)
    
def postgresql_user_db_flush():
    require('hosts',provided_by=[production])
    require('POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', provided_by=[production])
    
    run('sudo -u postgres psql -c "drop database %s"' % env.POSTGRES_DB, pty=True)
    run('sudo -u postgres psql -c "drop user %s"' % env.POSTGRES_USER, pty=True)
    
    run('sudo -u postgres psql -c "create user %s with password \'%s\'"' \
        % (env.POSTGRES_USER, env.POSTGRES_PASSWORD), pty=True)
    run('sudo -u postgres createdb --owner=%s %s' % (env.POSTGRES_USER, env.POSTGRES_DB), pty=True)


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
    require('hosts',provided_by=[production])
    require('POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', provided_by=[production])
    #TODO: parametrize domain
    sudo('cd /webapp; rm -r %(name)s; git clone git@github.com:CrowdSense/saaskit-core.git %(name)s;' \
         % {'name': env.host_string}, pty=True)
    
    #create local settings
    put('./deploy/_local_settings.py', '/webapp/%s/src/saaskit/local_settings.py' % env.host_string)

    #buildout the project
    sudo('cd /webapp/%s; python ./bootstrap.py -c ./production.cfg; ./bin/buildout -v -c ./production.cfg' % env.host_string, pty=True)
    sudo('chown -R webapp:www-data /webapp', pty=True)

def update_project():
    require('hosts',provided_by=[production])
    sudo('cd /webapp/%s; git pull origin master;' % env.host_string, pty=True)
    sudo('cd /webapp/%s; python ./bootstrap.py -c ./production.cfg; ./bin/buildout -v -c ./production.cfg' % env.host_string, pty=True)
    sudo('chown -R webapp:www-data /webapp', pty=True)
    
def nginx_config():
    """setup nginx"""
    require('hosts', provided_by=[production])
    sudo('apt-get -y install nginx', pty=True)
    sudo('/etc/init.d/nginx stop; rm -f /etc/nginx/site-enabled/default;', pty=True)

    #cp -u ./nginx/assets /etc/nginx/sites-available/assets
    #ln -s /etc/nginx/sites-available/assets /etc/nginx/sites-enabled/assets
    #TODO: parametrize server_name
    put('./deploy/linode/nginx/webapp', '/etc/nginx/sites-available/webapp')
    sudo('ln -f -s /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/webapp', pty=True)
    put('./deploy/linode/nginx/nginx.conf', '/etc/nginx/nginx.conf')
    put('./deploy/linode/nginx/proxy.conf', '/etc/nginx/proxy.conf')
    
    sudo('/etc/init.d/nginx start', pty=True)

def apache2_config():
    require('hosts', provided_by=[production])
    sudo('apt-get -y install apache2 apache2.2-common apache2-mpm-worker apache2-threaded-dev libapache2-mod-wsgi libapache2-mod-rpaf', pty=True)
    sudo('apache2ctl stop; a2dissite 000-default;', pty=True)
    
    put('./deploy/linode/apache/main', '/etc/apache2/sites-available/main')
    put('./deploy/linode/apache/sites', '/etc/apache2/sites-available/sites')
    sudo('a2ensite main; a2ensite sites;', pty=True)
    put('./deploy/linode/apache/apache2.conf', '/etc/apache2/apache2.conf')
    put('./deploy/linode/apache/ports.conf', '/etc/apache2/ports.conf')
    put('./deploy/linode/apache/security', '/etc/apache2/conf.d/security')
    
    sudo('a2enmod rewrite; apache2ctl start;', pty=True)

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
    require('hosts', provided_by=[production])
    sudo('/etc/init.d/apache2 restart', pty=True)
    sudo('/etc/init.d/nginx restart', pty=True)
