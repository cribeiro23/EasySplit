"""Asprise OCR API for Python: sample GUI application.

Read <a href="http://asprise.com/ocr/docs/html/?src=python">developer's guide to Python OCR SDK API</a>.

Using this file with or without modification in close source and/or commercial applications is strictly
prohibited unless you have obtained written approval from Asprise.
<a href="http://asprise.com/royalty-free-library/python-ocr-sdk-asprise_ocr_api-overview.html">Asprise OCR SDK Python API</a>
"""

__author__ = "Asprise OCR (support@asprise.com)"
__copyright__ = "Copyright (C) 1997-2015 Asprise"

try:
    from Tkinter import *
except ImportError:
    try:
        from tkinter.ttk import *
    except:
        try:
            from ttk import *
        except:
            raise RuntimeError("TK is required to run this application. Please install python tk.")

try:
    from tkFileDialog import *
except ImportError:
    from tkinter.filedialog import *

# try: # Combobox is not available on some platforms
#     from ttk import Combobox
# except ImportError:
#     from tkinter.ttk import Combobox

try:
    import tkMessageBox
except ImportError:
    import tkinter.messagebox as tkMessageBox

from time import sleep
from datetime import datetime

import sys
import os
import shutil

import threading
import webbrowser

# for lib downloading
try:
    from urllib2 import HTTPError
except ImportError:
    from urllib.error import HTTPError

try:
    from urllib import urlopen, urlretrieve
except ImportError:
    from urllib.request import urlopen, urlretrieve

import hashlib

try:
    import httplib
except ImportError:
    import http.client as httplib

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

import tempfile

try:
    import Queue as queue
except ImportError:
    import queue as queue

from ocr import *

class WorkerThread(threading.Thread):
    def __init__(self, thread_name, task_done_callback=None):
        threading.Thread.__init__(self)
        self.name = thread_name
        self.task_done_callback = task_done_callback
        self._queue = queue.Queue()
        self._running_task = False
        self.stopped = False

    def run(self):
        while not self.stopped:
            task = None
            task_return = None
            exception_raised = None
            try:
                if self._queue.empty():
                    time.sleep(0.1)
                    continue
                task = self._queue.get(False)  # non-blocking
                if task:
                    self._running_task = True
                    try:
                        task_return = task()
                    except Exception as te:
                        exception_raised = te
                    finally:
                        self._running_task = False
                        try:
                            if self.task_done_callback:
                                self.task_done_callback(task, task_return, exception_raised)
                        except Exception as ce:
                            print(ce)
            except Exception as qe:
                print(qe)


    def enqueue_task(self, task_func):
        self._queue.put_nowait(task_func)

    def shutdown(self):
        """Shutdown gracefully"""
        self.stopped = True

    def is_busy(self):
        return self._queue.qsize() > 0 or self._running_task


def open_file_in_browser(file_path):
    """
    :type file_path str
    :return:
    """
    if not file_path:
        return
    url = "file://" + file_path.replace("\\", "/")
    webbrowser.open(url)
    return

def open_file_with_default_program(file_path):
    if Ocr.is_windows():
        os.startfile(file_path, 'open')
    elif Ocr.is_mac():
        os.system('open ' + file_path)
    elif Ocr.is_linux():
        os.system('xdg-open ' + file_path)
    else:
        os.system(file_path)
    return

