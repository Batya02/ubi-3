from datetime import datetime as dt

def datetime_format(arg) -> str:
    """Formating datetime

    :param: Get datetime from db
    :type arg:?
    :return: Formated datetime
    :rtype: str

    """

    if not arg:
        return None 

    return dt.strftime(arg, "%Y-%m-%d %H:%M:%S")