#!/usr/bin/env python3

import argparse
import configparser
import logging


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", "-v", action="count")
    ap.add_argument("--quiet", "-q", action="count")
    ap.add_argument("--config", "-c", nargs="?", type=argparse.FileType('r'), default="./config.ini")
    ap.add_argument("--logfile", "-l")
    ap.add_argument("--debug", "-d", action="store_true")
    args = ap.parse_args()

    configure_logging(args)

    config = configparser.ConfigParser()
    config.read_file(args.config)


if __name__ == "__main__":
    main()
