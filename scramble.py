#!/usr/bin/env python3

'Simple script to generate a random cycle of names'

import argparse
import sys
import json

import util

def main(argv=None):
    "Parse args and create a random cycle"
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', dest='output', metavar='output', help='Output file (Default to stdout)', type=argparse.FileType('w'), default=sys.stdin)
    parser.add_argument('names', nargs='?', help='Input names file to scramble (Default to stdin)', type=argparse.FileType('r'), default=sys.stdin)

    args = parser.parse_args(argv)

    scramble(args.names, args.output)


def scramble(infile=sys.stdin, outfile=sys.stdout):
    "Scramble the contacts into a random cycle and put it to the output"
    contacts = util.parse_contacts(infile)
    cycle = util.random_cycle(contacts)
    json.dump(cycle, outfile)


if __name__ == '__main__':
    main()
