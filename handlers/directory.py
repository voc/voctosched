from typing import Type

from .base import ImportHandler, ExportHandler
from .import_handlers import FakeImportHandler, CSVImportHandler
from .export_handlers import BasicXMLExportHandler, ExtendedXMLExportHandler

import_handlers = {
    "csv": CSVImportHandler,
    "fake": FakeImportHandler,
}

export_handlers = {
    "xml-basic": BasicXMLExportHandler,
    "xml-extended": ExtendedXMLExportHandler,
}


def resolve_import_handler(name: str) -> Type[ImportHandler]:
    return import_handlers[name]


def resolve_export_handler(name: str) -> Type[ExportHandler]:
    return export_handlers[name]
