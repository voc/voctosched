#!/usr/bin/env python3

import logging

from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from functools import reduce
from typing import List

from fahrplan.model.schedule import Schedule
from handlers.base import ImportHandler, ExportHandler
from handlers.directory import resolve_import_handler, resolve_export_handler


log = logging.getLogger(__name__)


def configure_logging(args):
    verbosity = (args.verbose or 0) - (args.quiet or 0)
    if verbosity <= -2:
        level = logging.CRITICAL
    elif verbosity == -1:
        level = logging.ERROR
    elif verbosity == 0:
        level = logging.WARNING
    elif verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG

    # fancy colors
    logging.addLevelName(logging.CRITICAL, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.CRITICAL))
    logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.DEBUG, "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))

    if args.debug:
        log_format = '%(asctime)s - %(name)s - %(levelname)s {%(filename)s:%(lineno)d} %(message)s'
    else:
        log_format = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=args.logfile, level=level, format=log_format)


def initialize_handlers(kind: str, config: ConfigParser):
    if kind == "import":
        resolve = resolve_import_handler
    elif kind == "export":
        resolve = resolve_export_handler
    else:
        raise ValueError(f'Invalid handler kind "{kind}"')
    handler_names = [name.strip() for name in config[kind]["active"].split(",")]
    handlers = []
    for name in handler_names:
        handler_config = config[f"{kind}:{name}"]
        handler_type = handler_config["type"]
        handler_class = resolve(handler_type)
        handler = handler_class(name, handler_config)
        handlers.append(handler)

    return handlers


def initialize_import_handlers(config: ConfigParser) -> List[ImportHandler]:
    return initialize_handlers("import", config)


def initialize_export_handlers(config: ConfigParser) -> List[ExportHandler]:
    return initialize_handlers("export", config)


def main():
    ap = ArgumentParser()
    ap.add_argument("--verbose", "-v", action="count")
    ap.add_argument("--quiet", "-q", action="count")
    ap.add_argument("--config", "-c", nargs="?", type=FileType('r'), default="./config.ini")
    ap.add_argument("--logfile", "-l")
    ap.add_argument("--debug", "-d", action="store_true")
    args = ap.parse_args()

    configure_logging(args)

    config = ConfigParser()
    config.read_file(args.config)

    import_handlers = initialize_import_handlers(config)
    export_handlers = initialize_export_handlers(config)

    imported_schedules = []
    for handler in import_handlers:
        imported_schedules.append(handler.run())

    final_schedule = reduce(Schedule.merge, imported_schedules)

    # TODO (zuntrax) use config["conference"]

    for handler in export_handlers:
        handler.run(final_schedule)


if __name__ == "__main__":
    main()
