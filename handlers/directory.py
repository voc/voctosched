from typing import Type

from .base import ImportHandler, ExportHandler
from .import_handlers import FakeImportHandler, CSVImportHandler, JSONImportHandler, ProyektorImportHandler, XcalImportHandler
from .export_handlers import BasicXMLExportHandler, ExtendedXMLExportHandler, FrabJsonExportHandler

import_handlers = {
    "csv": CSVImportHandler,
    "fake": FakeImportHandler,
    "json": JSONImportHandler,
    "proyektor": ProyektorImportHandler,
    "xcal": XcalImportHandler,
}

export_handlers = {
    "xml-basic": BasicXMLExportHandler,
    "xml-extended": ExtendedXMLExportHandler,
    "json-frab": FrabJsonExportHandler,
}


def resolve_import_handler(name: str) -> Type[ImportHandler]:
    return import_handlers[name]


def resolve_export_handler(name: str) -> Type[ExportHandler]:
    return export_handlers[name]
