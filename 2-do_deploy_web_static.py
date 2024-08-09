#!/usr/bin/python3
""" Packs webstatic into an archive """
import os
from fabric.api import *
from datetime import datetime

env.hosts = ['54.196.38.185', '35.153.232.27']


def do_pack():
    """ Generates a .tgz archive from web_static """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    full_path = "web_static_" + date

    if not os.path.exists('./versions'):
        os.mkdir('./versions')

    local(f"tar -cvzf versions/{full_path}.tgz web_static")
    print(f"Packing web_static to versions/{full_path}.tgz")
    if os.path.getsize(f"versions/{full_path}.tgz"):
        size = os.path.getsize(f"versions/{full_path}.tgz")
        print(f"web_static packed: versions/{full_path} -> {size}Bytes")
        return f"{full_path}.tgz"
    return None


def do_deploy(archive_path):
    """distributes an archive to the web server"""
    if not os.path.exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        not_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run(f'mkdir -p {path}{not_ext}/')
        run(f'tar -xzf /tmp/{file_n} -C {path}{not_ext}/')
        run(f'rm /tmp/{file_n}')
        run('mv {0}{1}/web_static/* {0}{1}'.format(path, not_ext))
        run(f'rm -rf {path}{not_ext}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {path}{not_ext}/ /data/web_static/current')
        return True
    except Exception as e:
        return False
