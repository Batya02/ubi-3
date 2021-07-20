from datetime import datetime as dt

def datetime_format(arg) -> str:
    return dt.strftime(arg, "%Y-%m-%d %H:%M:%S")