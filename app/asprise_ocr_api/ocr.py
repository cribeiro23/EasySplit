"""Asprise OCR API for Python: core classes and functions.

Read <a href="http://asprise.com/ocr/docs/html/?src=python">developer's guide to Python OCR SDK API</a>.

Using this file with or without modification in close source and/or commercial applications is strictly
prohibited unless you have obtained written approval from Asprise.
<a href="http://asprise.com/royalty-free-library/python-ocr-sdk-asprise_ocr_api-overview.html">Asprise OCR SDK Python API</a>
"""

__author__ = "Asprise OCR (support@asprise.com)"
__copyright__ = "Copyright (C) 1997-2015 Asprise"

import sys
import platform
import os
import ctypes
import time
from datetime import datetime
import threading
import tempfile

_OCR_WIN_DLL_NAME_32 = "aocr.dll";
_OCR_WIN_DLL_NAME_64 = "aocr_x64.dll";
_OCR_LINUX_SO_NAME_32 = "libaocr.so"
_OCR_LINUX_SO_NAME_64 = "libaocr_x64.so"
_OCR_MAC_DYLIB_NAME_64 = "libaocr_x64.dylib"

_CONFIG_PROP_SEPARATOR = "|";
_CONFIG_PROP_KEY_VALUE_SEPARATOR = "=";

OCR_PAGES_ALL = -1

UTF_8 = "utf-8"

# Property configure constants
OCR_SPEED_FASTEST = "fastest"
OCR_SPEED_FAST = "fast"
OCR_SPEED_SLOW = "slow"

LANGUAGE_ENG = "eng"
LANGUAGE_SPA = "spa"
LANGUAGE_POR = "por"
LANGUAGE_DEU = "deu"
LANGUAGE_FRA = "fra"

START_PROP_DICT_SKIP_BUILT_IN_DEFAULT = "START_PROP_DICT_SKIP_BUILT_IN_DEFAULT"
START_PROP_DICT_SKIP_BUILT_IN_ALL = "START_PROP_DICT_SKIP_BUILT_IN_ALL"
START_PROP_DICT_CUSTOM_DICT_FILE = "START_PROP_DICT_CUSTOM_DICT_FILE"
START_PROP_DICT_CUSTOM_TEMPLATES_FILE = "START_PROP_DICT_CUSTOM_TEMPLATES_FILE"
PROP_DICT_DICT_IMPORTANCE = "PROP_DICT_DICT_IMPORTANCE"

OCR_RECOGNIZE_TYPE_TEXT = "text"
OCR_RECOGNIZE_TYPE_BARCODE = "barcode"
OCR_RECOGNIZE_TYPE_ALL = "all"

OCR_OUTPUT_FORMAT_PLAINTEXT = "text"
OCR_OUTPUT_FORMAT_XML = "xml"
OCR_OUTPUT_FORMAT_PDF = "pdf"
OCR_OUTPUT_FORMAT_RTF = "rtf"

PROP_PAGE_TYPE = "PROP_PAGE_TYPE"
PROP_PAGE_TYPE_AUTO_DETECT = "auto"
PROP_PAGE_TYPE_SINGLE_BLOCK = "single_block"
PROP_PAGE_TYPE_SINGLE_COLUMN = "single_column"
PROP_PAGE_TYPE_SINGLE_LINE = "single_line"
PROP_PAGE_TYPE_SINGLE_WORD = "single_word"
PROP_PAGE_TYPE_SINGLE_CHARACTOR = "single_char"
PROP_PAGE_TYPE_SCATTERED = "scattered"

PROP_LIMIT_TO_CHARSET = "PROP_LIMIT_TO_CHARSET"
PROP_OUTPUT_SEPARATE_WORDS = "PROP_OUTPUT_SEPARATE_WORDS"
PROP_INPUT_PDF_DPI = "PROP_INPUT_PDF_DPI"

