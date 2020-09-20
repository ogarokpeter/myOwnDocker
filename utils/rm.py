import os
import subprocess
import shutil
import cgroups
import traceback


def Rm(container_id, **kwargs):
    try:
        for image_id in os.listdir('/var/myOwnDocker/ps/{0}'.format(container_id)):
            if image_id.endswith('.log'):
                shutil.rm(os.path.join('/var/myOwnDocker/ps/{0}'.format(container_id), image_id))
            else:
                subprocess.run(['btrfs', 'subvolume', 'delete', '/var/myOwnDocker/ps/{0}/{1}'.format(container_id, image_id)], check=True)
        cg = cgroups.Cgroup(container_id)
        cg.delete()
        print("rm :: Successfully deleted container with id {0}".format(container_id))
    except Exception as e:
        print("rm :: Failed to delete container with id {0}".format(container_id))
        traceback.print_exc()
    shutil.rmtree('/var/myOwnDocker/ps/{0}'.format(container_id), ignore_errors=True)