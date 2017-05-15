from ..uuid import uuid
from fahrplan.xml import XmlSerializer


class Event:
    def __init__(self, uid, date, start, duration, title, language, slug, persons, rec_license="???",
                 rec_optout=False, guid="", subtitle="", track="", event_type="", abstract="", description='',
                 logo="", links=None, attachments=None, download_url=None):
        self.id = uid
        self.date = date
        self.start = start
        self.duration = duration
        self.title = title
        self.language = language
        self.guid = guid or uuid(uid, title)
        self.slug = slug
        self.rec_license = rec_license
        self.rec_optout = rec_optout
        self.subtitle = subtitle
        self.track = track
        self.type = event_type
        self.abstract = abstract
        self.description = description
        self.logo = logo
        assert persons
        self.persons = persons
        self.links = links or dict()
        self.attachments = attachments or dict()
        self.download_url = download_url
        self.room = None

    def add_person(self, uid, name):
        self.persons[uid] = name

    def add_link(self, href, title):
        self.links[href] = title

    def add_attachment(self, href, title):
        self.attachments[href] = title

    def to_xml(self, serializer=None):
        xml = serializer or XmlSerializer()
        xml.enter("event", guid=self.guid, id=self.id)
        xml.tag("date", f"{self.date:%Y-%m-%dT%H:%M:%S}")
        xml.tag("start", f"{self.start:%H:%M}")
        xml.tag("duration", f"{str(self.duration)[:-3]}")
        xml.tag("room", self.room)
        xml.tag("slug", self.slug)
        xml.enter("recording")
        xml.tag("license", self.rec_license)
        xml.tag("optout", str(self.rec_optout).lower())
        xml.exit("recording")
        xml.tag("title", self.title)
        xml.tag("language", self.language)
        xml.tag("subtitle", self.subtitle)
        xml.tag("track", self.track)
        xml.tag("type", self.type)
        xml.tag("abstract", self.abstract)
        xml.tag("description", self.description)
        xml.tag("logo", self.logo)
        xml.dict("person", self.persons, "id")
        xml.dict("link", self.links, "href")
        xml.dict("attachment", self.attachments, "href")
        xml.tag("download_url", self.download_url)
        xml.exit("event")

        if not serializer:
            return xml.buffer
