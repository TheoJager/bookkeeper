import csv

from tkinter import filedialog


def csv_to_records( path: str ) -> list:
  # @TODO dynamically determine delimiter
  csv_file = open( path, 'r' )

  records = [ ]
  for row in csv.DictReader( csv_file, delimiter = ';' ):
    records.append( {
      'mts_date'       : row[ 'Transactiedatum' ],
      'mts_amount'     : row[ 'Transactiebedrag' ],
      'mts_description': row[ 'Omschrijving' ],
      'mts_category'   : 0
    } )

  csv_file.close()

  return records


def csv_get_filename() -> str:
  return filedialog.askopenfilename(
    title = 'Open CSV File',
    filetypes = [ ('CSV Files', '*.csv') ]
  )
