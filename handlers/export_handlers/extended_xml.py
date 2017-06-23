import logging

from ..base import ExportHandler
from fahrplan.model.schedule import Schedule


log = logging.getLogger(__name__)


class ExtendedXMLExportHandler(ExportHandler):
    def run(self, schedule: Schedule) -> bool:
        try:
            with open(self.config["path"], "w") as f:
                f.write(schedule.to_xml(extended=True))
            return True
        except (PermissionError, IOError):
            log.exception()
            return False
