from django.conf import settings

from hashids import Hashids


hashid_hasher = Hashids(salt=settings.HASHID_SALT, alphabet=settings.HASHID_ALPHABET)


def hashid_encode(*args):
    """
    Encodes args as a hashid string using our settings.

    :param args: arguments (integers) to be encoded
    :return: encoded hashid
    :rtype: str
    """
    return hashid_hasher.encode(*args)


def hashid_decode(hashid):
    """
    Decode a hashid string to a set of integer values using our settings.

    :param hashid: a hashid string
    :type hashid: str
    :return: decoded values
    :rtype: tuple
    """
    return hashid_hasher.decode(hashid)
