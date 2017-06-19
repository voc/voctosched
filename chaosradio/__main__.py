from configparser import ConfigParser
from glob import glob
from os.path import expanduser
from xml.sax import make_parser

from chaosradio.content_handler import ChaosradioContentHandler
from chaosradio.sort import get_num


def main():
    conf = ConfigParser()
    conf.read(["chaosradio.ini"])
    parser = make_parser()
    handler = ChaosradioContentHandler(conf)
    parser.setContentHandler(handler)
    for path in sorted(
        glob(expanduser(conf["input"]["glob"])),
        key=get_num
    ):
        with open(path) as f:
            try:
                parser.parse(f)
            except Exception as e:
                print(path)
                raise e

    schedule = handler.get_schedule()
    print(schedule.to_xml())


if __name__ == "__main__":
    main()
