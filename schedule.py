#!/usr/bin/env python3

import logging
import sys

from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from functools import reduce
from typing import List

from fahrplan.model.schedule import Schedule
from handlers.base import ImportHandler, ExportHandler
from handlers.directory import resolve_import_handler, resolve_export_handler


if sys.version_info < (3, 6):
    print("At least python version 3.6 is required to run.")
    sys.exit(1)


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
    logging.addLevelName(logging.CRITICAL, '\033[1;41m%s\033[1;0m' % logging.getLevelName(logging.CRITICAL))
    logging.addLevelName(logging.ERROR, '\033[1;31m%s\033[1;0m' % logging.getLevelName(logging.ERROR))
    logging.addLevelName(logging.WARNING, '\033[1;33m%s\033[1;0m' % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.INFO, '\033[1;32m%s\033[1;0m' % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.DEBUG, '\033[1;34m%s\033[1;0m' % logging.getLevelName(logging.DEBUG))

    if args.debug:
        log_format = '%(asctime)s - %(name)s - %(levelname)s {%(filename)s:%(lineno)d} %(message)s'
    else:
        log_format = '%(asctime)s - %(levelname)s - %(message)s'

    logging.basicConfig(filename=args.logfile, level=level, format=log_format)


def initialize_handlers(kind: str, config: ConfigParser):
    if kind == 'import':
        resolve = resolve_import_handler
    elif kind == 'export':
        resolve = resolve_export_handler
    else:
        raise ValueError(f'Invalid handler kind "{kind}"')
    handler_names = [name.strip() for name in config[kind]['active'].strip().split(',')]
    handlers = []
    for name in handler_names:
        if not name:
            log.warning("Skipping empty handler name.")
            continue
        full_name = f'{kind}:{name}'
        log.debug(f'Initializing handler "{full_name}"')
        try:
            handler_config = config[full_name]
        except KeyError:
            log.error(f'{kind.capitalize()} handler "{name}" configured as active, '
                      f'but section "{full_name}" in config is missing.')
            continue
        handler_type = handler_config["type"]
        log.debug(f'Requesting {kind} handler type "{handler_type}".')
        try:
            handler_class = resolve(handler_type)
        except KeyError:
            log.error(f'Handler type "{handler_type}" does not exist. Skipping.')
            continue
        handler = handler_class(full_name, handler_config)
        handlers.append(handler)

    return handlers


def initialize_import_handlers(config: ConfigParser) -> List[ImportHandler]:
    log.info('Initializing import handlers.')
    handlers = initialize_handlers("import", config)
    log.debug('Finished initializing import handlers.')
    return handlers


def initialize_export_handlers(config: ConfigParser) -> List[ExportHandler]:
    log.info('Initializing export handlers.')
    handlers = initialize_handlers("export", config)
    log.debug('Finished initializing export handlers.')
    return handlers


def main():
    ap = ArgumentParser()
    ap.add_argument('--verbose', '-v', action='count')
    ap.add_argument('--quiet', '-q', action='count')
    ap.add_argument('--config', '-c', nargs='?', type=FileType('r'), default='./config.ini')
    ap.add_argument('--logfile', '-l')
    ap.add_argument('--debug', '-d', action='store_true')
    args = ap.parse_args()

    configure_logging(args)

    log.info(f'Using config file "{args.config.name}".')
    config = ConfigParser()
    config.read_file(args.config)
    log.debug('Basic initialization done.')

    import_handlers = initialize_import_handlers(config)
    imported_schedules = []
    log.info('Running import handlers')
    if not import_handlers:
        log.critical("No import handlers to run, aborting.")
        sys.exit(1)
    for handler in import_handlers:
        log.info(f'Running import handler "{handler.name}".')
        imported_schedules.append(handler.run())
    log.debug('Finished running import handlers')

    if not any(imported_schedules):
        log.critical("All import handlers failed, aborting.")
        sys.exit(1)

    log.info('Merging schedules.')
    final_schedule = reduce(Schedule.merge, imported_schedules)
    log.debug('Finished merging schedules.')

    # TODO (zuntrax) use config["conference"]
    if 'conference' in config:
        log.warning('Overriding conference data not implemented.')

    export_handlers = initialize_export_handlers(config)
    results = []
    log.info('Running export handlers')
    if not export_handlers:
        log.critical("No export handlers to run, aborting.")
        sys.exit(1)
    for handler in export_handlers:
        log.info(f'Running export handler "{handler.name}".')
        result = handler.run(final_schedule)
        results.append(result)
    log.debug('Finished running export handlers')

    if not any(results):
        log.critical("All export handlers failed, no usable output produced.")
        sys.exit(1)


if __name__ == '__main__':
    main()
