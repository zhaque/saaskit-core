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


def ifnotsetted(key, default, is_prompt=False, text=None, validate=None):
    if not (key in env and env[key]):
        if is_prompt:
            prompt(text, key, default, validate)
        else:
            env['key'] = default

#env.hosts = []

ifnotsetted('hosts', 'yotweets.com', True, 
    "No hosts found. Please specify (single) host string for connection")
ifnotsetted('user', 'root', True, "Server user name")
ifnotsetted('VPS_IP', '97.107.138.174', True, "VPS IP")
ifnotsetted('POSTGRES_USER', 'saaskit', True, "PostgreSQL user name")
ifnotsetted('POSTGRES_PASSWORD', 'saaskitS3n89mkk', True, "PostgreSQL user's password")
ifnotsetted('POSTGRES_DB', 'saaskit', True, "PostgreSQL DATABASE")
ifnotsetted('UBUNTU_VERSION', 'jaunty')
ifnotsetted('PAYPAL_EMAIL', 'admin_1255085897_biz@crowdsense.com', True, "PAYPAL EMAIL")

env.SOURCE_PATH = 'src/saaskit'
env.git_path = 'git@github.com:CrowdSense/saaskit-core.git'


def install_packages():
    """Install system wide packages"""
    render_put('deploy/apt/sources.list', '/etc/apt/sources.list.d/sources.list', env)
    sudo('apt-get -y update; apt-get -y upgrade;', pty=True)
    #locale
    sudo('dpkg-reconfigure locales; apt-get install -y language-pack-en; locale-gen en_US.UTF-8;', pty=True)
    
    #Because if high-possibility of hanging up by system when too much packages install. 
    sudo('apt-get -y install build-essential gcc libc6-dev', pty=True)
    sudo('apt-get -y install wget nmap unzip wget csstidy ant curl python-dev python-egenix-mxdatetime memcached tar mc libmemcache-dev', pty=True)
    
def install_mail_transfer_agent():
    sudo('apt-get -y install sendmail;', pty=True)
    
def log_setup():
    """setup log"""
    sudo('mkdir -p /var/log/webapp; mkdir -p /var/log/webapp/main;', pty=True)
    sudo('mkdir -p /var/log/webapp/assets; mkdir -p /var/log/webapp/user_sites;', pty=True)

def github_config():
    """setup user config for github. global and ssh public keys """
    sudo('apt-get -y install git-core', pty=True)
    
    #Github user's settings
    run('git config --global github.user deploy-admin', pty=True)
    run('git config --global github.email deploy@crowdsense.com', pty=True)
    run('git config --global github.token 445c8da5521cd969ec42a3de85f323d7', pty=True)
    
    #ssh public keys
    run('mkdir -p ~/.ssh', pty=True)
    render_put('deploy/.ssh/id_rsa', '~/.ssh/id_rsa', env, mode=0600)
    render_put('deploy/.ssh/id_rsa.pub', '~/.ssh/id_rsa.pub', env)
    render_put('deploy/.ssh/known_hosts', '~/.ssh/known_hosts', env)

def postgresql_setup():
    require('POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB')
    
    sudo('apt-get -y install postgresql-8.3 postgresql-client-8.3 libpq-dev', pty=True)
    
    render_put('deploy/postgresql/pg_hba.conf', '/etc/postgresql/8.3/main/pg_hba.conf', env)
    sudo('/etc/init.d/postgresql-8.3 restart', pty=True)
    
    run('sudo -u postgres psql -c "create user %s with password \'%s\'"' \
        % (env.POSTGRES_USER, env.POSTGRES_PASSWORD), pty=True)
    run('sudo -u postgres createdb --owner=%s %s' % (env.POSTGRES_USER, env.POSTGRES_DB), pty=True)
    
def postgresql_user_db_flush():
    require('POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB')
    
    run('sudo -u postgres psql -c "drop database %s"' % env.POSTGRES_DB, pty=True)
    run('sudo -u postgres psql -c "drop user %s"' % env.POSTGRES_USER, pty=True)
    
    run('sudo -u postgres psql -c "create user %s with password \'%s\'"' \
        % (env.POSTGRES_USER, env.POSTGRES_PASSWORD), pty=True)
    run('sudo -u postgres createdb --owner=%s %s' % (env.POSTGRES_USER, env.POSTGRES_DB), pty=True)


