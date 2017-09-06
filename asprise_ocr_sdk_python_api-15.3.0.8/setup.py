# Ref: https://github.com/pypa/sampleproject/blob/master/setup.py
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='asprise_ocr_sdk_python_api',
    version='15.3.0.8',
    description='Asprise OCR (optical character recognition) and barcode recognition SDK is a high performance '
                'royalty-free Python API library. It converts images (JPEG, PNG, TIFF, PDF, etc) into text, xml, searchable PDF or editable RTF/Word formats. '
                'Data capture are supported for processing documents like invoices and forms.',
    long_description=long_description,
    keywords='Asprise OCR SDK Image Convert Text Searchable PDF Barcode Recognition Invoice Form OMR',
    license='ASPRISE OCR SDK LICENSE',
    author='Asprise OCR',
    author_email='ocr-sdk@asprise.com',
    maintainer='Asprise OCR',
    maintainer_email='support@asprise.com',
    url='http://asprise.com/royalty-free-library/python-ocr-sdk-asprise_ocr_api-overview.html',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: Other Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: Freely Distributable',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Natural Language :: French',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Java',
        'Programming Language :: Python',
        'Topic :: Office/Business',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities'
    ],
    packages=[
        'asprise_ocr_api'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'asprise_ocr=asprise_ocr_api.ocr_app:run_ocr_app',
        ],
    },
)