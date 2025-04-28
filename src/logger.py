# log_config.py
import logging
import colorlog
import os
from datetime import datetime



# Define custom level
SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

def success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS_LEVEL):
        self._log(SUCCESS_LEVEL, message, args, **kwargs)

logging.Logger.success = success


def setup_logger(name="my_logger", level=logging.DEBUG):

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if not logger.handlers:
        # Console handler with color
        console_handler = logging.StreamHandler()
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(levelname)s] %(asctime)s - %(message)s",
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'SUCCESS': 'bold_green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        )
        console_handler.setFormatter(console_formatter)




        # File handler (plain)
        LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" 
        log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
        os.makedirs(log_path, exist_ok=True)

        LOG_FILE_PATH  = os.path.join(log_path, LOG_FILE)

        
        file_handler = logging.FileHandler(LOG_FILE_PATH, mode="a")
        file_formatter = logging.Formatter("[%(levelname)s] %(asctime)s - %(message)s",
                                           datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger





