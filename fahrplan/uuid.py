import uuid as _uuid

NAMESPACE_VOCTOSCHED = _uuid.UUID('54dc9c85-9b6a-40bd-9a36-41c004a5829b')


def uuid(uid, name):
    # TODO (AK) please document this method in detail and what the uuid namespace is for
    return str(_uuid.uuid5(NAMESPACE_VOCTOSCHED, f"{name}{uid}"))
