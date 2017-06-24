import datetime as dt
from typing import Dict, Union, Callable

from fahrplan.datetime import format_datetime, format_time, format_duration
from fahrplan.exception import FahrplanError
from fahrplan.xml import XmlWriter, XmlSerializable
from ..uuid import uuid


class Event(XmlSerializable):
    # TODO (MO) decide about reasonable default license or make mandatory
    # TODO (MO) maybe use UUID instances instead of strings? probably inconvenient
    def __init__(self, uid: int, date: dt.datetime, start: dt.time, duration: dt.timedelta, title: str, language: str,
                 slug: Union[str, Callable], persons: Dict[int, str], recording_license: str = "???",
                 recording_optout: bool = False, guid: str = "", subtitle: str = "", track: str = "",
                 event_type: str = "", abstract: str = "", description: str = '', logo: str = "",
                 download_url: str = "", links: Dict[str, str] = None, attachments: Dict[str, str] = None):
        self.id = uid
        self.date = date
        self.start = start
        self.duration = duration
        self.title = title
        self.language = language
        self.guid = guid or uuid(uid, title)
        self.rec_license = recording_license
        self.rec_optout = recording_optout
        self.subtitle = subtitle
        self.track = track
        self.type = event_type
        # TODO (MO) proper indentation for multi-line text blobs
        self.abstract = abstract
        self.description = description
        self.logo = logo
        if not persons:
            raise FahrplanError("Excepted at least one person for event creation, none are given.")
        self.persons = persons
        self.links = links or {}
        self.attachments = attachments or {}
        self.download_url = download_url
        self.room = None
        if callable(slug):
            self.slug = slug(self)
        else:
            self.slug = slug

    def add_person(self, uid: int, name: str):
        self.persons[uid] = name

    def add_link(self, href: str, title: str):
        self.links[href] = title

    def add_attachment(self, href: str, title: str):
        self.attachments[href] = title

    def append_xml(self, xml: XmlWriter, extended: bool):
        with xml.context("event", guid=self.guid, id=self.id):
            xml.tag("date", format_datetime(self.date))
            xml.tag("start", format_time(self.start))
            xml.tag("duration", format_duration(self.duration))
            xml.tag("room", self.room.name)
            xml.tag("slug", self.slug)
            with xml.context("recording"):
                xml.tag("license", self.rec_license)
                xml.tag("optout", str(self.rec_optout).lower())
            xml.tag("title", self.title)
            xml.tag("language", self.language)
            xml.tag("subtitle", self.subtitle)
            xml.tag("track", self.track)
            xml.tag("type", self.type)
            xml.tag("abstract", self.abstract)
            xml.tag("description", self.description)
            xml.tag("logo", self.logo)
            xml.append_dict("person", self.persons, "id")
            xml.append_dict("link", self.links, "href")
            xml.append_dict("attachment", self.attachments, "href")
            if extended:
                xml.tag("video_download_url", self.download_url)
