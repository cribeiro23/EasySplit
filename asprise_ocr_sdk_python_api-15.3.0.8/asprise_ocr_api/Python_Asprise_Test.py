# Author: Carlos Eduardo Matos Ribeiro
# Version 1.0
# Last edited: 28/08/2017
#
# Function to take user selected image and perform OCR on it,
# using the Asprise api free-trial

from asprise_ocr_api import *

def doOcr():
    ocr = Ocr()
    ocr.start_engine("por")  # deu, fra, por, spa
                             #- more than 30 languages are supported

    path = input("Insert path of image to be read: ")

    text = ocr.recognize(
        path,  # gif, jpg, pdf, png, tif, etc.
        OCR_PAGES_ALL,  # the index of the selected page
        -1, -1, -1, -1,  # you may optionally specify a region on the page instead of the whole page
        OCR_RECOGNIZE_TYPE_TEXT,  # recognize type: TEXT, BARCODES or ALL
        OCR_OUTPUT_FORMAT_PLAINTEXT  # output format: TEXT, XML, or PDF
      )

    # ocr.recognize(more_images...)

    ocr.stop_engine()

    return text

