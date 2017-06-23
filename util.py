import logging

from typing import Union


log = logging.getLogger(__name__)


def write_file(path: str, content: str) -> bool:
    log.info(f'Writing file "{path}".')
    try:
        with open(path, "w") as f:
            f.write(content)
        return True
    except PermissionError:
        log.error(f'No permission to open "{path}".')
        return False
    except IsADirectoryError:
        log.error(f'Cannot open directory "{path}".')
        return False
    except IOError:
        log.exception(f'Error writing file "{path}".')
        return False


def read_file(path: str) -> Union[str, None]:
    log.info(f'Reading file "{path}".')
    try:
        with open(path, "r") as f:
            content = f.read()
        return content
    except PermissionError:
        log.error(f'No permission to open "{path}".')
        return None
    except IsADirectoryError:
        log.error(f'Cannot open directory "{path}".')
        return None
    except IOError:
        log.exception(f'Error reading file "{path}".')
        return None
