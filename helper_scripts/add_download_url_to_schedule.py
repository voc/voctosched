#!/usr/bin/python3
"""
build a schedule with download URLs from a given schedule and a file list.
"""
import xml.etree.ElementTree as ET
import pprint

schedule = 'froscon2008.xml'
file_list = 'froscon2008.txt'
output = 'froscon2008_dl.xml'
delimitter = '_-_'
id_posittion = -1
video_base_url = 'https://cdn.media.ccc.de/events/froscon/2008/'

files = {}
files_count = 0
files_format_error = 0
print('reading file list')
with open(file_list,'r') as list:
    for line in list:
        try:
            files_count += 1
            files[line.split(delimitter)[id_posittion].split('.')[0].strip()] = video_base_url + line.rstrip()
            print(str(files_count) + ': ' + line.rstrip())
        except:
            print('Warning: line ' + line + ' is not in expected format, skipping')
            files_format_error += 1

printer = pprint.PrettyPrinter()
printer.pprint(files)
print(len(files))
print('reading schedule')
frab_data = None
events_count = 0
matches_count = 0

with open(schedule, 'r') as schedule:
    tree = ET.parse(schedule)
    root = tree.getroot()
    to_be_deleted = {}
    for room in root.iter('room'):
        for event in room.iter('event'):
            print(event.attrib['id'])
            events_count += 1
            if event.attrib['id'] in files.keys():
                event.append(ET.Element('video_download_url'))
                event.find('video_download_url').text = files[event.attrib['id']]
                matches_count += 1
                del files[event.attrib['id']]
            else:
                to_be_deleted[event] = room

    for event,room in to_be_deleted.items():
        room.remove(event)
    tree.write(output)
print('schedule written to ' + output)
print('Found ' + str(events_count) + ' events and ' + str(files_count) + ' video files. There where ' +
      str(matches_count) + ' matches. ' + str(files_format_error) + ' files had a format errors in its '
                                                          'filnename and have been skipped')
print('not matching files' + str(files))