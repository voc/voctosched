import logging

from ..base import ExportHandler
from fahrplan.model.schedule import Schedule
from hacks import noexcept
from util import write_file


log = logging.getLogger(__name__)


class ExtendedXMLExportHandler(ExportHandler):
    @noexcept(log)
    def run(self, schedule: Schedule) -> bool:
        path = self.config["path"]
        content = schedule.to_xml(extended=True)
        return write_file(path, content)
