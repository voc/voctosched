class XmlSerializer:
    # TODO (AK) add type annotation, rename indent to indent_style to match attribute
    def __init__(self, indent="  "):
        self.indent_style = indent
        self.buffer = ""
        # TODO (AK) rename to indent_level or rename all occurrences of indent* to indentation*
        self.level = 0

    def indent(self):
        return self.indent_style * self.level

    # TODO (AK) add type annotation for inner
    def tag(self, tag: str, inner, **kwargs):
        # TODO (AK) put all expressions on the right-hand-sides into format strings and don't concatenate with +
        start = self.indent() + f"<{tag}"
        # TODO (AK) rename k and v so that their names represent their actual meanings
        for k, v in kwargs.items():
            start += f' {k}="{v}"'
        # TODO (AK) change to "if inner" and exchange bodies
        if not inner:
            self.buffer += start + " />\n"
        else:
            self.buffer += start + f">{inner}</{tag}>\n"

    # TODO (AK) rename to open_close_tag or something similar
    def inout(self, tag: str, **kwargs):
        start = self.indent() + f"<{tag}"
        # TODO (AK) rename k and v so that their names represent their actual meanings
        for k, v in kwargs.items():
            start += f' {k}="{v}"'
        self.buffer += start + ">\n"

    def enter(self, tag: str, **kwargs):
        self.inout(tag, **kwargs)
        self.level += 1

    def exit(self, tag: str):
        self.level -= 1
        self.inout(f"/{tag}")

    # TODO (AK) don't use a built-in name
    # TODO (AK) add type annotation for content and prop
    def dict(self, tag: str, content, prop):
        # TODO (AK) document how the given content is serialized in detail
        if not content:
            self.tag(tag + "s", None)
        else:
            self.enter(tag + "s")
            # TODO (AK) rename k and v so that their names represent their actual meanings
            for k, v in content.items():
                self.tag(tag, v, **{prop: k})
            self.exit(tag + "s")
