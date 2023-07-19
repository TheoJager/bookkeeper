from tkinter import *

from application.csv.csv_upload import csv_get_filename, csv_to_records
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories

root = Tk()
root.title( 'bookkeeper' )
root.iconbitmap( 'D:/python/bookkeeper/favicon.ico' )
root.geometry( '1000x600' )


# pyinstaller --onefile --noconsole --icon=favicon.ico main.py


def get( dictionary, key, default = None ):
  return dictionary[ key ] if key in dictionary.keys() else default


# BOOKKEEPER
#######################################

name = Label( text = "Bookkeeper" )
name.grid( row = 0, column = 0, columnspan = 1, sticky = 'nsew' )

import locale
import datetime

x = datetime.datetime.now()

locale.setlocale( locale.LC_TIME, "nl_NL" )

date = Label( text = x.strftime( "%B %Y" ) )
date.grid( row = 0, column = 1, columnspan = 1, sticky = 'nsew' )

# IMPORT EXCEL
# create database
# add mutations to database
#######################################

Database_Mutations.create_table_if_not_exists()


def csv_to_database():
  records = csv_to_records( csv_get_filename() )
  for record in records:
    try:
      Database_Mutations.insert( record )
    except Exception:
      continue


upload_csv = Button( root, text = 'Upload CSV File', command = csv_to_database )
upload_csv.grid( row = 1, column = 0, columnspan = 1, sticky = 'nsew' )


# MUTATIONS
# add categories (ai)
#######################################

def add_categories():
  pass


records_to_categories = Button( root, text = 'Voeg categorien toe', command = add_categories )
records_to_categories.grid( row = 2, column = 0, columnspan = 1, sticky = 'nsew' )

# IMPORT EXCEL
# basis bedrag
# toevoegen records
# check dubbel
# toevoegen aan categorie (ai)
# initieer tabellen
#######################################

# LABEL
# deze maand
# bedrag op rekening
#######################################

# CATEGORIE
# initialize categories
#######################################

Database_Categories.create_table_if_not_exists()

records = [
  {
    'ctr_name'  : 'Incidenteel',
    'ctr_income': 0,
  },
  {
    'ctr_name'  : 'Eten',
    'ctr_income': 0,
  },
  {
    'ctr_name'  : 'Boodschappen',
    'ctr_income': 0,
  },
  {
    'ctr_name'  : 'Abonnementen',
    'ctr_income': 0,
  },
  {
    'ctr_name'  : 'Kosten',
    'ctr_income': 0,
  },
  {
    'ctr_name'  : 'Sparen',
    'ctr_income': 0,
  },
  {
    'ctr_name'  : 'Beleggingen',
    'ctr_income': 0,
  },
  {
    'ctr_name'  : 'Salaris',
    'ctr_income': 1,
  },
]
for record in records:
    try:
      Database_Categories.insert( record )
    except Exception:
      continue

# CATEGORIE
# bedragen deze maand
#######################################

# CATEGORIE
# bedragen alle maanden
# aanklikbare staven
#######################################

# MAANDEN
# navigatie nu, vorige, volgende
#######################################

# OVERZICHT
# deze maand
# per categorie deze maand
#######################################


if __name__ == '__main__':
  root.mainloop()
