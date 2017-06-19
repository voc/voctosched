#    Copyright (C) 2017  derpeter
#    derpeter@berlin.ccc.de
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import configparser
import logging
import os
import sys
import csv
import urllib.request

from fahrplan.datetime import parse_date, parse_datetime, parse_duration, parse_time
import fahrplan.model.conference
from fahrplan.model.conference import Conference
from fahrplan.model.event import Event
from fahrplan.model.schedule import Schedule
#from fahrplan.model import Conference, Event, Schedule
from fahrplan.slug.standard import StandardSlugGenerator


class main:
    """
    This class reads an CSV file and creates a schedule object from it.
    """

    def __init__(self):
        if not os.path.exists('config.conf'):
            raise IOError("config file not found")

        self.config = configparser.ConfigParser()
        self.config.read('config.conf')

        # set up logging
        logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
        logging.addLevelName(logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
        logging.addLevelName(logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
        logging.addLevelName(logging.DEBUG, "\033[1;85m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))

        self.logger = logging.getLogger()

        ch = logging.StreamHandler(sys.stdout)
        if self.config['general']['debug']:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s {%(filename)s:%(lineno)d} %(message)s')
        else:
            formatter = logging.Formatter('%(asctime)s - %(message)s')

        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.logger.setLevel(logging.DEBUG)

        level = self.config['general']['debug']
        if level == 'info':
            self.logger.setLevel(logging.INFO)
        elif level == 'warning':
            self.logger.setLevel(logging.WARNING)
        elif level == 'error':
            self.logger.setLevel(logging.ERROR)
        elif level == 'debug':
            self.logger.setLevel(logging.DEBUG)

        self.type = self.config.get('source', 'type')
        self.source = self.config.get('source', 'source')

        logging.debug('reading ' + str(self.source) + ' from ' + self.type)

        if self.type == 'file':
            logging.info('reading CSV from file')
            self.openCSV()
            self.readCSV()
        elif self.type == 'URL':
            self.downloadCSV()
        else:
            logging.error(str(self.type) + ' is not a valid source type')


    def readCSV(self):
        """
        read the given CSV
        :return:
        """

    def downloadCSV(self):
        pass

    def openCSV(self):
        with open(self.source, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                print(row['Title'])


if __name__ == '__main__':
    main()