import uuid as _uuid

# TODO (AK) rename to UUID_NAMESPACE as this is a global constant?
uuid_namespace = _uuid.UUID('54dc9c85-9b6a-40bd-9a36-41c004a5829b')


def uuid(uid, name):
    # TODO (AK) please document this method in detail and what the uuid namespace is for
    # TODO (AK) use format string for concatenation of name and uid
    # f"{name}{uid}"
    return str(_uuid.uuid5(uuid_namespace, str(name) + str(uid)))
