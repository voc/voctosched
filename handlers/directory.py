from typing import Type

from .base import ImportHandler, ExportHandler
from .import_handlers import FakeImportHandler, CSVImportHandler, JSONImportHandler, ProyektorImportHandler
from .export_handlers import ScheduleXMLExportHandler, ExtendedXMLExportHandler, FrabJsonExportHandler

import_handlers = {
    "csv": CSVImportHandler,
    "fake": FakeImportHandler,
    "json": JSONImportHandler,
    "proyektor": ProyektorImportHandler,
}

export_handlers = {
    "xml": ScheduleXMLExportHandler,
    "xml-basic": ScheduleXMLExportHandler,
    "xml-extended": ExtendedXMLExportHandler,
    "json-frab": FrabJsonExportHandler,
}


def resolve_import_handler(name: str) -> Type[ImportHandler]:
    return import_handlers[name]


def resolve_export_handler(name: str) -> Type[ExportHandler]:
    return export_handlers[name]