class OcrRecognizeRequest:
    def __init__(self, props_start, props_recognize, img_files, recognize_type, output_format, demo_mode, **kwargs):
        """
        @type img_files: str
        """
        if img_files.find(',') < 0 and not os.path.isfile(img_files.strip()):
            raise ValueError("File doesn't exist: {0}".format(img_files))

        self.props_start = props_start
        self.props_recognize = props_recognize
        self.img_files = img_files
        self.recognize_type = recognize_type
        self.output_format = output_format
        self.demo_mode = demo_mode
        self.options = kwargs
        self.recognized = False
        self.recognize_result = None
        self.recognize_output_file = None
        self.recognize_exception = None

        if self.output_format == OCR_OUTPUT_FORMAT_PDF:
            if PROP_PDF_OUTPUT_TEXT_VISIBLE not in self.options.keys():
                self.options[PROP_PDF_OUTPUT_TEXT_VISIBLE] = True
            if PROP_PDF_OUTPUT_FILE not in self.options.keys():
                self.options[PROP_PDF_OUTPUT_FILE] = get_writable_dir_with_trailing_slash() + get_date_time_stamp() + ".pdf"
            if PROP_PDF_OUTPUT_IMAGE_FORCE_BW not in self.options.keys():
                self.options[PROP_PDF_OUTPUT_IMAGE_FORCE_BW] = True

        if self.output_format == OCR_OUTPUT_FORMAT_RTF:
            if PROP_RTF_OUTPUT_FILE not in self.options.keys():
                self.options[PROP_RTF_OUTPUT_FILE] = get_writable_dir_with_trailing_slash() + get_date_time_stamp() + ".rtf"

        # props
        self.options = Ocr.combineDict(self.options, Ocr.stringToDict(props_recognize));

    def __str__(self):
        return "Recognize {1} to output as {2} format on image {0} ...\nOCR engine start props: {3}\nOCR recognition props:  {4}".format(
            self.img_files, self.recognize_type, self.output_format, self.props_start, Ocr.dictToString(self.options))

    def recognize(self, ocr):
        """
        Performs OCR on the given ocr engine; sets recognized, recognize_result, recognize_exception after done.
        :type ocr: Ocr
        :return:
        """
        try:
            self.recognize_result = ocr.recognize(self.img_files, OCR_PAGES_ALL, -1, -1, -1, -1, self.recognize_type, self.output_format, **(self.options))
            try:  # post processing
                if self.recognize_result:
                    pass # self.recognize_result = self.recognize_result.decode('utf-8')
                if self.demo_mode:
                    if self.output_format == OCR_OUTPUT_FORMAT_XML and self.recognize_result:
                        file_xml = get_writable_dir_with_trailing_slash() + get_date_time_stamp() + ".xml"
                        with open(file_xml, "wb") as f:
                            f.write(self.recognize_result.encode("UTF-8"))
                        self.recognize_output_file = file_xml
                        file_xsl_source = get_asprise_ocr_root_with_trailing_slash() + "asprise_ocr_api" + os.sep + "aocr.xsl"
                        file_xsl_target = get_writable_dir_with_trailing_slash() + "aocr.xsl"
                        if os.path.isfile(file_xsl_source) and not os.path.isfile(file_xsl_target):
                            shutil.copyfile(file_xsl_source, file_xsl_target)
                        open_file_in_browser(file_xml)

                    elif self.output_format == OCR_OUTPUT_FORMAT_PDF:
                        file_pdf = None if PROP_PDF_OUTPUT_FILE not in self.options.keys() else self.options[PROP_PDF_OUTPUT_FILE]
                        self.recognize_output_file = file_pdf
                        if os.path.isfile(file_pdf):
                            open_file_with_default_program(file_pdf)

                    elif self.output_format == OCR_OUTPUT_FORMAT_RTF:
                        file_rtf = None if PROP_RTF_OUTPUT_FILE not in self.options.keys() else self.options[PROP_RTF_OUTPUT_FILE]
                        self.recognize_output_file = file_rtf
                        if os.path.isfile(file_rtf):
                            open_file_with_default_program(file_rtf)

            except Exception as pe: # exception in post processing
                print(pe)

        except Exception as e: # exception thrown in OCR recognize
            self.recognize_exception = e
        finally:
            self.recognized = True

