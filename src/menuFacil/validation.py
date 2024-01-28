import uuid
from django.http import QueryDict

def contains(post: QueryDict, keys: list[str]) -> bool:
    return set(keys).issubset(post.keys())

def valid_uuid(uuid_to_test: str) -> bool:
    try:
        uuid.UUID(uuid_to_test)
        return True
    except ValueError:
        return False
