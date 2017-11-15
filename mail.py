#!/usr/bin/env python3

'Simple script to mail everyone their giftee'

import argparse

import util


def main(argv=None):
    'Parse args and send emails'

    parser = argparse.ArgumentParser()
    parser.add_argument('contacts', help='Contacts file', type=argparse.FileType('r'))
    parser.add_argument('cycle', help='Cycle secret', type=argparse.FileType('r'))

    args = parser.parse_args(argv)

    mail(args.parser.contacts, args.cycle)


def mail(contactsfile, cyclefile):
    'Mail all participants in cyclefile using their email in contactsfile'
    contacts = util.parse_contacts(contactsfile)
    cycle = util.parse_cycle(cyclefile)
    for gifter, gift_recipient in util.cycle_as_dict(cycle).items():
        gifter_info = contacts[gifter]
        recipient_info = contacts[gift_recipient]
        util.send_mail(gifter_info, recipient_info)
	print('Mailed to', gifter)


if __name__ == '__main__':
    main()
