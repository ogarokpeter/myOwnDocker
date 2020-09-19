#!/usr/bin/python3

import argparse
from utils.base import Base
from utils.init import Init
from utils.pull import Pull
from utils.rmi import Rmi
from utils.images import Images
from utils.ps import Ps
from utils.run import Run
from utils.exec import Exec
from utils.logs import Logs
from utils.rm import Rm
from utils.commit import Commit


if __name__ == '__main__':

    func = Base

    parser = argparse.ArgumentParser(description='My Own Docker - Docker written in Python.')
    
    subparsers = parser.add_subparsers(help='My Own Docker commands')

    parser_init = subparsers.add_parser('init', help='Create container image using given directory as root. Return container image id.')
    parser_init.add_argument('--directory', '-dir', default='/', help='Directory to use as root')
    parser_init.set_defaults(func=Init)
    
    parser_pull = subparsers.add_parser('pull', help='Download the latest tag of a given container image from Docker Hub. Return container image id.')
    parser_pull.add_argument('--image', '-im', help='Container image to download')
    parser_pull.set_defaults(func=Pull)
    
    parser_rmi = subparsers.add_parser('rmi', help='Delete container image with given image id.')
    parser_rmi.add_argument('--image_id', '-im_id', help='Container image id')
    parser_rmi.set_defaults(func=Rmi)
    
    parser_images = subparsers.add_parser('images', help='Print all local container images.')
    parser_images.set_defaults(func=Images)
    
    parser_ps = subparsers.add_parser('ps', help='Print all containers.')
    parser_ps.set_defaults(func=Ps)
    
    parser_run = subparsers.add_parser('run', help='Create a container from given container image id and run it with a given command.')
    parser_run.add_argument('--image_id', '-im_id', help='Container image id')
    parser_run.add_argument('--command', '-c', help='Command')
    parser_run.set_defaults(func=Run)
    
    parser_exec = subparsers.add_parser('exec', help='Execute a given command in a container with given id.')
    parser_exec.add_argument('--container_id', '-c_id', help='Container id')
    parser_exec.add_argument('--command', '-c', help='Command')
    parser_exec.set_defaults(func=Exec)
    
    parser_logs = subparsers.add_parser('logs', help='Print logs from the container with given id.')
    parser_logs.add_argument('--container_id', '-c_id', help='Container id')
    parser_logs.set_defaults(func=Logs)
    
    parser_rm = subparsers.add_parser('rm', help='Delete a container with given id.')
    parser_rm.add_argument('--container_id', '-c_id', help='Container id')
    parser_rm.set_defaults(func=Rm)
    
    parser_commit = subparsers.add_parser('commit', help='Create a new container by applying changes from a container with given id to image with given id.')
    parser_commit.add_argument('--container_id', '-c_id', help='Container id')
    parser_commit.add_argument('--image_id', '-im_id', help='Container image id')
    parser_commit.set_defaults(func=Commit)
    
    args = parser.parse_args()

    args.func(**vars(args))
    
