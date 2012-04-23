import argparse
import hashlib
import sqlite3

def calculate_MD5(file_handler):

    file_hash = hashlib.md5()
    while True:
        try:
            file_hash.update(args.filename.read(8192))
        except:
            break

    return file_hash.digest()

def main():
    parser = argparse.ArgumentParser(
            description='Handles media licensing information')

    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser('add', help='Adds a new piece of media.')

    parser_add.add_argument('file', action='store',
            type=argparse.FileType('r'),
            help='The file path of the media to be added.')
    parser_add.add_argument('license', action='store',
            choices=['CC-BY', 'CC-BY-SA', 'GPL3', 'GPL2', 'CC0'],
            help='The license the media is under.')
    parser_add.add_argument('-u', '--url', action='store', dest='url',
            help='The attribution URL for the media.')
    parser_add.add_argument('-a', '--ancestor', action='store', dest='ancestor',
            nargs='?', type=argparse.FileType('r'),
            help='The file path of the parent of this derivitive work.')

    args = parser.parse_args()
    #Calculate MD5 of the new file.
    md5 = calculate_MD5(args.filename)
    name = args.filename.name
    license = args.license
    ancestor = args.ancestor
    ancestor_name = ancestor.name
    ancestor_md5 = calculate_MD5(ancestor)

    #insert_item(args.filename, name, md5, license, ancestor_name, ancestor_md5)

if __name__ == '__main__':
    main()

