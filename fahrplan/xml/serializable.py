from abc import ABCMeta, abstractmethod

from .writer import XmlWriter


class XmlSerializable(metaclass=ABCMeta):
    def to_xml(self):
        xml = XmlWriter()
        self.append_xml(xml)
        return xml.buffer

    @abstractmethod
    def append_xml(self, xml: XmlWriter):
        pass
