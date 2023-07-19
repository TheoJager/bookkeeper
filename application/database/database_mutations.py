from typing import Dict
from application.database.database import Database


class Database_Mutations:

  @staticmethod
  def create_table_if_not_exists():
    sql = """
      CREATE TABLE IF NOT EXISTS mutations (
        mts_id integer primary key, 
        mts_date text, 
        mts_amount real, 
        mts_category integer, 
        mts_description text,
        UNIQUE(mts_date,mts_amount,mts_description)
      )
    """
    Database.query( sql )

  @staticmethod
  def select() -> list:
    sql = 'SELECT mts_id, mts_date, mts_amount, mts_category, mts_description FROM mutations ORDER BY mts_date DESC'
    return Database.query( sql )

  @staticmethod
  def record( id: int ) -> list:
    sql = 'SELECT mts_id, mts_date, mts_amount, mts_description, mts_category FROM mutations WHERE mts_id = :mts_id'
    execute = { 'mts_id': id }
    return Database.query( sql, execute )

  @staticmethod
  def insert( record: Dict ):
    sql = 'INSERT INTO mutations(mts_date, mts_amount, mts_description) VALUES(:mts_date, :mts_amount, :mts_description)'
    execute = {
      'mts_date'       : record[ 'mts_date' ],
      'mts_amount'     : record[ 'mts_amount' ],
      'mts_description': record[ 'mts_description' ],
      'mts_category'   : record[ 'mts_category' ],
    }
    Database.query( sql, execute )

  @staticmethod
  def update( record: Dict ):
    sql = 'UPDATE mutations SET mts_date = :mts_date, mts_amount = :mts_amount, mts_description = :mts_description, mts_category = :mts_category WHERE mts_id = :mts_id'
    execute = {
      'mts_id'         : record[ 'mts_id' ],
      'mts_date'       : record[ 'mts_date' ],
      'mts_amount'     : record[ 'mts_amount' ],
      'mts_description': record[ 'mts_description' ],
      'mts_category'   : record[ 'mts_category' ],
    }
    Database.query( sql, execute )

  @staticmethod
  def delete( id: int ):
    sql = 'DELETE FROM mutations WHERE mts_id = :mts_id'
    execute = { 'mts_id': id }
    Database.query( sql, execute )
