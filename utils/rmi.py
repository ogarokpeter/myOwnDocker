import subprocess
import shutil
import traceback


def Rmi(image_id, **kwargs):
    try:
        subprocess.run(['btrfs', 'subvolume', 'delete', '/var/myOwnDocker/images/{0}'.format(image_id)], check=True)
        print("rmi :: Successfully deleted image with id {0}".format(image_id))
    except Exception as e:
        print("rmi :: Failed to delete image with id {0}".format(image_id))
        traceback.print_exc()
    shutil.rmtree('/var/myOwnDocker/images/{0}'.format(image_id), ignore_errors=True)