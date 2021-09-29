from objects import globals
from base64 import b85decode

def decode_host(hash_host: str) -> str:
    """Decoding host

    :param: Get hash host (url)
    :type: str
    :return: Already decoded host
    :rtype: str

    """

    decode_hash_host = (b85decode(hash_host).decode("utf-8")
    [len(globals.config["services_url_hash_key"].split("::")[0]):]
    [:-len(globals.config["services_url_hash_key"].split("::")[1])])

    return decode_hash_host