class OcrApp(Frame):
    def load_prefs(self):
        try:
            with open (get_writable_dir_with_trailing_slash() + ".ocr-demo-python", "r") as myfile:
                data=myfile.read().replace('\n', '')
            d = Ocr.stringToDict(data, "@@", "==")
            self.props_start_value.set(d.get("props_start_value", ""))
            self.props_recognize_value.set(d.get("props_recognize_value", ""))
            self.img_file_value.set(d.get("img_file_value", ""))
        except Exception as e:
            return

    def save_prefs(self):
        try:
            d = {}
            d["props_start_value"] = self.props_start_value.get()
            d["props_recognize_value"] = self.props_recognize_value.get()
            d["img_file_value"] = self.img_file_value.get()
            with open (get_writable_dir_with_trailing_slash() + ".ocr-demo-python", "w") as prefFile:
                prefFile.write(Ocr.dictToString(d, "@@", "=="))
        except Exception as e:
            return

    def browse_file(self):
        self.fileName = askopenfilename()
        # print "file browsed: " + self.fileName
        if self.fileName:
            self.img_file_value.set(self.fileName)
        return

    def on_ui_changes(self):
        self.check_pdf_highlight['state'] = NORMAL if self.output_format_value.get().lower().find('pdf') >= 0 else DISABLED

    def visit_asprise_web(self, *args):
        webbrowser.open("http://asprise.com/royalty-free-library/python-ocr-sdk-api-overview.html")

    def visit_help_web(self, *args):
        webbrowser.open("http://asprise.com/ocr/docs/html/asprise-ocr-sdk-api-options.html?src=python")

    def createWidgets(self):
        Grid.columnconfigure(self, 0, weight=1)
        Grid.rowconfigure(self, 0, weight=1)

        self.top_frame = Frame(self)
        self.top_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        Grid.columnconfigure(self.top_frame, 0, weight=1)
        Grid.rowconfigure(self.top_frame, 3, weight=1)

        # Line 0
        self.label_language = Label(self.top_frame, text="Language: ")
        self.label_language.grid(row=0, column=0, sticky="e")

        self.language_value = StringVar(value="eng")
        self.combo_language = OptionMenu(self.top_frame, self.language_value, self.language_value.get())
        self.combo_language.grid(row=0, column=1, sticky="w", padx=4)

        self.label_props_start = Label(self.top_frame, text="Engine start props (optional): ")
        self.label_props_start.grid(row=0, column=2, sticky="e")
        self.props_start_value = StringVar()
        self.text_props_start = Entry(self.top_frame, textvariable=self.props_start_value)
        self.text_props_start.grid(row=0, column=3, columnspan=4, sticky="we", padx=4)

        # Line 1
        self.label_img = Label(self.top_frame, text="Image: ")
        self.label_img.grid(row=1, column=0, sticky="e")
        self.img_file_value = StringVar()
        self.text_img_file = Entry(self.top_frame, textvariable=self.img_file_value)
        self.text_img_file.grid(row=1, column=1, columnspan=5, sticky="we", padx=4)
        self.button_browse = Button(self.top_frame, text="...", command=self.browse_file)
        self.button_browse.grid(row=1, column=6, padx=6, sticky="ew")

        # Line 2
        self.label_text_layout = Label(self.top_frame, text="Text Layout: ")
        self.label_text_layout.grid(row=2, column=0, sticky="e")

        self.text_layout_value = StringVar(value="auto")
        self.combo_text_layout = OptionMenu(self.top_frame, self.text_layout_value, "auto", "single_block", "single_column", "single_line", "single_word", "single_char", "scattered")
        self.combo_text_layout.grid(row=2, column=1, sticky="w", padx=4)

        self.data_capture_value = IntVar(value=1)
        self.check_data_capture = Checkbutton(self.top_frame, text="Data Capture (forms & invoices)", variable=self.data_capture_value)
        self.check_data_capture.grid(row=2, column=2, sticky="w", padx=12)

        self.auto_rotate_page_value = IntVar(value=0)
        self.check_auto_rotate_page = Checkbutton(self.top_frame, text="Auto Rotate Pages", variable=self.auto_rotate_page_value)
        self.check_auto_rotate_page.grid(row=2, column=3)

        self.word_level_value = IntVar(value=0)
        self.check_word_level = Checkbutton(self.top_frame, text="Word level (instead of line)", variable=self.word_level_value, width=30)
        self.check_word_level.grid(row=2, column=4, sticky="w")

        # Line 3
        self.label_output_format = Label(self.top_frame, text="Output format:")
        self.label_output_format.grid(row=3, column=0, sticky="e")

        # Line 3 - frame 1
        self.frame_for_radios = Frame(self.top_frame)
        self.frame_for_radios.grid(row=3, column=1, columnspan=2, sticky="w")

        self.output_format_value = StringVar(value="xml")
        count = 0;
        for text, val in [("Plain text", "text"), ("XML", "xml"), ("RTF", "rtf"), ("PDF", "pdf")]:
            b = Radiobutton(self.frame_for_radios, text=text, variable=self.output_format_value, value=val, command=self.on_ui_changes)
            b.grid(row=1, column=count)
            count += 1

        self.pdf_highlight_value = IntVar(value=1)
        self.check_pdf_highlight = Checkbutton(self.frame_for_radios, text="Highlight text in PDF", variable=self.pdf_highlight_value)
        self.check_pdf_highlight.grid(row=1, column=4)

        # Line 3 - frame 2
        self.frame_for_ocr = Frame(self.top_frame)
        self.frame_for_ocr.grid(row=3, column=3, columnspan=3, sticky="w")

        self.label_rec_type = Label(self.frame_for_ocr, text="Recognize: ")
        self.label_rec_type.grid(row=0, column=0, sticky="e")

        self.recognize_type_value = StringVar(value="Text + Barcodes")
        self.combo_recognize_type = OptionMenu(self.frame_for_ocr, self.recognize_type_value, "Text + Barcodes", "Text only", "Barcodes only")
        self.combo_recognize_type.grid(row=0, column=1, sticky="e", padx=10)

        # Line 4
        self.label_props_recognize = Label(self.top_frame, text="Props (optional): ")
        self.label_props_recognize.grid(row=4, column=0, sticky="e")
        self.props_recognize_value = StringVar()
        self.text_props_recognize = Entry(self.top_frame, textvariable=self.props_recognize_value)
        self.text_props_recognize.grid(row=4, column=1, columnspan=4, sticky="we", padx=4)

        self.label_help = Label(self.top_frame, text="Help", fg="#038", cursor="hand2")
        self.label_help.bind("<Button-1>", self.visit_help_web)
        self.label_help.grid(row=4, column=5, padx=2, sticky="w")

        self.button_ocr = Button(self.top_frame, text="OCR", command=self._button_ocr_clicked, bg="#038", fg="#fff", width=12)
        self.button_ocr.grid(row=4, column=6, sticky="we", padx=4)

        # Line 5
        self.frame_for_logging = Frame(self.top_frame)
        self.frame_for_logging.grid(row=5, column=0, columnspan=7, pady=6, padx=6, sticky="nsew")
        Grid.rowconfigure(self.top_frame, 5, weight=1)

        Grid.rowconfigure(self.frame_for_logging, 0, weight=1)
        Grid.columnconfigure(self.frame_for_logging, 0, weight=1)

        self.text_logging = Text(self.frame_for_logging)
        self.text_logging.grid(row=1, column=0, sticky="nsew")
        # Create scrollbars
        self.xscrollbar = Scrollbar(self.frame_for_logging, orient=HORIZONTAL, command=self.text_logging.xview)
        self.xscrollbar.grid(row=2, column=0, columnspan=2, sticky="we")
        self.yscrollbar = Scrollbar(self.frame_for_logging, orient=VERTICAL, command=self.text_logging.yview)
        self.yscrollbar.grid(row=1, column=1, rowspan=2, sticky="ns")

        # Attach canvas to scrollbars
        self.text_logging.configure(xscrollcommand=self.xscrollbar.set)
        self.text_logging.configure(yscrollcommand=self.yscrollbar.set)
        self.text_logging.tag_configure("blue", foreground="blue")
        self.text_logging.tag_configure("red", foreground="red")
        self.text_logging.tag_configure("green", foreground="#009911")
        self.label_link = Label(self.top_frame, text="We'll be glad to provide you any help. Email us at support@asprise.com or visit asprise.com", fg="#038", cursor="hand2")
        self.label_link.bind("<Button-1>", self.visit_asprise_web)
        self.label_link.grid(row=6, column=0, columnspan=7, padx=6, sticky="e")

        self.on_ui_changes()
        # print "UI thread: ",threading.currentThread()

    def _button_ocr_clicked(self):
        self.ocr_request_img_files = self.img_file_value.get()
        if len(self.ocr_request_img_files.strip()) == 0:
            tkMessageBox.showerror("Error", "Please specify an input file first")
            return
        if self.ocr_request_img_files.find(',') < 0 and not os.path.isfile(self.ocr_request_img_files.strip()):
            tkMessageBox.showerror("Error", "File doesn't exist: " + self.ocr_request_img_files)
            return
        if self.ocr_request is not None and not self.ocr_request.recognized: # pending request
            tkMessageBox.showerror("Error", "OCR is in progress, please click the button after it is done.")
            return
        self.ocr_language = self.language_value.get()
        self.ocr_props_start = self.props_start_value.get()
        self.ocr_request = OcrRecognizeRequest(
            self.props_start_value.get().strip(),
            self.props_recognize_value.get().strip(),
            self.img_file_value.get().strip(),
            OCR_RECOGNIZE_TYPE_ALL if self.recognize_type_value.get().lower().find('text') >= 0 and self.recognize_type_value.get().lower().find('barcode') >= 0 else (
                OCR_RECOGNIZE_TYPE_TEXT if self.recognize_type_value.get().lower().find('text') >= 0 else OCR_RECOGNIZE_TYPE_BARCODE),
            OCR_OUTPUT_FORMAT_PLAINTEXT if self.output_format_value.get().lower().find('text') >= 0 else (
                OCR_OUTPUT_FORMAT_PDF if self.output_format_value.get().lower().find('pdf') >= 0 else (
                OCR_OUTPUT_FORMAT_RTF if self.output_format_value.get().lower().find('rtf') >= 0 else OCR_OUTPUT_FORMAT_XML)
            ),
            True,
            PROP_PAGE_TYPE=self.text_layout_value.get(),
            PROP_TABLE_SKIP_DETECTION=(not self.data_capture_value.get()),
            PROP_OUTPUT_SEPARATE_WORDS=self.word_level_value.get() != 0,
            PROP_IMG_PREPROCESS_TYPE=(PROP_IMG_PREPROCESS_TYPE_DEFAULT_WITH_ORIENTATION_DETECTION if self.auto_rotate_page_value.get() else PROP_IMG_PREPROCESS_TYPE_DEFAULT),
            PROP_PDF_OUTPUT_TEXT_VISIBLE=self.pdf_highlight_value.get() != 0
        )
        self.ocr_thread.enqueue_task(self._ocr_recognize)
        self.log(self.ocr_request, False)
        self.log("OCR in progress, please stand by ..." +
                 ("" if Ocr.is_windows() else " Trial version on Unix: q, x, 0, and 9 will be replaced with *"))

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.lib_download_attempt = 0
        self.lib_download_attempts_max = 3
        self.pack(expand=True, fill="both", side=TOP)
        self.createWidgets()
        self.load_prefs()
        self.stopped = False

        try: # center the window
            master.withdraw()
            master.update_idletasks()  # Update "requested size" from geometry manager

            x = (master.winfo_screenwidth() - self.winfo_reqwidth()) / 2
            y = (master.winfo_screenheight() - self.winfo_reqheight()) / 2
            master.geometry("+%d+%d" % (x, y))

            # This seems to draw the window frame immediately, so only call deiconify()
            # after setting correct window position
            master.deiconify()
        except Exception as e:
            print(e)

        self.ocr = None
        """:type: Ocr"""
        self.ocr_thread = WorkerThread('ocr', self._ocr_thread_task_done_callback)
        self.ocr_thread.start()  # start the worker thread
        self.ocr_language = "eng"
        self.ocr_props_start = ""

        self.ocr_request = None
        """:type: OcrRecognizeRequest"""
        self._ui_update_queue = queue.Queue()  # FIFO queue

        self.ocr_thread.enqueue_task(self._ocr_start_engine)

        self.lib_downloader = None
        """:type: OcrLibDownloader"""
        self._last_log_print = None

    def _ocr_thread_task_done_callback(self, task_func=None, task_return=None, exception=None):
        """ this function is executed in ocr thread
        :type exception: Exception
        :return:
        """
        if isinstance(task_return, OcrRecognizeRequest):
            self.log("OCR Finished.")
            if task_return.recognize_output_file:
                if task_return.recognize_output_file.find(".pdf") > 0:
                    self.log("PDF output file: " + task_return.recognize_output_file, True, "green")
                elif task_return.recognize_output_file.find(".rtf") > 0:
                    self.log("View in a word processor: " + task_return.recognize_output_file, True, "green")
                elif task_return.recognize_output_file.find(".xml") > 0:
                    self.log("View in Firefox/IE/Safari: " + task_return.recognize_output_file, True, "green")
            self.log(task_return.recognize_result, True, "blue")
            self.save_prefs()
        elif isinstance(task_return, Ocr):  # ocr engine started
            self.log(Ocr.get_version() + " - OCR engine started.") # + Ocr.get_version())
            self._enqueue_ui_action(self._update_ocr_lang_list_from_ui_thread, Ocr.list_supported_languages())
        if exception:
            if isinstance(exception, LibraryNotFoundException):
                self.ocr_request = None  # clear the request
                self._enqueue_ui_action(self._prompt_library_download_dialog)
            else:
                self.log(exception.__class__.__name__ + ": " + str(exception), True, "red")
        return

    def _ocr_recognize(self):  # to be executed in OCR thread
        #print "_ocr_recognize",threading.currentThread()
        if self.ocr_request is None:
            raise RuntimeError("OCR request is None")
        if self.ocr_request.recognized:
            raise RuntimeError("OCR request has already been processed")
        self._ocr_start_engine()
        self.ocr_request.recognize(self.ocr)
        return self.ocr_request

    def _ocr_start_engine(self):  # to be executed in OCR thread
        """Long running, execute in other thread. Please set self.ocr_language before calling this."""
        if self.ocr is not None:
            if self.ocr.is_engine_running():
                if self.ocr.language == self.ocr_language and \
                        self.ocr.start_props == self.ocr.stringToDict(self.ocr_props_start): # running with the required lang
                    return
                else:
                    self.ocr.stop_engine()
        self.ocr = Ocr()
        d = self.ocr.stringToDict(self.ocr_props_start);
        self.ocr.start_engine(self.ocr_language, **d)
        return self.ocr

    def _ocr_stop_engine(self):  # to be executed in OCR thread
        if self.ocr is not None and self.ocr.is_engine_running():
            self.ocr.stop_engine()
        return

    def shutdown(self):
        self._ocr_stop_engine()
        if self.ocr_thread:
            self.ocr_thread.stopped = True
        self.ocr = None
        self.master.quit()
        #Ocr.unload_lib()

    def log(self, mesg, append=True, color=None, new_line=True):
        """ Thread-safe logging to screen"""
        self._enqueue_ui_action(self._log_from_ui_thread, mesg, append, color, new_line)

    def _log_from_ui_thread(self, mesg, append=True, color=None, new_line=True):
        """ Thread-unsafe: must be called from the main GUI thread """
        if not mesg:
            return
        if append:
            if new_line and "1.0" != self.text_logging.index('end-1c'):  # ref: http://www.tkdocs.com/tutorial/text.html
                self.text_logging.insert(END, "\n")  # new line inserted in there is any existing text
        else:
            self.text_logging.delete(1.0, END)
        if color:
            self.text_logging.insert(END, mesg, (color))
        else:
            self.text_logging.insert(END, mesg)

    def _reset_option_menu(self, option_menu, value_variable, options):
        menu = option_menu["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string, command=lambda value=string: value_variable.set(value))


    def _update_ocr_lang_list_from_ui_thread(self, languages):
        previous_selected = self.language_value.get()
        #self.combo_language['values'] = languages
        self._reset_option_menu(self.combo_language, self.language_value, languages)
        self.language_value.set(previous_selected)

    def _attempt_library_download(self):
        self.lib_download_url_bases = ["http://asprise.com/ocr/files/downloads/latest/lib/", "http://cdn.asprise.com/ocr/files/downloads/latest/lib/"]
        #self.lib_download_url_bases = ["http://asprise.com2/ocr/files/downloads/latest/lib/", "http://asprise.com/ocr/files/downloads/latest/lib/"]
        self.lib_downloader = OcrLibDownloader(self.lib_download_url_bases[self.lib_download_attempt % len(self.lib_download_url_bases)], self._on_lib_download_finish, self._on_lib_download_progress, 2)
        self.lib_download_attempt += 1
        self.lib_downloader.start()

    def _prompt_library_download_dialog(self):
        if tkMessageBox.askokcancel("Easy download", "Data library is missing. Press 'OK' to download it now and start to OCR right away or 'Cancel' to exit."):
            self.log("Downloading ")
            if self.lib_downloader:
                tkMessageBox.showinfo("Info", "Downloading is already in progress.")
            else:
                self._attempt_library_download()
        else:
            self.shutdown()
        return

    def _on_lib_download_finish(self, downloader):
        if self.lib_downloader and self.lib_downloader.lib_installed:  # success
            self.log("Data library has been downloaded successfully. You may perform OCR now.", False)
            self.ocr_thread.enqueue_task(self._ocr_start_engine)
            self.lib_downloader = None
        else:
            if self.lib_download_attempt < self.lib_download_attempts_max:
                self.log("Re-try download ...")
                self._attemp_library_download()
            else:
                self.log("Failed to download data library. Re-start to try again or contact support@asprise.com", True, "red")
                self.lib_downloader = None
        return

    def _on_lib_download_progress(self, total_size, current_size):
        if self._last_log_print is None or Ocr.get_time_tick() - self._last_log_print > 1:
            self.log(".", True, None, False)
            self._last_log_print = Ocr.get_time_tick()
        return

    def _enqueue_ui_action(self, func, *args, **kwargs):
        self._ui_update_queue.put_nowait((func, args, kwargs))

    def _update_ui(self):
        try:
            if not self._ui_update_queue.empty():
                ui_update = self._ui_update_queue.get_nowait()
                if ui_update:
                    func_obj = ui_update[0]
                    func_args = ui_update[1]
                    func_kwargs = ui_update[2]
                    func_obj(*func_args, **func_kwargs)
        except Exception as e:
            print(e)  # not much we can do here
        finally:
            self.after(50, self._update_ui)  # 1/20 second interval

    @staticmethod
    def main():
        root = Tk()
        if Ocr.is_windows():
            root.iconbitmap(get_asprise_ocr_root_with_trailing_slash() + 'asprise_ocr_api' + os.path.sep + 'icon.ico')
        root.wm_title("Asprise OCR")
        if Ocr.is_windows():
            root.wm_attributes("-topmost", 1)
        # root.geometry("800x600")
        app = OcrApp(master=root)
        app._update_ui()
        app.log(get_system_info())

        # center window

        app.mainloop()
        app.shutdown()
        #os._exit(0)
        sys.exit()

# OcrApp.main()


def md5_for_file(path, block_size=256*128):
    ''' Ref: http://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
    '''
    md5 = hashlib.md5()
    with open(path,'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
             md5.update(chunk)
    return md5.hexdigest()

def get_url_response_status(url):
    '''
    Return 0 if no internet connection; 502 if host doesn't exist, 404 if page not found; 200 if found.
    Ref: http://stackoverflow.com/questions/6471275/python-script-to-see-if-a-web-page-exists-without-downloading-the-whole-page '''
    try :
        p = urlparse(url)
        conn = httplib.HTTPConnection(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        return resp.status
    except Exception as e:
        print(e)
        return 0


class FileDownloader(threading.Thread):
    def __init__(self, url, save_to_file, progress_callback=None, max_attempts=3):
        '''
        :param url:
        :param save_to_file:
        :param progress_callback: func(total_size, current_size) total_size will be -1 if unknown.
        :param max_attempts:
        :return:
        '''
        if max_attempts <= 0:
            raise ValueError("max_attempts must be at least 1")
        threading.Thread.__init__(self)
        self.name = "downloader." + datetime.now().strftime("%H-%M-%S_%f")
        self.url = url
        self.save_to_file = save_to_file
        self.progress_callback = progress_callback
        self.max_attempts = max_attempts
        self._attempts = 0
        self.last_result = None
        self.last_exception = None
        self.success = False
        self.md5_checked = False

    def _report_hook(self, count, block_size, total_size):
        if self.progress_callback:
            self.progress_callback(total_size, count * block_size)
        return

    def run(self):
        self.download()
        return

    def download(self):
        while self._attempts < self.max_attempts:
            try:
                url_status = get_url_response_status(self.url)
                if url_status != 200:
                    continue

                self.last_result = urlretrieve(self.url, self.save_to_file, self._report_hook)

                # optional md5 check
                md5_attempts = 0
                md5_url = self.url + ".md5"
                md5_check_failure = False
                while md5_attempts < self.max_attempts:
                    try:
                        md5_f = urlopen(md5_url)
                        if md5_f.code == 404:  # not available
                            break
                        md5_value = md5_f.read()
                        md5_value = str(md5_value).strip()
                        if len(md5_value) == 32:  # found md5
                            md5_computed = md5_for_file(self.save_to_file)
                            if md5_value.lower() == md5_computed.lower():
                                self.md5_checked = True
                                break
                            else:
                                md5_check_failure = True
                    except Exception as me:
                        print(me)
                    finally:
                        md5_attempts += 1

                if md5_check_failure:
                    raise RuntimeError("MD5 check failed. Excepted: " + md5_value + ", Actual: " + md5_computed)

                self.success = True
                self.last_exception = None
                break  # file download while
            except Exception as e:
                self.last_exception = e
                if isinstance(e, HTTPError):
                    e.code == '404'  # not found
                    break
            finally:
                self._attempts += 1
        return


class OcrLibDownloader(FileDownloader):
    def __init__(self, base_url, finish_callback=None, progress_callback=None, max_attempts=3):
        self.finish_callback = finish_callback
        self.lib_installed = False
        self.lib_installed_to = None

        self.lib_file_name = Ocr._get_dynmaic_lib_file_name()
        url = base_url + self.lib_file_name
        self.tmp_folder = tempfile.mkdtemp("ol", "tmp")
        save_to_file = self.tmp_folder + os.sep + self.lib_file_name
        super(OcrLibDownloader, self).__init__(url, save_to_file, progress_callback, max_attempts)

    def run(self):
        try:
            self.download()
            if self.success:
                paths = [get_asprise_ocr_root_with_trailing_slash() + "asprise_ocr_api" + os.sep + "lib",
                         get_current_dir_with_trailing_slash(), get_writable_dir_with_trailing_slash()]
                for p in paths:
                    try:
                        os.makedirs(p)
                    except:
                        pass
                    f = suffix_with_trailing_slash(p) + self.lib_file_name
                    try:
                        shutil.copyfile(self.save_to_file, f)
                        # add to path if not in
                        if not p in sys.path:
                            sys.path.append(p)
                        self.lib_installed = True
                        self.lib_installed_to = f
                        break
                    except Exception as e:
                        print(e)

                if self.lib_installed:
                    shutil.rmtree(self.tmp_folder, True)
        finally:
            if self.finish_callback:
                self.finish_callback(self)
        return


def run_ocr_app():
    OcrApp.main()


if __name__ == '__main__':
    run_ocr_app()