# -------- PDF output specific ---------
PROP_PDF_OUTPUT_FILE = "PROP_PDF_OUTPUT_FILE"
PROP_PDF_OUTPUT_IMAGE_DPI = "PROP_PDF_OUTPUT_IMAGE_DPI"
PROP_PDF_OUTPUT_FONT = "PROP_PDF_OUTPUT_FONT"
PROP_PDF_OUTPUT_TEXT_VISIBLE = "PROP_PDF_OUTPUT_TEXT_VISIBLE"
PROP_PDF_OUTPUT_IMAGE_FORCE_BW = "PROP_PDF_OUTPUT_IMAGE_FORCE_BW"

PROP_PDF_OUTPUT_CONF_THRESHOLD = "PROP_PDF_OUTPUT_CONF_THRESHOLD"
PROP_PDF_OUTPUT_RETURN_TEXT = "PROP_PDF_OUTPUT_RETURN_TEXT"

# -------- RTF output specific ---------
PROP_RTF_OUTPUT_FILE = "PROP_RTF_OUTPUT_FILE"
PROP_RTF_PAPER_SIZE = "PROP_RTF_PAPER_SIZE"
PROP_RTF_OUTPUT_RETURN_TEXT = "PROP_RTF_OUTPUT_RETURN_TEXT"

# -------- image processing related ---------

# Image pre-processing type
PROP_IMG_PREPROCESS_TYPE = "PROP_IMG_PREPROCESS_TYPE"
PROP_IMG_PREPROCESS_TYPE_DEFAULT = "default"
PROP_IMG_PREPROCESS_TYPE_DEFAULT_WITH_ORIENTATION_DETECTION = "default_with_orientation_detection"
PROP_IMG_PREPROCESS_TYPE_CUSTOM = "custom"

# Image pre-processing command
PROP_IMG_PREPROCESS_CUSTOM_CMDS = "PROP_IMG_PREPROCESS_CUSTOM_CMDS"

# -------- table related ---------
# table will be detected by default; set this property to true to skip detection. */
PROP_TABLE_SKIP_DETECTION = "PROP_TABLE_SKIP_DETECTION"

# default is 32 if not specified
PROP_TABLE_MIN_SIDE_LENGTH = "PROP_TABLE_MIN_SIDE_LENGTH"

# Save intermediate images generated for debug purpose - don't specify or empty string to skip saving
PROP_SAVE_INTERMEDIATE_IMAGES_TO_DIR = "PROP_SAVE_INTERMEDIATE_IMAGES_TO_DIR"

