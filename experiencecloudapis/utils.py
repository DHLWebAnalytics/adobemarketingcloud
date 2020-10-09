import typing
import datetime


def lower_keys(obj: dict) -> dict:
    """
    Lowercase first level keys of a dictionary

    :param obj: object to be lowercased
    :return: same object with lowercase keys in first level
    """
    nu_obj = dict()
    for key in obj:
        nu_obj[key.lower()] = obj[key]
    return nu_obj


def read_file_or_string(filepath_or_file: typing.Union[str, typing.TextIO]) \
        -> str:
    """
    Reads a file or filepath and opens and returns the content

    :param filepath_or_file: file or filepath that needs to be read
    :return: file content
    """
    if getattr(filepath_or_file, "read", None):
        try:
            return filepath_or_file.read()
        except ValueError:
            with open(filepath_or_file.name, "r", encoding="UTF-8") as fd:
                return fd.read()
    with open(str(filepath_or_file), "r", encoding="UTF-8") as fd:
        return fd.read()


def now_in_ms(date: datetime.datetime = datetime.datetime.now()) -> int:
    """
    Returns datetime into ms ISO format

    :param date: desired datetime object
    :return: date in ms ISO format
    """
    return int(date.timestamp() * 1000)
