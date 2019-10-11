## Rekognition
A prototype Python application for testing AWS Rekognition on localhost.

### Install
Log in with mshell to get access to the service in AWS
```bash
mshell-aws-login
```

Start a virtualenv and install requirements
```bash
virtualenv reko -p python3
source reko/bin/activate
cd rekognition
pip install -r requirements.txt
```

Put your images into the directory `/images` and start the application with 
```bash
python start.py
```
For more information about AWS Rekognition read the [Developer Guide](https://docs.aws.amazon.com/rekognition/latest/dg/rekognition-dg.pdf)

### Explanation about the results (using the images supplied)
#### EXIF tags
EXIF information gets stripped out by some applications, such as Slack, and some images downloaded from, the web also are missing them. 

The first image I tested was made in the office with my Samsung Galaxy (Android) phone with the location tagging disabled.

Sending the image via email, I managed to retain the tags and the application picked them up.
```json
{"Exif": {"Make": "samsung", "Model": "SM-G930F"}}
```
_NOTE: to see all the tags just take out the tags from the method parameter [here](https://github.com/gberdal/rekognition/blob/master/start.py#L88)._

#### Object/Theme Recognition
The AWS Rekognition service has a well trained model for recognising objects and themes of images. It can even tell the difference
between genders, a swimsuit and a bikini, or whether a building is a residential or office building.

#### Image Moderation
Using the examples above, the API will flag up the picture with the bikini as `Suggestive` and recognising that it belongs to a category
of `Female Swimwear Or Underwear`.

#### Weaknesses
- face labeling often misses the `mustache` but detects `beard` very well, depending on the lighting conditions.
- It seems to miss obvious gestures such as a "middle-finger" on an image that I had taken of myself.

