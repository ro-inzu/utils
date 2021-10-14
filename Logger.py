import datetime
import logging
import os
from datetime import datetime
from configs import AppConfig, EnvironmentConfig

stm = datetime.now().strftime('%H:%M:%S.%f')[:-3]


class TimeFilter(logging.Filter):
    def filter(self, record):
        global stm
        record.relative = stm
        stm = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        return True


app_con = AppConfig()
env_conf = EnvironmentConfig()
log_path = os.path.join(app_con.get_log_path())
root_output = env_conf.root_output_path()


class Logger(object):

    def __init__(self, mod_name, log_fname, state="", county=""):
        self.date_fmt = "{:%m-%d-%Y}".format(datetime.now())
        # setup filename info
        self.log_name = f"{self.date_fmt}_{log_fname}.log"
        self.mod_name = mod_name
        if state and county:
            self.file_name = f"{state}_{county}_{self.log_name}"
        else:
            self.file_name = f"{self.date_fmt}_{self.log_name}.log"
        # sends logging output to disk file
        self.file_handler = logging.FileHandler(os.path.join(env_conf.log_output_path(), self.file_name), mode='w')
        # sends logging output to streams (STDOUT and STDERR)
        self.stream_handler = logging.StreamHandler()
        self.logger = logging.getLogger(self.mod_name)

    def get_logger(self):
        self.setup_logger()
        return self.logger

    def setup_logger(self):
        # add log format
        fmt = app_con.get_log_fmt()
        formatter = logging.Formatter(fmt, datefmt='%H:%M:%S')
        # set formatting to file and stream handler(s)
        self.file_handler.setFormatter(formatter)
        self.stream_handler.setFormatter(formatter)
        # add handlers to log obj
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)
        # set logging levels to log obj
        self.logger.setLevel(logging.INFO)
        self.logger.setLevel(logging.DEBUG)
        for handle in self.logger.handlers:
            handle.addFilter(TimeFilter())
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


# listener_log_obj = Logger("listener", "jobs")
# log = listener_log_obj.setup_logger()
# counter = 50
# dict_state = {"KY": "Woodford", "AL": "AL_county", "CA": "ORange"}
# while counter > 0:
#     log.info("looking for a job")
#     for state, county in dict_state.items():
#         state_obj_logger = Logger("semantic", f"{state}_{county}---test", state, county)
#         logger_sate = state_obj_logger.setup_logger()
#         logger_sate.info("logging : {}".format(state))
#         state_obj_logger.reset_logger()
#         del state_obj_logger
#     counter = -1
#     log.info("processed a job")
