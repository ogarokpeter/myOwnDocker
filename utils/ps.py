import os


def Ps(**kwargs):
    try:
        ps = os.listdir('/var/myOwnDocker/ps')
    except Exception as e:
        ps = []
    print("ps :: Total containers: {0}.".format(len(ps)))
    for p in ps:
        print(p)
    return ps