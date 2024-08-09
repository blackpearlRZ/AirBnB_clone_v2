#!/usr/bin/python3
""" Packs webstatic into an archive """
import os
from fabric.api import local
from datetime import datetime


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
