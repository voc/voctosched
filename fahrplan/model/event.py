from uuid import uuid4
from fahrplan.xml import xml, xml_open, xml_close, xml_dict


class Event:
    def __init__(self, uid, date, start, duration, title, language, slug, rec_license, rec_optout,
                 guid="", subtitle="", track="", event_type="", abstract="", description='', logo="",
                 persons=None, links=None, attachments=None, download_url=None):
        self.id = uid
        self.date = date
        self.start = start
        self.duration = duration
        self.title = title
        self.language = language
        self.guid = guid or uuid4()
        self.slug = slug
        self.rec_license = rec_license
        self.rec_optout = rec_optout
        self.subtitle = subtitle
        self.track = track
        self.type = event_type
        self.abstract = abstract
        self.description = description
        self.logo = logo
        self.persons = persons or dict()  # TODO: should be mandatory
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

    def to_xml(self, level=3):
        # TODO: this is ugly, maybe XmlSerializer class?
        result = ""
        result += xml_open("event", level, guid=self.guid, id=self.id)
        result += xml("date", f"{self.date:%Y-%m-%dT%H:%M:%S}", level+1)
        result += xml("start", f"{self.start:%H:%M}", level+1)
        result += xml("duration", f"{str(self.duration)[:-3]}", level+1)
        result += xml("room", self.room, level+1)
        result += xml("slug", self.slug, level+1)
        result += xml_open("recording", level+1)
        result += xml("license", self.rec_license, level+2)
        result += xml("optout", self.rec_optout, level+2)
        result += xml_close("recording", level+1)
        result += xml("title", self.title, level+1)
        result += xml("language", self.language, level+1)
        result += xml("subtitle", self.subtitle, level+1)
        result += xml("track", self.track, level+1)
        result += xml("type", self.type, level+1)
        result += xml("abstract", self.abstract, level+1)
        result += xml("description", self.description, level+1)
        result += xml("logo", self.logo, level+1)
        result += xml_dict("person", self.persons, "id", level+1)
        result += xml_dict("link", self.links, "href", level+1)
        result += xml_dict("attachment", self.attachments, "href", level+1)
        result += xml("download_url", self.download_url, level+1)
        result += xml_close("event", level)

        return result
