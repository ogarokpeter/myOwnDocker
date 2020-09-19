import os
import random
import subprocess
import shutil
import traceback
from .images import Images


def copytree(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                try:
                    shutil.copy2(s, d, follow_symlinks=False)
                except Exception as e:
                    continue


def Init(directory='/', **kwargs):
    if not os.path.exists('/var/mocker/images'):
        os.makedirs('/var/mocker/images')
    if not os.path.exists('/var/mocker/ps'):
        os.makedirs('/var/mocker/ps')
    try:
        while True:
            uuid = ''.join(random.sample('qwertyuiopasdfghjklzxcvbnm', 15))
            images = Images()
            if uuid not in images:
                break

        uuid_path = os.path.join('/var/mocker/images', uuid)
        
        subprocess.run(['btrfs', 'subvolume', 'create', uuid_path], check=True)
        copytree(directory, uuid_path)
        print("init :: Initialized image successfully. Image id is {0}".format(uuid))
        return uuid
    except Exception as e:
        print("init :: Failed to initialize image.")
        traceback.print_exc()
