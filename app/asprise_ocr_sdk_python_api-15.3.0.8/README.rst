
Asprise OCR SDK with Data Capture - the Ultimate Royalty Free OCR Engine
========================================================================

.. image:: https://badge.fury.io/py/asprise_ocr_sdk_python_api.png
    :target: http://asprise.com/royalty-free-library/python-ocr-sdk-asprise_ocr_api-overview.html
    :alt: Latest version

.. image:: https://pypip.in/d/asprise_ocr_sdk_python_api/badge.png
    :target: https://pypi.python.org/pypi/asprise_ocr_sdk_python_api
    :alt: Number of PyPI downloads


Install and Run the Sample OCR Application
------------------------------------------

You may install with Python's pip either from a Unix/Linux shell or Windows command console: ::

    > pip install asprise_ocr_sdk_python_api       # Windows

    $ sudo pip install asprise_ocr_sdk_python_api  # Linux/Mac OS X

A sample front-end GUI for the OCR engine will be installed as a script named 'asprise_ocr'.
You can run the following command in the same shell/console: ::

    asprise_ocr

The following are the screenshots on Linux and Windows respectively:

.. image:: http://asprise.com/ocr/img/screenshots/python-linux-thumb.png
    :target: http://asprise.com/ocr/img/screenshots/python-linux.png
    :alt: Asprise OCR for Python on Linux

.. image:: http://asprise.com/ocr/img/screenshots/python-win-thumb.png
    :target: http://asprise.com/ocr/img/screenshots/python-win.png
    :alt: Asprise OCR for Python on Windows


Invoke Asprise OCR API from Your Own Code
-----------------------------------------

.. code-block:: python

    from asprise_ocr_api import *

    ocr = Ocr()
    ocr.start_engine("eng")  # deu, fra, por, spa - more than 30 languages are supported
    text = ocr.recognize(
        "PATH_TO_INPUT_IMAGE.tif",  # gif, jpg, pdf, png, tif, etc.
        OCR_PAGES_ALL,  # the index of the selected page
        -1, -1, -1, -1,  # you may optionally specify a region on the page instead of the whole page
        OCR_RECOGNIZE_TYPE_TEXT,  # recognize type: TEXT, BARCODES or ALL
        OCR_OUTPUT_FORMAT_PLAINTEXT  # output format: TEXT, XML, or PDF
    )
    print "Result: " + text

    # ocr.recognize(more_images...)

    ocr.stop_engine()


Asprise OCR Programming Guide
-----------------------------

Developer's Guide: http://asprise.com/royalty-free-library/python-ocr-barcode-reader-sdk-samples-docs.html

We'd Like to Hear From You
--------------------------

Asprise OCR supports more than twenty languages, however only five popular languages are included
in this trial kit. Please contact us if you need to evaluate other languages.

Email: contact@asprise.com
Homepage: `Python OCR SDK API on asprise.com <http://asprise.com/royalty-free-library/python-ocr-sdk-asprise_ocr_api-overview.html>`_
