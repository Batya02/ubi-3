import re 

def phone_format(arg:str):
    phone = re.sub("[^0-9]", "", arg)
    return phone