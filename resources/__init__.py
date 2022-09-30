# -*- coding: utf-8 -*-

"""Resources __init__ module."""
from resources.lib.database.createtables import DBCreateTables

# A quick way to create the tables on opening the script
# avoids the need to call this function in multiple different locations
DBCreateTables()
