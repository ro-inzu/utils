from datetime import datetime
import logging
import os

STM = datetime.now().strftime('%H:%M:%S.%f')[:-3]

FMT = '[%(asctime)s]  %(name)s  %(levelname)s  %(funcName)s:%(lineno)d  %(message)s'
FORMATTER = logging.Formatter(FMT, datefmt='%H:%M:%S')

class Logger(object):

    def __init__(self, mod_name, log_fname,options = ""):
        self.mod_name = mod_name
        # list of options entered from user [example_file.py -d]
        self.options = options
        self.log_fname = log_fname
        self.logger = logging.getLogger(self.mod_name)

    # writes to stream/console
    def get_stream_handler(self):  
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(CustomFormatter(FMT))
        return stream_handler


    # writes to disk
    def get_file_handler(self):
        # log name date format
        file_date_fmt = "{:%m-%d-%Y}".format(datetime.now())
        # name of log file
        file_name = f"{file_date_fmt}_{self.log_fname}.log"
        # path where log file is written to disk
        file_out = "~/"

        file_handler = logging.FileHandler(os.path.join(file_out, file_name), mode='w')
        file_handler.setFormatter(FORMATTER)
        return file_handler


    def setup_logger(self):
        self.logger.setLevel(logging.DEBUG)
        # add handlers to log obj
        self.logger.addHandler(self.get_stream_handler())
        # looks through all optional args entered from user 
        for option in self.options:
            # write to disk if option in sys.args from file invoking the logger
            if option in ["-d","-D","-Disk","-disk"]:
                print(f"File handler added to logger..")
                self.logger.addHandler(self.get_file_handler())

        return self.logger

    def reset_logger(self):
        self.logger.propagate = True
        self.logger.disabled = False
        self.logger.filters.clear()
        handlers = self.logger.handlers.copy()
        for handler in handlers:
            try:
                handler.acquire()
                handler.flush()
                handler.close()
            except Exception as e:
                print(e)
            finally:
                handler.release()
            self.logger.removeHandler(handler)


class CustomFormatter(logging.Formatter):

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


log_obj = Logger("app","app")
log = log_obj.setup_logger()
log.info("eatea")
