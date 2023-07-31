import re
import csv
import sqlite3

from random import randrange
from tkinter import filedialog
from application.ui.message import Message
from application.database.database_mutations import Database_Mutations


def csv_get_header( path: str ) -> str:
  csv_file = open( path, 'r' )

  header = csv_file.readline()

  csv_file.close()
  return header


def csv_get_delimiter( header: str ) -> str:
  delimiter = re.search( r'Rekeningnummer(.+)Muntsoort', header, re.IGNORECASE )
  return delimiter.group( 1 )


def csv_to_records( path: str ) -> list:
  delimiter = csv_get_delimiter( csv_get_header( path ) )

  csv_file = open( path, 'r' )

  records = [ ]
  for row in csv.DictReader( csv_file, delimiter = delimiter ):
    record = {
      'mts_date'  : row[ 'Transactiedatum' ],
      'mts_amount': csv_convert_numbers( row[ 'Transactiebedrag' ] ),
      'mts_start' : csv_convert_numbers( row[ 'Beginsaldo' ] ),
      'mts_text'  : csv_sanitize( row[ 'Omschrijving' ] ),
      'ctr_id'    : randrange( 1, 8 )
    }
    records.append( record )

  csv_file.close()

  return records


def csv_sanitize( text: str ) -> str:
  text = re.sub( r"[\t\r\n]+", ' ', text )
  text = re.sub( r"\s+", ' ', text )
  return text


def csv_to_database():
  filename = csv_get_filename()
  if len( filename ):
    records = csv_to_records( filename )
    Database_Mutations.insert_base_value( records[ 0 ] )
    for record in records:
      try:
        Database_Mutations.insert( record )
      except sqlite3.IntegrityError:
        continue
    Message.ok( 'result', 'import successful' )


def csv_convert_numbers( number: str ):
  return number.replace( ",", "." )


def csv_get_filename() -> str:
  return filedialog.askopenfilename(
    title = 'Open CSV File',
    filetypes = [ ('CSV Files', '*.csv') ]
  )
