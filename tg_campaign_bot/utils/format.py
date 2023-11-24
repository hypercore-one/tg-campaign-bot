import datetime
from dateutil import parser


def sanitize_output(text):
    escape_chars = ['!', '-', '#', '.', '>', '=', '(', ')', '[', ']', '|', '@', '_', '+', '{', '}']
    for c in escape_chars:
        text = text.replace(c, f'\\{c}')
    return text


def format_post_criteria(arr):
    if len(arr) == 1:
        return arr[0].replace("'", '')

    response = ''
    for tag in arr:
        response += f'{tag.replace("'", '')}, '
    return response[:-2]


def format_tags(arr):
    response = ''
    for tag in arr:
        response += f'{tag.replace("'", '')}, '
    return response[:-2]


def format_links(arr):
    response = ''
    for link in arr:
        response += f'    - {link.replace("'", '')}\n'
    return response


def format_time(end_time):
    return str(datetime.timedelta(
        seconds=round(
            parser.parse(end_time).timestamp() - datetime.datetime.timestamp(datetime.datetime.now(datetime.UTC)))))
