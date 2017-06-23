import logging

from ..base import ExportHandler
from fahrplan.model.schedule import Schedule


log = logging.getLogger(__name__)


class BasicXMLExportHandler(ExportHandler):
    def run(self, schedule: Schedule) -> bool:
        try:
            with open(self.config["path"], "w") as f:
                f.write(schedule.to_xml(extended=False))
            return True
        except (PermissionError, IOError):
            log.exception()
            return False
