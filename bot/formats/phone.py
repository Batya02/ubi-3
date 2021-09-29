import re 

def phone_format(phone: str) -> str:
    """ Formating phone
    :param: Get user phone
    :type: str
    :return: Formated user phone
    :rtype: str
    """
    
    phone = re.sub("[^0-9]", "", phone)
    return phone