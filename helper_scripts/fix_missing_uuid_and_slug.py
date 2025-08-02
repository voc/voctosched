#!/usr/bin/python3
"""
early versions of frab and pentabarf schedules are missing a slug and guid which we need for the tracker
"""
import xml.etree.ElementTree as ET
import uuid

schedule = "froscon2008_dl.xml"
output = "froscon2008_foo.xml"

uuid_namespace = uuid.UUID("54dc9c85-9b6a-40bd-9a36-41c004a5829b")

with open(schedule, "r") as schedule:
    tree = ET.parse(schedule)
    root = tree.getroot()
    for event in root.iter("event"):
        print(event.attrib["id"])
        event.append(ET.Element("slug"))
        print(event.find("room").text)
        slug_elements = [
            event.find("room").text,
            event.find("title").text,
            event.attrib["id"],
        ]
        print(slug_elements)
        slug = "_-_".join(slug_elements).replace(" ", "_")
        event.find("slug").text = slug
        event.attrib["guid"] = str(uuid.uuid5(uuid_namespace, slug))

    tree.write(output)
print("schedule written to " + output)
