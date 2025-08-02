from fahrplan.model.person import Person


def test_minimal_person():
    person = Person(name="Alice")
    assert person.guid == "71bc5e0c-582a-5442-aa86-ff0b3e7cc2bd"


def test_person_guid():
    person = Person(name="Alice", guid="f4c4c716-7ee6-11ed-aa36-6c400891b752")
    assert person.guid == "f4c4c716-7ee6-11ed-aa36-6c400891b752"
    # we have no other information about the origin system, so the URI falls back to the UUID
    assert person.uri == "urn:uuid:f4c4c716-7ee6-11ed-aa36-6c400891b752"


def test_person_from_dict_with_guid():
    person = Person.from_dict(
        {"name": "Alice", "guid": "f4c4c716-7ee6-11ed-aa36-6c400891b752", "id": 123, "origin": "domain.tld"}
    )
    assert person.guid == "f4c4c716-7ee6-11ed-aa36-6c400891b752"
    assert person.uri == "urn:domain.tld:person:123"


def test_classic_frab_person():
    data = {"id": 7797, "public_name": "royce"}
    person = Person.from_dict(data)
    assert person.name == "royce"
    assert person.uri is None
    assert person.guid == "00d95612-6fe0-56f9-a9b5-2c9ed405abec"

    person.origin_system = "frab.cccv.de"
    assert person.uri == "urn:frab.cccv.de:person:7797"
    assert person.guid == "d04f5971-648b-5aa6-af6d-843b38a6bb54"


def test_pretalx_person_from_dict():
    data = {
        "name": "Jane",
        "code": "DEFAB",
        "biography": "A speaker",
        "avatar": "avatar.png",
    }
    person = Person.from_dict(data)
    person.origin_system = "pretalx.com"
    assert person.name == "Jane"
    assert person.uri == "urn:pretalx.com:person:DEFAB"
    assert person.guid == "2d818073-0a8a-5240-952a-e81e0cd19766"


def test_full_frab_person_from_dict():
    data = {
        "id": 100,
        "name": "Royce",
        "full_name": "Royce Jakubowski",
        "email": "royce_jakubowski@example.net",
        "avatar": None,
        "biography": "Royce Jakubowski is a well-respected tech conference speaker with over a decade of experience in the industry. He has a deep understanding of a wide range of technologies, from software development to data analytics, and is known for his engaging and informative presentations.",
        "links": [{"url": "https://domain.tld", "title": "title"}],
        "contacts": [],
        "state": "unclear",
        "availabilities": [
            {"start": "2021-10-20T11:00:00+02:00", "end": "2021-10-20T17:00:00+02:00"}
        ],
        "url": "http://localhost:3000/en/democon/people/100",
    }
    person = Person.from_dict(data)
    assert person.name == "Royce"
    assert person.uri == "acct:royce_jakubowski@example.net"
    assert person.guid == "6b4d383e-70f5-5a7a-8b38-3d168d02210f"
