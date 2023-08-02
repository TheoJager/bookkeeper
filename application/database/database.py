import sqlite3

from typing import Dict
from pathlib import Path


class Database:

  @staticmethod
  def root( dir ) -> Path:
    return [ p for p in dir.parents if p.parts[ -1 ] == 'application' ][ 0 ]

  @staticmethod
  def dict_factory( cursor, row ) -> Dict:
    d = { }
    for idx, col in enumerate( cursor.description ):
      d[ col[ 0 ] ] = row[ idx ]
    return d

  @staticmethod
  def query( sql: str, variables: Dict = None ) -> list:
    path = str( Database.root( Path( __file__ ) ).absolute() ).replace( '\\', '/' )
    db = sqlite3.connect( path + '/PennyTracker.sqlite' )
    db.row_factory = Database.dict_factory

    cursor = db.cursor()
    cursor.execute( sql, { } if variables is None else variables )

    records = cursor.fetchall()

    db.commit()
    db.close()

    return records