def webapp_setup():
    """webapp folder and user """
    sudo('echo "/dev/xvdc /webapp ext3   noatime  0 0" >> /etc/fstab', pty=True)
    sudo('mkdir -p /webapp', pty=True)
    sudo('mount /webapp', pty=True)
    sudo('useradd webapp', pty=True) 
    sudo('usermod -d /webapp webapp; usermod -a -G www-data webapp;', pty=True) 
    sudo('chsh webapp -s /bin/bash', pty=True)

def install_project():
    """get source from repository and build it"""
    require('POSTGRES_USER', 'POSTGRES_PASSWORD', 'POSTGRES_DB', 'SOURCE_PATH')
    
    sudo('cd /webapp; rm -f -r %(host_string)s; git clone %(git_path)s %(host_string)s;' \
         % env, pty=True)
    
    build_source()

def update_project():
    sudo('cd /webapp/%s; git pull origin master;' % env.host_string, pty=True)
    build_source()
    
def build_source():
    #create local settings
    render_put('deploy/_local_settings.py', 
               '/webapp/%s/%s/local_settings.py' % (env.host_string, env.SOURCE_PATH), 
               env)
    #copy sites fixture
    render_put('deploy/sites.json', 
               '/webapp/%s/%s/sites.json' % (env.host_string, env.SOURCE_PATH), 
               env)
    
    #buildout the project
    sudo('cd /webapp/%s; python ./bootstrap.py -c ./production.cfg; ./bin/buildout -v -c ./production.cfg; ./bin/main_site loaddata ./%s/sites.json;' \
            % (env.host_string, env.SOURCE_PATH), pty=True)
    sudo('chown -R webapp:www-data /webapp', pty=True)

def nginx_config():
    """setup nginx"""
    require('SOURCE_PATH')
    sudo('apt-get -y install nginx', pty=True)
    sudo('/etc/init.d/nginx stop; rm -f /etc/nginx/sites-enabled/default;', pty=True)
    
    env.MEDIA_ROOT = '/webapp/%s/%s/wide_media' % (env.host_string, env.SOURCE_PATH)
    
    render_put('deploy/nginx/assets', '/etc/nginx/sites-available/assets', env)
    sudo('ln -f -s /etc/nginx/sites-available/assets /etc/nginx/sites-enabled/assets', pty=True)
    render_put('deploy/nginx/webapp', '/etc/nginx/sites-available/webapp', env)
    sudo('ln -f -s /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/webapp', pty=True)
    render_put('deploy/nginx/nginx.conf', '/etc/nginx/nginx.conf', env)
    render_put('deploy/nginx/proxy.conf', '/etc/nginx/proxy.conf', env)
    
    sudo('/etc/init.d/nginx start', pty=True)

def apache2_config():
    """ setup apache2 """
    sudo('apt-get -y install apache2 apache2.2-common apache2-mpm-worker apache2-threaded-dev libapache2-mod-wsgi libapache2-mod-rpaf', pty=True)
    sudo('apache2ctl stop; a2dissite 000-default;', pty=True)
    
    render_put('deploy/apache/main', '/etc/apache2/sites-available/main', env)
    render_put('deploy/apache/sites', '/etc/apache2/sites-available/sites', env)
    sudo('a2ensite main; a2ensite sites;', pty=True)
    render_put('deploy/apache/apache2.conf', '/etc/apache2/apache2.conf', env)
    render_put('deploy/apache/ports.conf', '/etc/apache2/ports.conf', env)
    render_put('deploy/apache/security', '/etc/apache2/conf.d/security', env)
    
    sudo('a2enmod rewrite; apache2ctl start;', pty=True)

#===============================================================================
# def install_development_tarball():
#    "Compress development packages, put them to server, extract."
#    
#    local('cd ../../; tar cf - "src" | gzip -f9 > "src.tar.gz"')
#    put("../../src.tar.gz", '%s/' % env.path)
#    run('cd %s; tar zxf src.tar.gz;' % env.path)
#    local('rm -f ../../src.tar.gz')
#===============================================================================

def restart_webserver():
    "Restart the web server"
    sudo('/etc/init.d/apache2 restart', pty=True)
    sudo('/etc/init.d/nginx restart', pty=True)
