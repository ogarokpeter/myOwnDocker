import os


def Images(**kwargs):
    try:
        images = os.listdir('/var/mocker/images')
    except Exception as e:
        images = []
    print("images :: Total images: {0}.".format(len(images)))
    for image in images:
        print(image)
    return images