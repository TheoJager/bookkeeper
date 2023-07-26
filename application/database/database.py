import sqlite3

from typing import Dict


class Database:

  @staticmethod
  def dict_factory( cursor, row ):
    d = { }
    for idx, col in enumerate( cursor.description ):
      d[ col[ 0 ] ] = row[ idx ]
    return d

  @staticmethod
  def query( sql: str, variables: Dict = None ) -> list:
    db = sqlite3.connect( 'bookkeeper.db' )
    db.row_factory = Database.dict_factory

    cursor = db.cursor()
    cursor.execute( sql, { } if variables is None else variables )

    records = cursor.fetchall()

    db.commit()
    db.close()

    return records
