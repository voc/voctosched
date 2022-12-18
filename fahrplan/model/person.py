from dataclasses import InitVar, dataclass, field, fields
from typing import Optional, Union
import uuid

from fahrplan.uuid import NAMESPACE_VOCTOSCHED


@dataclass
class Person:
    """A person e.g. speaker, contributor etc."""

    name: str
    "public name of the person"
    guid: InitVar[Optional[str]] = None
    "global unique idenifier, might be automatically computed from uri, email, id or code"
    _guid: Optional[uuid.UUID] = field(init=False, repr=False, default=None)
    "internal storage place if we got a precomputed person guid from origin system"
    _uri: Optional[str] = field(init=False, repr=False, default=None)
    "URL, URN or other URI identifing this person"
    email: Optional[str] = None
    "public email address, used as base for URI/GUID when nothing else is set"
    id: Optional[int] = None
    "deprecated: integer id of this person in the origin system"
    code: Optional[str] = None
    "deprecated: pretalx internal 5 char random id of this person in the origin system, e.g. `DEFAB`"

    # avatar: Optional[str] = None
    # biography: Optional[str] = None
    # links: Optional[List[Any]] = None
    # contacts: Optional[List[Any]] = None
    # state: Optional[str] = None

    origin_system: Optional[str] = None
    "internet domain of system this entity originating from, e.g. `frab.cccv.de`"

    def __post_init__(self, guid):
        if type(guid) == str or type(guid) == uuid.UUID:
            self._guid = guid

    @classmethod
    def from_dict(cls, data: dict):
        assert isinstance(data, dict), 'Data must be a dictionary.'

        # older schedule versions used other keys for public person name
        name = data.get('name') or data.get('public_name') or data.get('full_public_name')

        fieldSet = {f.name for f in fields(cls) if f.init and f.name != 'name'}
        fieldSet.add('guid')
        filteredData = {k: v for k, v in data.items() if k in fieldSet}

        # support shorthand of previous `origin_system` key
        if 'origin' in data:
            filteredData['origin_system'] = data['origin']

        return Person(name, **filteredData)

    @property
    def uri(self):
        # if we got a precomputed person URID from the origin system, stay consistent
        if self._uri:
            return self._uri

        if self.email:
            return f"acct:{self.email}"

        if (self.id or self.code) and self.origin_system:
            # TODO person vs people
            return f'urn:{self.origin_system}:person:{self.id or self.code}'

        if self._guid:
            return f'urn:uuid:{self._guid}'

        return None

    @uri.setter
    def uri(self, value):
        # TODO: raise exception if value is not an URI
        self._uri = value

    @property
    def guid(self) -> str:
        # if we got a precomputed person guid from the origin system, stay consistent
        if self._guid:
            return str(self._guid)

        uri = self.uri
        if uri:
            return uuid.uuid5(uuid.NAMESPACE_URL, uri).__str__()

        # we tried everything else, so fall back to hash of person name
        return uuid.uuid5(NAMESPACE_VOCTOSCHED, self.name).__str__()

    @guid.setter
    def guid(self, value: Union[str, uuid.UUID]):
        if type(value) != uuid.UUID:
            self._guid = uuid.UUID(value)
        else:
            self._guid = value

# used resources:
# https://stackoverflow.com/a/61480946
# https://medium.com/swlh/python-dataclasses-with-properties-and-pandas-5c59b05e9131