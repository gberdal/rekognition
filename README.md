## Rekognition
A prototype Python application for testing AWS Rekognition on localhost.

### Install
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
NOTE: The folder already contains a few images sourced from [Google Open Images](https://storage.googleapis.com/openimages/web/download.html). If you need more free images you can find quite a few more there.

For more information about AWS Rekognition read the [Developer Guide](https://docs.aws.amazon.com/rekognition/latest/dg/rekognition-dg.pdf)

### Configuration
In order to access the service you'd need to configure your credentials following this [document](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).


### Explanation about the results
Using various images (not necesserily the ones supplied in the repo) I could identofy some areas where the serrvice performs well, and some where it does not so well.

#### EXIF tags (THIS IS NOT PART OF AWS REKOGNITION)
Although not part of AWS Rekognition, I thought it might be useful to know what information images might be carrying themselves that could be used for evaluation. For example size of resolution.

EXIF information gets stripped out by some applications, such as Slack, and some images downloaded from, the web also are missing them. 

The first image I tested was made in the office with my Samsung Galaxy (Android) phone with the location tagging disabled.

Sending the image via email, I've managed to make it retain the tags and the application picked them up sucessfully.
```json
{"Exif": {"Make": "samsung", "Model": "SM-G930F"}}
```
_NOTE: to see all the tags just take out the tags from the method parameter [here](https://github.com/gberdal/rekognition/blob/master/start.py#L88)._

#### Object/Theme Recognition
The AWS Rekognition service has a well trained model for recognising objects and themes of images. It can even tell the difference
between genders, a swimsuit and a bikini, or whether a building is a residential or office building.

#### Image Moderation
The API flags up the picture of a person wearing a bikini as `Suggestive`, assiggns it to a category
of `Female Swimwear Or Underwear`. It will also flag up images of surgery as `Gore`, or disfigured bodies as `Visually Disturbing`, so as pictures of guns as `Weapons`.

#### Weaknesses
- face labeling often misses the `mustache` but detects `beard` very well, depending on the lighting conditions.
- it misses labels that you'd think should be there, such as the colour `black` on a picture of a black car, or an Arab delegation wearing `ghutra`s.
- It seems to miss obvious gestures, such as a "middle-finger", on images.
- Weaponry sometimes recognised as a label but called out in the moderation. E.g. a tray of cakes with a knife and a blood splatter over them does not trigger the moderation flags, but a picture of an AK47 does.
- Rekognition is able to spot the innocent nature of a stage performance where men hold guns to a woman's head, on the other hand does not recognise the violence on an obvious war scene with smoke and vehicles being on fire, etc.
