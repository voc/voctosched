import uuid as _uuid


uuid_namespace = _uuid.UUID('54dc9c85-9b6a-40bd-9a36-41c004a5829b')


def uuid(uid, name):
    return str(_uuid.uuid5(uuid_namespace, str(name)+str(uid)))
