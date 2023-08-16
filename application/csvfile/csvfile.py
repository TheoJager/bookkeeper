import re
import csv
import sqlite3
import globals as glb

from tkinter import filedialog
from view.view import View
from ui.message import Message
from database.database_mutations import Database_Mutations


class CSVFile:

  @staticmethod
  def to_database():
    filename = CSVFile.get_filename()
    if len( filename ):
      records = CSVFile.to_records( filename )
      Database_Mutations.insert_base_value( records[ 0 ] )
      for record in records:
        try:
          Database_Mutations.insert( record )
        except sqlite3.IntegrityError:
          continue

      View.initiate()
      View.update( glb.SELECTED_MONTH )
      Message.ok( 'result', 'import successful' )

  @staticmethod
  def get_filename() -> str:
    return filedialog.askopenfilename(
      title = 'Open CSV File',
      filetypes = [ ('CSV Files', '*.csv') ]
    )

  @staticmethod
  def to_records( path: str ) -> list:
    delimiter = CSVFile.get_delimiter( CSVFile.get_header( path ) )

    csv_file = open( path, 'r' )

    records = [ ]
    for row in csv.DictReader( csv_file, delimiter = delimiter ):
      record = {
        'mts_date'  : row[ 'Transactiedatum' ],
        'mts_amount': CSVFile.convert_numbers( row[ 'Transactiebedrag' ] ),
        'mts_start' : CSVFile.convert_numbers( row[ 'Beginsaldo' ] ),
        'mts_text'  : CSVFile.sanitize( row[ 'Omschrijving' ] ),
        # 'ctr_id'    : CSVFile.get_category( row[ 'Omschrijving' ] )
      }
      records.append( record )

    csv_file.close()

    return records

  @staticmethod
  def get_header( path: str ) -> str:
    csv_file = open( path, 'r' )

    header = csv_file.readline()

    csv_file.close()
    return header

  @staticmethod
  def get_delimiter( header: str ) -> str:
    delimiter = re.search( r'Rekeningnummer(.+)Muntsoort', header, re.IGNORECASE )
    return delimiter.group( 1 )

  @staticmethod
  def convert_numbers( number: str ) -> str:
    return number.replace( ",", "." )

  @staticmethod
  def sanitize( text: str ) -> str:
    text = re.sub( r"[\t\r\n]+", ' ', text )
    text = re.sub( r"\s+", ' ', text )
    return text

  @staticmethod
  def get_category( text: str ) -> str:
    # @TODO insert AI
    return text
