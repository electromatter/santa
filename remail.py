#!/usr/bin/env python3

'Simple script to send a specific person an email'

import argparse
import pprint

import util


def main(argv=None):
    'Parse args and send emails'

    parser = argparse.ArgumentParser()
    parser.add_argument('contacts', help='Contacts file', type=argparse.FileType('r'))
    parser.add_argument('cycle', help='Cycle secret', type=argparse.FileType('r'))
    parser.add_argument('gifter', nargs='?', help='Gifter to re-mail (omit to list possible values)')

    args = parser.parse_args(argv)

    if args.gifter is None:
        show_gifters(args.contacts, args.cycle)
        return

    remail(args.gifter, args.contacts, args.cycle)


def remail(gifter, contactsfile, cyclefile):
    'Remail a specific gifter their gift recipient'
    contacts = util.parse_contacts(contactsfile)
    cycle = util.parse_cycle(cyclefile)
    cycle_dict = util.cycle_as_dict(cycle)
    gifter_info = contacts[gifter]
    recipient_info = contacts[cycle_dict[gifter]]
    util.send_mail(gifter_info, recipient_info)


def show_gifters(contactsfile, cyclefile):
    'Show the available contacts for a given secret'
    contacts = util.parse_contacts(contactsfile)
    cycle = set(util.parse_cycle(cyclefile))
    available = {name: contact for name, contact in contacts.items() if name in cycle}
    pprint.pprint(available)


if __name__ == '__main__':
    main()
