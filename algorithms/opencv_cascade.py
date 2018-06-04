import numpy as np
import cv2
import argparse
from imutils import paths
import imutils
from imutils.object_detection import non_max_suppression


def run_cascade_algorithm(img_paths):
    # body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    # body_cascade = cv2.CascadeClassifier('haarcascade_lowerbody.xml')
    # body_cascade = cv2.CascadeClassifier('haarcascade_upperbody.xml')
    body_cascade = cv2.CascadeClassifier()
    # body_cascade.load('rand_cascade.xml')
    body_cascade.load('cascades/rand_cascade_people.xml')

    # loop over the image paths
    num_people = []

    for imagePath in paths.list_images(img_paths):
        # load the image and resize it to (1) reduce detection time
        # and (2) improve detection accuracy
        image = cv2.imread(imagePath)
        image = imutils.resize(image, width=900)
        orig = image.copy()

        gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        people = body_cascade.detectMultiScale(gray, 1.03, 6)

        for (x,y,w,h) in people:
            cv2.rectangle(image, (x,y), (x + w, y + h), (255,255,0), 2)

        num_people.append(len(people))
        cv2.imwrite('/'.join(imagePath.split('/')[:-1]) + '/pred_' + imagePath.split('/')[-1], image)
        
        # cv2.imshow('img', image)
        # cv2.waitKey(0)
    return num_people


if __name__ == "__main__":
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images", required=True, help="path to images directory")
    args = vars(ap.parse_args())
    run_cascade_algorithm(args)