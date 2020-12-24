import logging

from ..base import ExportHandler
from fahrplan.model.schedule import Schedule
from hacks import noexcept
from util import write_output


log = logging.getLogger(__name__)


class ExtendedXMLExportHandler(ExportHandler):
    def export(self, schedule: Schedule) -> str:
        return schedule.to_xml(extended=True)
