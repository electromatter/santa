import json
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def parse_contacts(file):
    'Parse contact dict(short_name=dict(name="Eric Chai", address="<address>", email="electromatter@gmail.com"), ...)'
    contacts = json.load(file)
    if not isinstance(contacts, dict):
        raise TypeError('expected contacts to be a dict')
    for name, contact in contacts.items():
        for key in ('address', 'name', 'email'):
            if key not in contact:
                raise ValueError('Bad contact: %r missing info %s' % (name, key))
    return contacts


def parse_cycle(file):
    'Parse the cycle'
    cycle = json.load(file)
    if not hasattr(cycle, '__iter__'):
        raise TypeError('expected cycle to be an iterable')
    return cycle


def random_cycle(keys):
    '''Create a random cycle based on a list of keys

    A cycle is a list of names that wraps around, for example
    the list: ['spam', 'foo', 'baz'] indicates the gift cycle
    where:
     - spam gifts foo
     - foo gifts baz
     - baz gifts spam
    '''
    keys = list(keys)
    random.shuffle(keys)
    return keys


def cycle_as_dict(cycle):
    'Return a dict {gifter: gift_recipient} from the cycle'
    it = iter(cycle)
    result = {}

    try:
        # Save the first
        gifter = first = next(it)
    except StopIteration:
        return result

    try:
        while True:
            # Link in order pairs
            gift_recipient = next(it)
            result[gifter] = gift_recipient
            gifter = gift_recipient
    except StopIteration:
        # Reached the last, link it back to the first
        result[gifter] = first

    return result


def parse_tempate(file):
    template = json.load(file)
    for key in ('header', 'body'):
        if key not in template:
            raise ValueError('template missing section: %s' % key)
    for key in ('From', 'To', 'Subject'):
        if key not in template['header']:
            raise ValueError('template missing header: %s' % key)
    return template


TEMPLATE = dict(
    header=dict(
        From='santa-bot@electromatter.info',
        To='{gifter[email]}',
        Subject='Have you ever heard of the tragedy of Secret Santa?'),
    body='''
Dear {gifter[name]},

You are gifting:
{recipient[name]}
{recipient[address]}

Thank you for participating in Secret Santa!

Sincerely,
The Have-you-ever-heard-of-the-tragedy-of Secret Santa Bot
''')


def format_message(gifter, recipient, template=None):
    'Create SMTP message from template'

    if not template:
        template = TEMPLATE

    # Setup the header
    message = MIMEMultipart()
    for key, value in template['header'].items():
        message[key] = val = value.format(gifter=gifter, recipient=recipient)

    # Make the body
    body = template['body'].format(gifter=gifter, recipient=recipient)
    message.attach(MIMEText(body))

    return message


def send_mail(gifter_info, recipient_info, template=None, server='localhost'):
    'Send an email based on the template and the info'

    message = format_message(gifter_info, recipient_info, template)

    with smtplib.SMTP(server) as s:
        s.send_message(message)
