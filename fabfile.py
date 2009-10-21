### -*- coding: utf-8 -*- ##

import os

from saaskit.fabfile import * 

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
    