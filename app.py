from flask import Flask, jsonify, request
import os
# import numpy as np
import sys
import matplotlib.image as mpimg
import requests
from PIL import Image

app = Flask(__name__)

temp_images_path = 'temp_images/'
temp_images_name = 'temp_image.jpg'


@app.route('/getCarPlate', methods=['GET'])
def get():
    try:
        url = request.args.get('url')
        if url is not None:
            plate = get_number_by_photo_url(url)
            delete_image(temp_images_path+temp_images_name)
            if len(plate) > 0:
                return jsonify({'data': plate})
            else:
                return jsonify({'error': "no car plate on photo"})
        else:
            return jsonify({'error': "specify the 'url' argument"})

    except:
        e = sys.exc_info()[0]
        return jsonify({'error': e})


def get_number_by_photo_url(url):
    download_image(url)
    # change this property
    NOMEROFF_NET_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '/')

    # specify the path to Mask_RCNN if you placed it outside Nomeroff-net project
    MASK_RCNN_DIR = os.path.join(NOMEROFF_NET_DIR, 'Mask_RCNN')
    MASK_RCNN_LOG_DIR = os.path.join(NOMEROFF_NET_DIR, 'logs')

    sys.path.append(NOMEROFF_NET_DIR)

    # Import license plate recognition tools.
    from NomeroffNet import filters, RectDetector, TextDetector, OptionsDetector, Detector, textPostprocessing, \
        textPostprocessingAsync

    # Initialize npdetector with default configuration file.
    nnet = Detector(MASK_RCNN_DIR, MASK_RCNN_LOG_DIR)
    nnet.loadModel("latest")

    rectDetector = RectDetector()

    optionsDetector = OptionsDetector()
    optionsDetector.load("latest")

    # Initialize text detector.
    textDetector = TextDetector.get_static_module("ru")()
    textDetector.load("latest")

    # Detect numberplate
    print("START RECOGNIZING")
    img_path = temp_images_path + temp_images_name

    img = mpimg.imread(img_path)
    NP = nnet.detect([img])

    # Generate image mask.
    cv_img_masks = filters.cv_img_mask(NP)

    # Detect points.
    arrPoints = rectDetector.detect(cv_img_masks)
    zones = rectDetector.get_cv_zonesBGR(img, arrPoints)

    # find standart
    regionIds, stateIds, countLines = optionsDetector.predict(zones)
    regionNames = optionsDetector.getRegionLabels(regionIds)

    # find text with postprocessing by standart
    textArr = textDetector.predict(zones)
    textArr = textPostprocessing(textArr, regionNames)
    return textArr[0]


def download_image(url):
    img_data = requests.get(url).content
    f_ext = os.path.splitext(url)[-1]

    with open(temp_images_path + temp_images_name, 'wb') as handler:
        handler.write(img_data)


def delete_image(path):
    if os.path.exists("demofile.txt"):
        os.remove(path)


if (__name__) == '__main__':
    app.run(debug=False)
