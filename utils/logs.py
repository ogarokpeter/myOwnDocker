import os
from .ps import Ps
import subprocess
import traceback


def Logs(container_id, **kwargs):
    try:
        containers = Ps()
        if container_id not in containers:
            raise Exception("No container with id {0}".format(container_id))

        with open(os.path.join('/var/myOwnDocker/ps/{0}'.format(container_id), 'out.log'), 'r') as f:
            out = f.read()
        with open(os.path.join('/var/myOwnDocker/ps/{0}'.format(container_id), 'err.log'), 'r') as f:
            err = f.read()

        print("logs :: Extracted logs from container with id {0} successfully.".format(container_id))

        print("Out logs:")
        print(out)

        print("Error logs:")
        print(err)
        
    except Exception as e:
        print("logs :: Failed to extract logs from container with id {0}.".format(container_id))
        traceback.print_exc()
