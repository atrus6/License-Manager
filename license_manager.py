import argparse
import hashlib
import sqlite3

def xstr(string, nrep=''):
    if string == None:
        return nrep
    else:
        return string

def calculate_MD5(file_handler):

    file_hash = hashlib.md5()
    file_hash.update(file_handler.read())

    return file_hash.hexdigest()

def create_table(cursor):
    cursor.execute('CREATE TABLE media   \
                (name TEXT,              \
                md5 TEXT,                \
                license TEXT,            \
                url TEXT,                \
                file BLOB,               \
                ancestor_name TEXT,      \
                ancestor_md5 TEXT,       \
                PRIMARY KEY(name, md5))')

def open_database(db):
    con = None
    cursor = None

    if db == None:
        con = sqlite3.connect('media.db')
    else:
        con = sqlite3.connect(db)

    cursor = con.cursor()

    #Test if the table exists or we just opened up something new.
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="media"')
    table_exists = cursor.fetchone()

    if table_exists == None:
        create_table(cursor)

    return con, cursor



def insert_item(file_handle, filename, file_md5, license, url, ancestor_name, ancestor_md5, db):
    con, cursor = open_database(db)

    cursor.execute('INSERT INTO media (name, md5, file, license, url, ancestor_name, ancestor_md5)\
            VALUES (?, ?, ?, ?, ?, ?, ?)',
            (filename,
                str(file_md5),
                file_handle.read(),
                license, url,
                ancestor_name, ancestor_md5))

    con.commit()
    cursor.close()

def list_items(license, ancestor, url, database):
    con, cursor = open_database(database)
    cstr = ''
    if license != None:
        cstr = cstr + 'license = "' + license + '" '

    if ancestor != None:
        ancestor_name = ancestor.name
        ancestor_md5 = calculate_md5(ancestor)
        cstr = cstr + 'ancestor_name = "' + ancestor_name + '" '

    if url != None:
        cstr = cstr + 'url = "' + url + '" '

    if cstr != '':
        cursor.execute('SELECT name, license, url, ancestor_name FROM media WHERE ' + cstr)
    else:
        cursor.execute('SELECT name, license, url, ancestor_name FROM media')

    labels = ['Name: ', 'License: ', 'URL: ', 'Ancestor: ']
    for row in cursor:
        print(labels[0] + xstr(row[0], 'None') + ' ' + labels[1] + xstr(row[1], 'None') + ' ' +
                labels[2] + xstr(row[2], 'None') + ' ' + labels[3] + xstr(row[3], 'None'))


def main():
    license_names = ['CC-BY', 'CC-BY-SA', 'GPL3', 'GPL2', 'CC0']
    parser = argparse.ArgumentParser(
            description='Handles media licensing information')

    subparsers = parser.add_subparsers()

    parser_add = subparsers.add_parser('add', help='Adds a new piece of media.')
    parser_add.set_defaults(which='add')

    parser_add.add_argument('file', action='store',
            type=argparse.FileType('rb'),
            help='The file path of the media to be added.')
    parser_add.add_argument('license', action='store',
            choices=license_names,
            help='The license the media is under.')
    parser_add.add_argument('-u', '--url', action='store', dest='url',
            help='The attribution URL for the media.')
    parser_add.add_argument('-a', '--ancestor', action='store', dest='ancestor',
            type=argparse.FileType('rb'),
            help='The file path of the parent of this derivitive work.')

    parser_add.add_argument('-d', '--database', action='store', dest='database',
            type=argparse.FileType('r+'),
            help=('Database to work on. If none give, the assumed location is \
                ./media.db'))

    parser_list = subparsers.add_parser('list', help='Lists media in database.')
    parser_list.set_defaults(which='list')

    parser_list.add_argument('-l', '--license', action='store', dest='license',
            choices=license_names,
            help="List by license types")
    parser_list.add_argument('-a', '--ancestor', action='store', dest='ancestor',
            help='List by common ancestor.')
    parser_list.add_argument('-u', '--url', action='store', dest='url',
            help='List by attribution URL.')
    parser_list.add_argument('-d', '--database', action='store', dest='database',
            help='Location of database. Assumes ./models.db if not present.')

    args = parser.parse_args()

    if args.which == 'add':
        #Calculate MD5 of the new file.
        md5 = calculate_MD5(args.file)
        name = args.file.name
        ancestor = args.ancestor
        ancestor_name = None
        ancestor_md5 = None

        if ancestor != None:
            ancestor_name = ancestor.name
            ancestor_md5 = calculate_MD5(ancestor)

        insert_item(args.file, name, md5, args.license, args.url, ancestor_name, ancestor_md5, args.database)
    elif args.which == 'list':
        list_items(args.license, args.ancestor, args.url, args.database)

if __name__ == '__main__':
    main()

