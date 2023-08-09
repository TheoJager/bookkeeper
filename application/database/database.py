import sqlite3

from typing import Dict


class Database:
  last_inserted_id: int = 0

  @staticmethod
  def dict_factory( cursor, row ) -> Dict:
    d = { }
    for idx, col in enumerate( cursor.description ):
      d[ col[ 0 ] ] = row[ idx ]
    return d

  @staticmethod
  def query( sql: str, variables: Dict = None ) -> list:
    db = sqlite3.connect( 'pennytracker.sqlite' )
    db.row_factory = Database.dict_factory

    cursor = db.cursor()
    cursor.execute( sql, { } if variables is None else variables )

    records = cursor.fetchall()
    Database.last_inserted_id = cursor.lastrowid

    db.commit()
    db.close()

    return records
