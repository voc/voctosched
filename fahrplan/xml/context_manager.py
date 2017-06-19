from typing import Dict


class XmlContextManager:
    def __init__(self, tag: str, properties: Dict, xml_writer: 'XmlWriter'):
        self.tag = tag
        self.properties = properties
        self.xml_writer = xml_writer

    def __enter__(self):
        self.xml_writer.enter(self.tag, **self.properties)

    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_type, exc_val, exc_tb
        self.xml_writer.exit(self.tag)
