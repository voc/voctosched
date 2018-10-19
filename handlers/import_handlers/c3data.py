import logging

from hacks import noexcept
from ..base import ImportHandler
from graphql import run_query
from pprint import pprint
import json

from fahrplan.datetime import parse_date, parse_datetime, parse_duration, parse_time

from fahrplan.model.conference import Conference
from fahrplan.model.schedule import Schedule
from fahrplan.model.day import Day
from fahrplan.model.event import Event

query_template = """
query {
  conference: conferenceByAcronym(acronym: "__ACRONYM__") {
    acronym
    title
    start: startDate
    end: endDate
    days: daysByConferenceId {
      nodes {
        index
        date
        startDate
        endDate
      }
    }
    rooms: roomsByConferenceId {
      nodes {
        name
      }
    }
    events: eventsByConferenceId {
      nodes {
        id: localId
        guid
        dayIndex
        roomName
        logo
        startDate
        startTime
        duration: durationTime
        slug
        title
        subtitle
        track: trackByTrackId {
          name
        }
        eventType
        language
        abstract
        description
        recordingLicense
        doNotRecord
        persons(roles: [SPEAKER, MODERATOR]) {
          nodes {
            id
            publicName
          }
        }
        links {
          title
          url
        }
        attachments {
          title
          url
        }
      }
    }
  }
}
"""


log = logging.getLogger(__name__)


class C3DataImportHandler(ImportHandler):
    @noexcept(log)
    def run(self):
        query = query_template.replace('__ACRONYM__', self.config.get('acronym'))
        resp = run_query(self.config.get('url'), query)
        conf_tree = resp['data']['conference']

        conference = Conference(
            title=conf_tree['title'],
            acronym=conf_tree['acronym'],
            start=conf_tree['start'],
            end=conf_tree['end'],
            day_count=0,
            time_slot_duration=parse_duration("0:05")
        )
        schedule = Schedule(conference=conference, version="ASDF")

        for day_tree in conf_tree['days']['nodes']:
            schedule.add_day(Day(
                index=day_tree['index'],
                date=parse_date(day_tree['date']),
                start=parse_datetime(day_tree['startDate']),
                end=parse_datetime(day_tree['endDate'])
            ))
        
        for room_tree in conf_tree['rooms']['nodes']:
            schedule.add_room(room_tree['name'])
        
        for event_tree in conf_tree['events']['nodes']:
            persons = dict()
            for person_tree in event_tree['persons']['nodes'] or ():
                persons[int(person_tree['id'])] = person_tree['publicName']

            links = dict()
            for link_tree in event_tree['links'] or ():
                links[link_tree['title']] = link_tree['url']

            attachments = dict()
            for attachment_tree in event_tree['links'] or ():
                attachments[attachment_tree['title']] = attachment_tree['url']

            schedule.add_event(int(event_tree['dayIndex']), event_tree['roomName'], Event(
                uid=event_tree['id'],
                guid=event_tree['guid'],
                logo=event_tree['logo'],
                date=parse_datetime(event_tree['startDate']),
                start=parse_time(event_tree['startTime']),
                duration=parse_duration(event_tree['duration']),
                slug=event_tree['slug'],
                title=event_tree['title'],
                subtitle=event_tree['subtitle'],
                track=event_tree['track'],
                event_type=event_tree['eventType'],
                language=event_tree['language'],
                abstract=event_tree['abstract'],
                description=event_tree['description'],
                recording_license=event_tree['recordingLicense'],
                recording_optout=event_tree['doNotRecord'],
                persons=persons,
                links=links,
                attachments=attachments,
            ))

        return schedule
