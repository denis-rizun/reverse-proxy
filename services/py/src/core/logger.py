import logging
import sys


class Logger:
    FMT = "[%(asctime)s] [%(levelname)-8s]: %(message)s"
    DATEFMT = "%y-%m-%d %H:%M:%S"

    @classmethod
    def setup(cls) -> logging.Logger:
        logger = logging.getLogger(__name__)

        if logger.hasHandlers():
            logger.handlers.clear()

        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt=cls.FMT, datefmt=cls.DATEFMT)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger
