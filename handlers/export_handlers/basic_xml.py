from ..base import ExportHandler
from fahrplan.model.schedule import Schedule


class BasicXMLExportHandler(ExportHandler):
    def run(self, schedule: Schedule):
        with open(self.config["path"], "w") as f:
            f.write(schedule.to_xml(extended=False))
