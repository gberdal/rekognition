import boto3
import pprint
import os
import piexif
import imghdr


client = boto3.client('rekognition')


def read_image(image_path):
    """
    Reads images as bytes
    :param image_path: string
    :return: string
    """
    exceptions = ['.DS_Store']
    supported_img_types = ['jpg', 'jpeg', 'png']
    filename = os.path.basename(image_path)
    img_type = imghdr.what(image_path)
    if filename in exceptions:
        return
    if img_type not in supported_img_types:
        raise Exception('Invalid image type')
    with open(image_path, 'rb') as fh:
        return fh.read()


def get_moderation_labels(image_bytes):
    """
    Uses AWS Rekognition to retrieve moderation labels
    :param image_bytes: string
    :return: dict
    """
    _labels = client.detect_moderation_labels(
        Image={
            'Bytes': image_bytes
        },
        MinConfidence=80  # adjust for filtering out labels with low confidence
    )

    return _labels


def get_labels(image_bytes):
    """
    Uses AWS Rekognition to retrieve moderation labels
    :param image_bytes: string
    :return: dict
    """
    _labels = client.detect_labels(
        Image={
            'Bytes': image_bytes
        },
        MinConfidence=80  # adjust for filtering out labels with low confidence
    )

    return _labels


def get_exif(image_path, tags="*"):
    """
    Retrieves EXIF tags if they exist
    :type tags: list
    :param image_path: string
    :return: dict
    """
    _tags = {}
    exif_dict = piexif.load(image_path)
    for ifd in ("0th", "Exif", "GPS", "1st"):
        for tag in exif_dict[ifd]:
            tag_name = piexif.TAGS[ifd][tag]["name"]
            if tags == "*" or tag_name in tags:
                _tags[tag_name] = exif_dict[ifd][tag]
    return _tags


# read images folder and process them
response = []
for root, dirs, files in os.walk('images'):
    for file in files:
        path = "/".join([root, file])
        item = {}

        # get images as bytes
        image = read_image(image_path=path)
        if not image:
            continue

        # get mod labels
        mod_labels = get_moderation_labels(image_bytes=image)
        item['ImagePath'] = path
        item['ModerationLabels'] = [labels['Name'] for labels in mod_labels.get('ModerationLabels')]

        # get labels
        labels = get_labels(image_bytes=image)
        item['Labels'] = [labels['Name'] for labels in labels.get('Labels')]

        # get exif
        exif = get_exif(image_path=path, tags=['Make', 'Model'])
        item['Exif'] = exif

        response.append(item)

    pprint.pprint(response)
