def ind(level: int):
    return "  " * level


def xml(tag: str, inner, level: int = 0, **kwargs):
    start = ind(level) + f"<{tag}"
    for k, v in kwargs.items():
        start += f' {k}="{v}"'
    if inner is None or inner == "":
        return start + " />\n"
    return start + f">{inner}</{tag}>\n"


def xml_open(tag: str, level: int = 0, **kwargs):
    start = ind(level) + f"<{tag}"
    for k, v in kwargs.items():
        start += f' {k}="{v}"'
    return start + ">\n"


def xml_close(tag: str, level: int = 0):
    return xml_open(f"/{tag}", level)


def xml_dict(tag: str, content, prop, level: int = 0):
    if not content:
        return xml(tag + "s", None, level)
    result = xml_open(tag + "s", level)
    for k, v in content.items():
        result += xml(tag, v, level + 1, **{prop: k})
    result += xml_close(tag + "s", level)
    return result
