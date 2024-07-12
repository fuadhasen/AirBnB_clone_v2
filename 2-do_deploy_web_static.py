#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from the contents of the web_static
"""
import os
from fabric.api import env, run, put, sudo
import datetime

env.hosts = ['100.26.152.53', '35.174.208.133']


def do_deploy(archive_path):
    """ function to deploy archive """
    if archive_path:
        a_name = os.path.basename(archive_path)
        a_folder_name = a_name.split('.')[0]

        put(archive_path, "/tmp")
        # Uncompress the archive
        sudo("mkdir -p /data/web_static/releases/{}".format(a_folder_name))
        sudo("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(a_name, a_folder_name))
        sudo("rm /tmp/{}".format(a_name))
        sudo("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(a_folder_name, a_folder_name))
        sudo("rm -rf /data/web_static/releases/{}/web_static".format(a_folder_name))
        sudo("rm /data/web_static/current")

        sudo("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(a_folder_name))
        return True
    else:
        return False
