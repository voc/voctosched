import logging
import urllib.request

from typing import Union


log = logging.getLogger(__name__)


def looks_like_url(path: str):
    url_starts = ["http://", "https://"]
    return any(path.startswith(x) for x in url_starts)


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
    if looks_like_url(path):
        with urllib.request.urlopen(path) as f:
            content = f.read().decode()
        return content
    else:
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
