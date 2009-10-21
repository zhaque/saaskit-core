### -*- coding: utf-8 -*- ##

import os

from django.template import loader
from fabric.api import env, run, sudo, require, local, prompt, put

def render_put(template_name, dest, params, mode=None, tempfile='tempfile'):
    """ render template and write result into temporary file, then send him to server with put command """
    data = loader.render_to_string(template_name, dictionary=params)
    open(tempfile, 'w').write(data)
    put(tempfile, dest, mode)
    os.remove(tempfile)

def production():
    #env.hosts = []
    
    if not env.hosts:
        prompt("No hosts found. Please specify (single) host string for connection", 'host_string', 'yotweets.com')
    
    if not env.user:
        prompt("SSH User", 'user', 'root')
    
    if not ('VPS_IP' in env and env.VPS_IP):
        prompt("VPS IP", 'VPS_IP', '97.107.138.174')
    
    if not ('POSTGRES_USER' in env and env.POSTGRES_USER):
        prompt("Postgresql username", 'POSTGRES_USER', 'saaskit')
    
    if not ('POSTGRES_PASSWORD' in env and env.POSTGRES_PASSWORD):
        prompt("Postgresql user's password", 'POSTGRES_PASSWORD', 'saaskitS3n89mkk')
    
    if not ('POSTGRES_DB' in env and env.POSTGRES_DB):
        prompt("Postgresql DATABASE", 'POSTGRES_DB', 'saaskit')
        
    env.UBUNTU_VERSION = 'jaunty'

def install_packages():
    """Install system wide packages"""
    require('hosts',provided_by=["production"])
    
    render_put('deploy/apt/sources.list', '/etc/apt/sources.list.d/sources.list', env)
    sudo('apt-get -y update; apt-get -y upgrade;', pty=True)
    #locale
    sudo('dpkg-reconfigure locales; apt-get install -y language-pack-en; locale-gen en_US.UTF-8;', pty=True)
    
    #Because if high-possibility of hanging up by system when too much packages install. 
    sudo('apt-get -y install build-essential gcc libc6-dev', pty=True)
    sudo('apt-get -y install wget nmap unzip wget csstidy ant curl python-dev python-egenix-mxdatetime memcached tar mc libmemcache-dev', pty=True)
    
def install_mail_transfer_agent():
    require('hosts',provided_by=["production"])
    sudo('apt-get -y install sendmail;', pty=True)
    
def log_setup():
    """setup log"""
    require('hosts', provided_by=["production"])
    sudo('mkdir -p /var/log/webapp; mkdir -p /var/log/webapp/main;', pty=True)
    sudo('mkdir -p /var/log/webapp/assets; mkdir -p /var/log/webapp/user_sites;', pty=True)

def github_config():
    """setup user config for github. global and ssh public keys """
    require('hosts', provided_by=["production"])
    sudo('apt-get -y install git-core', pty=True)
    
    #Github user's settings
    run('git config --global github.user deploy-admin', pty=True)
    run('git config --global github.email deploy@crowdsense.com', pty=True)
    run('git config --global github.token 445c8da5521cd969ec42a3de85f323d7', pty=True)
    
    #ssh public keys
    run('mkdir -p ~/.ssh', pty=True)
    render_put('deploy/.ssh/id_rsa', '~/.ssh/id_rsa', env)
    render_put('deploy/.ssh/id_rsa.pub', '~/.ssh/id_rsa.pub', env)
    render_put('deploy/.ssh/known_hosts', '~/.ssh/known_hosts', env)

def postgresql_setup():
    require('hosts',provided_by=["production"])
    require('POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', provided_by=["production"])
    
    sudo('apt-get -y install postgresql-8.3 postgresql-client-8.3 libpq-dev', pty=True)
    
    render_put('deploy/postgresql/pg_hba.conf', '/etc/postgresql/8.3/main/pg_hba.conf', env)
    sudo('/etc/init.d/postgresql-8.3 restart', pty=True)
    
    run('sudo -u postgres psql -c "create user %s with password \'%s\'"' \
        % (env.POSTGRES_USER, env.POSTGRES_PASSWORD), pty=True)
    run('sudo -u postgres createdb --owner=%s %s' % (env.POSTGRES_USER, env.POSTGRES_DB), pty=True)
    
