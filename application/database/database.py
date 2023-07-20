import sqlite3

from typing import Dict


class Database:

  @staticmethod
  def query( sql: str, variables: Dict = None ) -> list:
    db = sqlite3.connect( 'bookkeeper.db' )

    cursor = db.cursor()
    cursor.execute( sql, { } if variables is None else variables )

    records = cursor.fetchall()

    db.commit()
    db.close()

    return records
