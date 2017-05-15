class XmlSerializer:
    def __init__(self, indent="  "):
        self.indent_style = indent
        self.buffer = ""
        self.level = 0

    def indent(self):
        return self.indent_style * self.level

    def tag(self, tag: str, inner, **kwargs):
        start = self.indent() + f"<{tag}"
        for k, v in kwargs.items():
            start += f' {k}="{v}"'
        if not inner:
            self.buffer += start + " />\n"
        else:
            self.buffer += start + f">{inner}</{tag}>\n"

    def inout(self, tag: str, **kwargs):
        start = self.indent() + f"<{tag}"
        for k, v in kwargs.items():
            start += f' {k}="{v}"'
        self.buffer += start + ">\n"

    def enter(self, tag: str, **kwargs):
        self.inout(tag, **kwargs)
        self.level += 1

    def exit(self, tag: str):
        self.level -= 1
        self.inout(f"/{tag}")

    def dict(self, tag: str, content, prop):
        if not content:
            self.tag(tag + "s", None)
        else:
            self.enter(tag + "s")
            for k, v in content.items():
                self.tag(tag, v, **{prop: k})
            self.exit(tag + "s")
