from typing import Any, Dict

from .context_manager import XmlContextManager


class XmlWriter:
    def __init__(self, indentation_style: str = "  "):
        self.indentation_style = indentation_style
        self.buffer = ""
        self.level = 0

    @staticmethod
    def pluralize(name: str):
        return f"{name}s"

    @staticmethod
    def format_properties(tag: str, properties: Dict):
        items = [tag]
        for name, value in properties.items():
            items.append(f'{name}="{value}"')
        return " ".join(items)

    def append_indentation(self):
        self.buffer += self.indentation_style * self.level

    def tag(self, tag: str, inner: Any, **properties):
        self.append_indentation()
        if not inner:
            self.buffer += f"<{self.format_properties(tag, properties)} />\n"
            return

        inner = str(inner).replace('&', '&amp;')

        if "\n" not in str(inner):
            self.buffer += f"<{self.format_properties(tag, properties)}>{inner}</{tag}>\n"
        else:
            self.buffer += f"<{self.format_properties(tag, properties)}>"
            self.buffer += f"\n{inner}\n"
            self.append_indentation()
            self.buffer += f"</{tag}>\n"

        return self

    def context(self, tag: str, **properties):
        return XmlContextManager(tag, properties, self)

    def open_close_tag(self, tag: str, **properties):
        self.append_indentation()
        self.buffer += f"<{self.format_properties(tag, properties)}>\n"

    def enter(self, tag: str, **properties):
        self.open_close_tag(tag, **properties)
        self.level += 1
        return self

    def exit(self, tag: str):
        self.level -= 1
        self.open_close_tag(f"/{tag}")
        return self

    def append_dict(self, tag: str, content: Dict, prop: str):
        """
        Serializes a dictionary. 
        :param tag: Tag name to be used for dict items.
                    The container tag will have a pluralized version.
        :param content: Dictionary to be serialized. Keys turn into
                        properties, values into content between the tags.
        :param prop: Name of the property the dictionary key is serialized as.
        :return: XmlWriter
        """
        if not content:
            self.tag(XmlWriter.pluralize(tag), None)
        else:
            with self.context(XmlWriter.pluralize(tag)):
                for name, value in content.items():
                    self.tag(tag, value, **{prop: name})
        return self

    def append_object(self, obj: 'XmlSerializable', extended: bool = False):
        obj.append_xml(self, extended)
        return self