class Ocr(object):
    """Asprise OCR API"""

    _dynamic_lib = None
    _set_up_done = 0
    _supported_languages = None

    def __init__(self):
        """Default constructor"""

        self._handle = 0
        """native handle"""
        self.language = None
        """The language supported if the engine is running"""
        self._currentThread = None
        """Current owning thread"""

        self.start_props = None
        """Start props (dict)"""

    @staticmethod
    def set_up():
        """Performs one-time setup; does nothing if setup has already been done."""
        if Ocr._set_up_done == 1: # skip if setup is done.
            return
        res = Ocr._do_set_up(0)
        if res == 1:
            Ocr._set_up_done = 1
        else:
            raise RuntimeError("Failed to set up OCR. Error code: " + res + ". Please contact support@asprise.com for help.")
        return

    @staticmethod
    def get_version():
        """The library version."""
        Ocr._load_dynamic_lib()
        func = Ocr._dynamic_lib.com_asprise_ocr_version
        assert isinstance(func, ctypes._CFuncPtr)
        func.argtypes = []
        func.restype = ctypes.c_char_p
        func_return = func()
        return '' if func_return is None else func_return.decode(UTF_8)

    @staticmethod
    def list_supported_languages():
        """ :return: all supported languages. """
        if Ocr._supported_languages is not None:
            return Ocr._supported_languages
        Ocr.set_up()
        func = Ocr._dynamic_lib.com_asprise_ocr_list_supported_langs
        assert isinstance(func, ctypes._CFuncPtr)
        func.argtypes = []
        func.restype = ctypes.c_char_p
        func_return = func()
        func_return = '' if func_return is None else func_return.decode(UTF_8)
        Ocr._supported_languages = sorted(func_return.split(','))
        return Ocr._supported_languages

    def start_engine(self, lang, **kwargs):
        """Starts the OCR Engine.
        :param lang: OCR language, e.g., 'eng', 'fra', 'deu', etc.
        """
        global _CONFIG_PROP_SEPARATOR, _CONFIG_PROP_KEY_VALUE_SEPARATOR, UTF_8
        if lang not in Ocr.list_supported_languages():
            raise RuntimeError(lang + " is not in supported languages: " + Ocr.list_supported_languages())
        func = Ocr._dynamic_lib.com_asprise_ocr_start
        assert isinstance(func, ctypes._CFuncPtr)
        func.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        func.restype = ctypes.c_int64
        self._handle = func(lang.encode(UTF_8), OCR_SPEED_FASTEST.encode(UTF_8),
                            self.dictToString(kwargs).encode(UTF_8),
                            _CONFIG_PROP_SEPARATOR.encode(UTF_8), _CONFIG_PROP_KEY_VALUE_SEPARATOR.encode(UTF_8))
        if self._handle == 0:
            raise RuntimeError("Failed to start OCR engine. ")
        self.language = lang
        self.start_props = kwargs
        return

    def is_engine_running(self):
        return self._handle > 0

    def stop_engine(self):
        """Stops the OCR Engine"""
        if not self.is_engine_running():
            return
        func = Ocr._dynamic_lib.com_asprise_ocr_stop
        assert isinstance(func, ctypes._CFuncPtr)
        func.argtypes = [ctypes.c_int64]
        func.restype = None
        func(self._handle)
        return

    def recognize(self, img_files, page_index, start_x, start_y, width, height, recognize_type, output_format, **kwargs):
        global _CONFIG_PROP_SEPARATOR, _CONFIG_PROP_KEY_VALUE_SEPARATOR, UTF_8
        global OCR_OUTPUT_FORMAT_PDF, OCR_OUTPUT_FORMAT_PLAINTEXT, OCR_OUTPUT_FORMAT_XML, OCR_OUTPUT_FORMAT_RTF, OCR_PAGES_ALL
        global OCR_RECOGNIZE_TYPE_ALL, OCR_RECOGNIZE_TYPE_BARCODE, OCR_RECOGNIZE_TYPE_BARCODE
        global PROP_PDF_OUTPUT_FILE, PROP_OUTPUT_SEPARATE_WORDS, PROP_RTF_OUTPUT_FILE
        if self._currentThread is not None:
            raise RuntimeError("Another thread is using the OCR engine. Please create multiple OCR engine instances for multi-threading.");

        # validations
        if not img_files:
            raise ValueError("Input image files can not be empty")

        # process properties
        for key, value in kwargs.items():
            if key is None or value is None:
                raise ValueError("Neither key or value can be None")

        if output_format == OCR_OUTPUT_FORMAT_PDF:
            if not kwargs.get(PROP_PDF_OUTPUT_FILE):
                raise ValueError("You must specify PROP_PDF_OUTPUT_FILE when output format is PDF")
            if kwargs.get(PROP_OUTPUT_SEPARATE_WORDS) is None: # if not specified, we set default to separate words
                kwargs[PROP_OUTPUT_SEPARATE_WORDS] = True

        if output_format == OCR_OUTPUT_FORMAT_RTF:
            if not kwargs.get(PROP_RTF_OUTPUT_FILE):
                raise ValueError("You must specify PROP_RTF_OUTPUT_FILE when output format is RTF")

        properties_string = self.dictToString(kwargs)

        try:
            self._currentThread = threading.currentThread()
            func = Ocr._dynamic_lib.com_asprise_ocr_recognize
            assert isinstance(func, ctypes._CFuncPtr)
            func.argtypes = [ctypes.c_int64,
                             ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
                             ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
            func.restype = ctypes.c_char_p
            result_bytes = func(self._handle,
                     img_files.encode(UTF_8), page_index, start_x, start_y, width, height,
                     recognize_type.encode(UTF_8), output_format.encode(UTF_8), properties_string.encode(UTF_8), _CONFIG_PROP_SEPARATOR.encode(UTF_8), _CONFIG_PROP_KEY_VALUE_SEPARATOR.encode(UTF_8))

            result_string = None if result_bytes is None else result_bytes.decode(UTF_8)
            return result_string
        except Exception as oe:
            raise oe  #re-raise
        finally:
            self._currentThread = None

    @staticmethod
    def _do_set_up(query_only):
        """
        :return: int 0 if setup required; 1 if setup has been done; or negative error code.
        """
        Ocr._load_dynamic_lib()
        func = Ocr._dynamic_lib.com_asprise_ocr_setup
        assert isinstance(func, ctypes._CFuncPtr)
        func.argtypes = [ctypes.c_int] # bool queryOnly
        func.restype = ctypes.c_int
        return func(query_only)

    @staticmethod
    def input_license(licenseeName, licenseCode):
        Ocr._load_dynamic_lib()
        func = Ocr._dynamic_lib.com_asprise_ocr_input_license
        assert isinstance(func, ctypes._CFuncPtr)
        func.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        func.restype = None
        func(licenseeName, licenseCode)
        return

    @staticmethod
    def delete_object(handle, is_array):
        Ocr._load_dynamic_lib()
        func = Ocr._dynamic_lib.com_asprise_ocr_util_delete
        assert isinstance(func, ctypes._CFuncPtr)
        func.argtypes = [ctypes.c_int64, ctypes.c_bool]
        func.restype = None
        func(handle, is_array)
        return

    @staticmethod
    def _load_dynamic_lib():
        """Loads dynamic library if it has not been loaded. Skip if already loaded."""
        if Ocr._dynamic_lib is not None:
            return
        lib_file = Ocr.find_dynamic_lib_file()
        if lib_file is None:
            raise LibraryNotFoundException('Dynamic library not found: ' + Ocr._get_dynmaic_lib_file_name() + ". Please download it and put to your PATH. \nAlternatively, you may contact support@asprise.com for assistance.")

        if Ocr.is_windows():
            Ocr._dynamic_lib = ctypes.windll.LoadLibrary(lib_file)
        else:
            Ocr._dynamic_lib = ctypes.cdll.LoadLibrary(lib_file)
        return

    @staticmethod
    def unload_lib():
        try:
            lib_handle = Ocr._dynamic_lib
            Ocr._dynamic_lib = None  # remove reference
            if Ocr.is_windows():
                ctypes.windll.kernel32.FreeLibrary.argtypes = [ctypes.c_int64 if Ocr.is_64_bit() else ctypes.c_int32]
                ctypes.windll.kernel32.FreeLibrary(lib_handle._handle)
            else:
                pass
        except Exception as e:
            print(e)

    @staticmethod
    def find_dynamic_lib_file():
        dll_name = Ocr._get_dynmaic_lib_file_name()
        paths = []

        # 1. First, current dir and all of its ancestors to path
        p = os.path.abspath(os.curdir)
        while os.path.isdir(p):
            paths.append(p)
            parent = os.path.abspath(os.path.join(p, os.pardir))
            if p == parent:
                break
            else:
                p = parent

        # lib
        lib_location = get_asprise_ocr_root_with_trailing_slash() + "asprise_ocr_api" + os.sep + "lib"
        paths.append(lib_location)

        # PYTHONPATH
        paths += sys.path # Python paths

        # System PATH
        paths += os.environ['PATH'].split(os.pathsep) # Windows %PATH% or Linux $PATH

        # print(paths)
        for path in paths:
            path = os.path.abspath(path)
            dll_file = suffix_with_trailing_slash(path) + dll_name
            # print(dll_file)
            if os.path.isfile(dll_file):
                print("library: " + dll_file)
                return dll_file

        return None
    # end of find_dynamic_lib_file

    @staticmethod
    def dictToString(d, propSep=_CONFIG_PROP_SEPARATOR, keyValueSep=_CONFIG_PROP_KEY_VALUE_SEPARATOR):
        global _CONFIG_PROP_SEPARATOR, _CONFIG_PROP_KEY_VALUE_SEPARATOR
        if not isinstance(d, dict):
            return ""
        return propSep.join(
            ['%s%s%s' % (key, keyValueSep,
                         str(value).lower() if value is True or value is False else value) for (key, value) in d.items()])

    @staticmethod
    def stringToDict(s, propSep=_CONFIG_PROP_SEPARATOR, keyValueSep=_CONFIG_PROP_KEY_VALUE_SEPARATOR):
        global _CONFIG_PROP_SEPARATOR, _CONFIG_PROP_KEY_VALUE_SEPARATOR
        dict = {}
        if not s:
            return dict
        s = str(s)
        props = s.split(propSep)
        for prop in props:
            parts = prop.split(keyValueSep)
            if parts and len(parts) >= 2 and parts[0]:
                dict[parts[0]] = parts[1]
        return dict

    @staticmethod
    def combineDict(dictBase, dictUpdate):
        d = dictBase.copy()
        d.update(dictUpdate)
        return d

    @staticmethod
    def is_64_bit():
        return ' '.join(platform.architecture()).find("64") >= 0

    @staticmethod
    def is_windows():
        return sys.platform.lower().find('darwin') < 0 and sys.platform.lower().find("win") >= 0

    @staticmethod
    def is_linux():
        return sys.platform.lower().find('linux') >= 0

    @staticmethod
    def is_mac():
        return sys.platform.lower().find('darwin') >= 0 or sys.platform.lower().find('mac') >= 0

    @staticmethod
    def _get_dynmaic_lib_file_name():
        global _OCR_WIN_DLL_NAME_32, _OCR_WIN_DLL_NAME_64, _OCR_LINUX_SO_NAME_32, _OCR_LINUX_SO_NAME_64, _OCR_MAC_DYLIB_NAME_64
        if Ocr.is_windows():
            return _OCR_WIN_DLL_NAME_64 if Ocr.is_64_bit() else _OCR_WIN_DLL_NAME_32
        if Ocr.is_linux():
            return _OCR_LINUX_SO_NAME_64 if Ocr.is_64_bit() else _OCR_LINUX_SO_NAME_32
        if Ocr.is_mac():
            return _OCR_MAC_DYLIB_NAME_64
        raise RuntimeError("Unsupported OS: " + ' '.join(platform.architecture()))

    @staticmethod
    def get_time_tick():
        if sys.platform == 'win32':
            return time.clock()   # On Windows, the best timer is time.clock
        else:
            return time.time()    # On most other platforms the best timer is time.time


class LibraryNotFoundException(Exception):
    pass


# Util funcs
def suffix_with_trailing_slash(path):
    if path.endswith('/') or path.endswith('\\'):
        return path
    else:
        return path + os.path.sep

def get_asprise_ocr_root_with_trailing_slash():
    p = os.path.dirname(os.path.abspath(__file__))
    p = os.path.dirname(p)
    assert isinstance(p, str)
    return suffix_with_trailing_slash(p)

def get_current_dir_with_trailing_slash():
    p = os.getcwd()
    return suffix_with_trailing_slash(p)

def get_writable_dir_with_trailing_slash():
    return suffix_with_trailing_slash(tempfile.gettempdir())

def get_date_time_stamp():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S_%f")

def get_system_info():
    return "Python {0} {1} on {2}".format(sys.version, "x64" if Ocr.is_64_bit() else "x86", sys.platform)