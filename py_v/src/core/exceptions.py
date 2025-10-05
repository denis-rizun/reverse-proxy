from py_v.src.core.logger import Logger

logger = Logger.setup(__name__)


class MainError(Exception):
    def __init__(self, message: str) -> None:
        logger.error(f"[{self.__class__.__name__}] {message}")
        super().__init__(message)


class ConfigError(MainError):
    pass


class ConfigNotFoundError(ConfigError):
    pass


class ConfigNotSupportTypeError(ConfigError):
    pass


class ConfigMissingRequiredKeyError(ConfigError):
    pass


class HTTPError(MainError):
    pass


class HTTPInvalidRequestError(HTTPError):
    pass


class HTTPRequestError(HTTPError):
    pass
