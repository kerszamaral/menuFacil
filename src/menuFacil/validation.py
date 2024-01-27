import uuid
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.contrib.sessions.backends.base import SessionBase
from django.http import QueryDict

TAB_KEY = 'tab_token'
TAB_REDIRECT_URL = "tab:present"


def tab_token_exists(session: SessionBase, user: AbstractBaseUser | AnonymousUser) -> bool:
    if user.is_authenticated:
        session[TAB_KEY] = str(user.tab.id) # type: ignore
        return True

    if TAB_KEY in session.keys():
        return True

    return False

def post_contains_keys(post: QueryDict, keys: list[str]) -> bool:
    return set(keys).issubset(post.keys())

def validate_UUID(uuid_to_test: str) -> bool:
    try:
        uuid.UUID(uuid_to_test)
        return True
    except ValueError:
        return False
