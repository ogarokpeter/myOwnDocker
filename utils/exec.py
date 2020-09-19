import os
from .ps import Ps
import cgroups
import subprocess
import traceback


def Exec(container_id, command, **kwargs):
    try:
        containers = Ps()
        if container_id not in containers:
            raise Exception("No container with id {0}".format(container_id))
        
        try:
            cg = cgroups.Cgroup(container_id)
        except Exception as e:
            raise Exception("Container with id {0} is not running".format(container_id))


        def put_in_cgroup():
            try:
                print("exec :: put_in_cgroup :: Putting process in Cgroup...")
                pid = os.getpid()
                print("exec :: put_in_cgroup :: pid={}".format(pid))
                cg = cgroups.Cgroup(container_id)
                cg.add(pid)
                print("exec :: put_in_cgroup :: Successfully put process in Cgroup.")
            except Exception as e:
                print("exec :: put_in_cgroup :: Failed to put process in Cgroup.")
                traceback.print_exc()

        print("exec :: Running command {1} in container with id {0}...".format(container_id, command))

        process = subprocess.run([command], 
            preexec_fn=put_in_cgroup, 
            universal_newlines=True, 
            check=True,
            executable='/bin/bash')
        out, err = process.stdout, process.stderr
        if out is None:
            out = ""
        if err is None:
            err = ""

        with open(os.path.join('/var/mocker/ps/{0}'.format(container_id), 'out.log'), 'a') as f:
            f.write(out + '\n')
        with open(os.path.join('/var/mocker/ps/{0}'.format(container_id), 'err.log'), 'a') as f:
            f.write(err + '\n')

        print("exec :: Command {1} ran successfully in container with id {0}.".format(container_id, command))
    
    except Exception as e:
        print("exec :: Failed to run command {1} in container with id {0}.".format(container_id, command))
        traceback.print_exc()