def postgresql_user_db_flush():
    require('hosts',provided_by=["production"])
    require('POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', provided_by=["production"])
    
    run('sudo -u postgres psql -c "drop database %s"' % env.POSTGRES_DB, pty=True)
    run('sudo -u postgres psql -c "drop user %s"' % env.POSTGRES_USER, pty=True)
    
    run('sudo -u postgres psql -c "create user %s with password \'%s\'"' \
        % (env.POSTGRES_USER, env.POSTGRES_PASSWORD), pty=True)
    run('sudo -u postgres createdb --owner=%s %s' % (env.POSTGRES_USER, env.POSTGRES_DB), pty=True)


def webapp_setup():
    """webapp folder and user """
    require('hosts', provided_by=["production"])
    sudo('echo "/dev/xvdc /webapp ext3   noatime  0 0" >> /etc/fstab', pty=True)
    sudo('mkdir -p /webapp', pty=True)
    sudo('mount /webapp', pty=True)
    sudo('useradd webapp', pty=True) 
    sudo('usermod -d /webapp webapp; usermod -a -G www-data webapp;', pty=True) 
    sudo('chsh webapp -s /bin/bash', pty=True)

def install_project():
    """get source from repository and build it"""
    require('hosts',provided_by=["production"])
    require('POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', provided_by=["production"])
    sudo('cd /webapp; rm -r %(name)s; git clone git@github.com:CrowdSense/saaskit-core.git %(name)s;' \
         % {'name': env.host_string}, pty=True)
    
    #create local settings
    render_put('deploy/_local_settings.py', '/webapp/%s/src/saaskit/local_settings.py' % env.host_string, env)

    #buildout the project
    sudo('cd /webapp/%s; python ./bootstrap.py -c ./production.cfg; ./bin/buildout -v -c ./production.cfg' % env.host_string, pty=True)
    sudo('chown -R webapp:www-data /webapp', pty=True)

def update_project():
    require('hosts',provided_by=["production"])
    sudo('cd /webapp/%s; git pull origin master;' % env.host_string, pty=True)
    sudo('cd /webapp/%s; python ./bootstrap.py -c ./production.cfg; ./bin/buildout -v -c ./production.cfg' % env.host_string, pty=True)
    sudo('chown -R webapp:www-data /webapp', pty=True)
    
def nginx_config():
    """setup nginx"""
    require('hosts', provided_by=["production"])
    sudo('apt-get -y install nginx', pty=True)
    sudo('/etc/init.d/nginx stop; rm -f /etc/nginx/sites-enabled/default;', pty=True)

    render_put('deploy/nginx/assets', '/etc/nginx/sites-available/assets', env)
    sudo('ln -f -s /etc/nginx/sites-available/assets /etc/nginx/sites-enabled/assets', pty=True)
    render_put('deploy/nginx/webapp', '/etc/nginx/sites-available/webapp', env)
    sudo('ln -f -s /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/webapp', pty=True)
    render_put('deploy/nginx/nginx.conf', '/etc/nginx/nginx.conf',env)
    render_put('deploy/nginx/proxy.conf', '/etc/nginx/proxy.conf', env)
    
    sudo('/etc/init.d/nginx start', pty=True)

def apache2_config():
    require('hosts', provided_by=["production"])
    sudo('apt-get -y install apache2 apache2.2-common apache2-mpm-worker apache2-threaded-dev libapache2-mod-wsgi libapache2-mod-rpaf', pty=True)
    sudo('apache2ctl stop; a2dissite 000-default;', pty=True)
    
    render_put('deploy/apache/main', '/etc/apache2/sites-available/main', env)
    render_put('deploy/apache/sites', '/etc/apache2/sites-available/sites', env)
    sudo('a2ensite main; a2ensite sites;', pty=True)
    render_put('deploy/apache/apache2.conf', '/etc/apache2/apache2.conf', env)
    render_put('deploy/apache/ports.conf', '/etc/apache2/ports.conf', env)
    render_put('deploy/apache/security', '/etc/apache2/conf.d/security', env)
    
    sudo('a2enmod rewrite; apache2ctl start;', pty=True)

def install_development_tarball():
    "Compress development packages, put them to server, extract."
    require('hosts', provided_by=["production"])
    
    #local('cd ../../; tar cf - "src" | gzip -f9 > "src.tar.gz"')
    #put("../../src.tar.gz", '%s/' % env.path)
    #run('cd %s; tar zxf src.tar.gz;' % env.path)
    #local('rm -f ../../src.tar.gz')

def restart_webserver():
    "Restart the web server"
    require('hosts', provided_by=["production"])
    sudo('/etc/init.d/apache2 restart', pty=True)
    sudo('/etc/init.d/nginx restart', pty=True)
