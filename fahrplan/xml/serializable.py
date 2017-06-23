from abc import ABCMeta, abstractmethod

from .writer import XmlWriter


class XmlSerializable(metaclass=ABCMeta):
    def to_xml(self, extended: bool = False):
        xml = XmlWriter()
        self.append_xml(xml, extended)
        return xml.buffer

    @abstractmethod
    def append_xml(self, xml: XmlWriter, extended: bool):
        pass
