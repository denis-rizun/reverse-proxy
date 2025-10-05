import logging
import sys


class Logger:
    FMT = "[%(asctime)s] [%(levelname)-8s]: %(message)s"
    DATEFMT = "%y-%m-%d %H:%M:%S"
    LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    @classmethod
    def setup(cls, level: str = "info") -> logging.Logger:
        logger = logging.getLogger(__name__)

        if logger.hasHandlers():
            logger.handlers.clear()

        level = cls.LEVELS.get(level, logging.INFO)
        logger.setLevel(level)
        formatter = logging.Formatter(fmt=cls.FMT, datefmt=cls.DATEFMT)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger
