import logging

from ..base import ExportHandler
from fahrplan.model.schedule import Schedule
from hacks import noexcept


log = logging.getLogger(__name__)


class BasicXMLExportHandler(ExportHandler):
    @noexcept
    def run(self, schedule: Schedule) -> bool:
        path = self.config["path"]
        try:
            with open(path, "w") as f:
                f.write(schedule.to_xml(extended=False))
            return True
        except PermissionError:
            log.error(f'No permission to open "{path}".')
            return False
        except IsADirectoryError:
            log.error(f'Cannot open directory "{path}" for writing.')
            return False
        except IOError:
            log.exception(f'Error writing file "{path}".')
            return False
