import re
import csv

from tkinter import filedialog


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
    records.append( {
      'mts_date'       : row[ 'Transactiedatum' ],
      'mts_amount'     : row[ 'Transactiebedrag' ],
      'mts_description': row[ 'Omschrijving' ],
      'mts_start'      : row[ 'Beginsaldo' ],
      'mts_category'   : 0
    } )

  csv_file.close()

  return records


def csv_get_filename() -> str:
  return filedialog.askopenfilename(
    title = 'Open CSV File',
    filetypes = [ ('CSV Files', '*.csv') ]
  )
