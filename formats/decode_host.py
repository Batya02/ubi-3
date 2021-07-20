from objects import globals
from base64 import b85decode

def decode_host(hash_host:str) -> str:
    
    decode_hash_host = b85decode(hash_host).decode("utf-8") \
    [len(globals.config["services_url_hash_key"].split("::")[0]):] \
    [:-len(globals.config["services_url_hash_key"].split("::")[1])]

    return decode_hash_host
