License Manager
===============

A simple python script that help keep track of a larger
amount of licensed work, as opposed to a simple txt file.

Creates a database called 'media.db' in current directory
if a database does not exist. Alternate locations can be
specified with -d.

Requires python3 and sqlite

To use
------

python license_manager.py add path/to/file license

This adds a file to the database. There are optional tags

* -u/--url adds an attribution URL
* -a/--ancestor adds a parent work
* -d/--database specifies an alternate database location.

python license_manager.py list

This lists all of the stored files. Filtering is possible
with optional tags

* -l/--license filters by license type
* -u/--url filters by attribution URL
* -a/--ancestor filters by ancestor

TODO
----

* Ability to extract added files.
* Add more license types.
* Ability to remove files
