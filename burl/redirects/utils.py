import secrets

from django.conf import settings

from hashids import Hashids


hashid_hasher = Hashids(salt=settings.HASHID_SALT, alphabet=settings.HASHID_ALPHABET)


def make_burl(record_count):
    """
    Generates a non-unique burl short url

    :param record_count: number of records in the database
    :return: burl short url
    :rtype: str
    """
    salt = secrets.token_hex(4)
    hasher = Hashids(salt=salt, alphabet=settings.HASHID_ALPHABET)
    random = secrets.randbelow(record_count + 1000)
    return hasher.encode(random)
