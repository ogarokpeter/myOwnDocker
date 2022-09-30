import os
import random
import requests
import tarfile
import traceback
import shutil
from .init import Init


def Pull(image, **kwargs):
    try:
        print("pull :: Getting authorization token...")
        url = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/{0}:pull'.format(image)
        token_req = requests.get(url)
        token = token_req.json()['token']
        headers = {'Authorization': 'Bearer {0}'.format(token)}
        
        print("pull :: Getting manifest of {0} image...".format(image))
        url = 'https://registry-1.docker.io/v2/library/{0}/manifests/latest'.format(image)
        manifest_req = requests.get(url, headers=headers)
        manifest = manifest_req.json()

        layer_sigs = [layer['blobSum'] for layer in manifest['fsLayers']]
        unique_layer_sigs = set(layer_sigs)

        uuid = ''.join(random.sample('qwertyuiopasdfghjklzxcvbnm', 15))
        uuid_path = os.path.join('tmp', uuid)
        if not os.path.exists(uuid_path):
            os.makedirs(uuid_path)

        layers_path = os.path.join(uuid_path, 'layers')
        if not os.path.exists(layers_path):
            os.makedirs(layers_path)

        contents_path = os.path.join(uuid_path, 'contents')
        if not os.path.exists(contents_path):
            os.makedirs(contents_path)

        print("pull :: Fetching layers:")
        for i, sig in enumerate(unique_layer_sigs):
            print("pull :: Fetching layer {0}...".format(sig))
            url = 'https://registry-1.docker.io/v2/library/{0}/blobs/{1}'.format(image, sig)
            arch = os.path.join(layers_path, str(i)) + '.tar'
            cont = requests.get(url, stream=True, headers=headers)
            with open(arch, 'wb') as f:
                for chunk in cont.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("pull :: Extracting layer {0}...".format(sig))
            with tarfile.open(arch, 'r') as tar:
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner) 
                    
                
                safe_extract(tar, contents_path)
        print("pull :: Successfully pulled image {0}.".format(image))
    except Exception as e:
        print("pull :: Failed to pull image {0}.".format(image))
        traceback.print_exc()
    
    uuid = Init(contents_path)
    shutil.rmtree(uuid_path)
    return uuid
