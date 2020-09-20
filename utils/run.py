import os
import random
from .ps import Ps
from .images import Images
import pyroute2
import cgroups
import subprocess
import traceback


def Run(image_id, command, **kwargs):
    try:
        images = Images()
        if image_id not in images:
            raise Exception("No image with id {0}".format(image_id))

        while True:
            uuid = ''.join(random.choices('0123456789', k=6))
            containers = Ps()
            if uuid not in containers:
                break
        
        uuid_path = os.path.join('/var/myOwnDocker/ps', uuid)
        if not os.path.exists(uuid_path):
            os.makedirs(uuid_path)

        print("run :: Creating container with id {0}...".format(uuid))

        ip = str(random.randint(100, 255))
        mac = str(int(uuid[-2:]))
        
        with pyroute2.IPDB() as ipdb:
            veth0_name = 'veth0_{0}'.format(uuid)
            veth1_name = 'veth1_{0}'.format(uuid)
            netns_name = 'netns_{0}'.format(uuid)
            bridge_interface_name = 'bridge0'

            with ipdb.create(kind='veth', ifname=veth0_name, peer=veth1_name) as interface:
                interface.up()
                if bridge_interface_name not in ipdb.interfaces.keys():
                    ipdb.create(kind='bridge', ifname=bridge_interface_name).commit()
                interface.set_target('master', bridge_interface_name)

            pyroute2.netns.create(netns_name)

            with ipdb.interfaces[veth1_name] as veth1:
                veth1.net_ns_fd = netns_name

            ns = pyroute2.IPDB(nl=pyroute2.NetNS(netns_name))
            with ns.interfaces.lo as lo:
                lo.up()
            with ns.interfaces[veth1_name] as veth1:
                veth1.address = "02:42:ac:11:00:{0}".format(mac)
                veth1.add_ip('10.0.0.{0}/24'.format(ip))
                veth1.up()
            ns.routes.add({'dst': 'default', 'gateway': '10.0.0.1'}).commit()

            print("run :: Creating snapshot...")

            subprocess.run(['btrfs', 'subvolume', 'snapshot', '/var/myOwnDocker/images/{0}'.format(image_id), '/var/myOwnDocker/ps/{0}'.format(uuid)], check=True)
            with open('/var/myOwnDocker/ps/{0}/{1}/etc/resolv.conf'.format(uuid, image_id), 'w') as f:
                f.write('nameserver 8.8.8.8\n')
            with open('/var/myOwnDocker/ps/{0}/{1}/{2}.cmd'.format(uuid, image_id, uuid), 'w') as f:
                f.write(command + '\n')

            try:
                print("run :: Creating Cgroup...")
                user = os.getlogin()
                cgroups.user.create_user_cgroups(user)
                cg = cgroups.Cgroup(uuid)
                cg.set_cpu_limit(50)
                cg.set_memory_limit(512)

                new_root_path = '/var/myOwnDocker/ps/{0}/{1}'.format(uuid, image_id)

                def put_in_cgroup():
                    try:
                        print("run :: put_in_cgroup :: Putting process in Cgroup...")
                        pid = os.getpid()
                        print("run :: put_in_cgroup :: pid={}".format(pid))
                        cg = cgroups.Cgroup(uuid)
                        cg.add(pid)
                        print("run :: put_in_cgroup :: Added pid in Cgroup.")
                        pyroute2.netns.setns(netns_name)
                        print("run :: put_in_cgroup :: Isolated NetNS.")
                        os.chdir(new_root_path)
                        os.chroot(new_root_path)
                        print("run :: put_in_cgroup :: Successfully put process in Cgroup.")
                    except Exception as e:
                        print("run :: put_in_cgroup :: Failed to put process in Cgroup.")
                        traceback.print_exc()

                print("run :: Running container with id {0} and command {1}...".format(uuid, command))

                process = subprocess.run(['unshare -fmuip --mount-proc && /bin/mount -t proc proc /proc && sleep 2 && ' + command], 
                    preexec_fn=put_in_cgroup, 
                    universal_newlines=True, 
                    check=True,
                    executable='/bin/bash')
                out, err = process.stdout, process.stderr
                if out is None:
                    out = ""
                if err is None:
                    err = ""

                with open(os.path.join('/var/myOwnDocker/ps/{0}'.format(uuid), 'out.log'), 'a') as f:
                    f.write(out + '\n')
                with open(os.path.join('/var/myOwnDocker/ps/{0}'.format(uuid), 'err.log'), 'a') as f:
                    f.write(err + '\n')

                print("run :: Container with id {0} and command {1} ran successfully.".format(uuid, command))
            except:
                print("run :: Failed to run container with id {0} and command {1}.".format(uuid, command))
                traceback.print_exc()
            finally:
                pyroute2.NetNS(netns_name).close()
                pyroute2.netns.remove(netns_name)
                ipdb.interfaces[veth0_name].remove()

    except Exception as e:
        print("run :: Failed to create container.")
        traceback.print_exc()












