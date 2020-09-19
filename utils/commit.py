import os
from .ps import Ps
from .images import Images
from .rm import Rm
import subprocess
import traceback


def Commit(container_id, image_id, **kwargs):
    try:
        containers = Ps()
        if container_id not in containers:
            raise Exception("No container with id {0}".format(container_id))
        
        images = Images()
        if image_id not in images:
            raise Exception("No image with id {0}".format(image_id))

        Rm(container_id)

        subprocess.run(['btrfs', 'subvolume', 'snapshot', '/var/mocker/images/{0}'.format(image_id), '/var/mocker/ps/{0}'.format(container_id)], check=True)
        
        print("commit :: Created new image out of image with id {1} by applying changes from container with id {0} successfully.".format(container_id, image_id))
        
    except Exception as e:
        print("commit :: Failed to create new image out of image with id {1} by applying changes from container with id {0}.".format(container_id, image_id))
        traceback.print_exc()
