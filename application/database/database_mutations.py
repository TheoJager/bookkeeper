import datetime

from typing import Dict
from application.database.database import Database


class Database_Mutations:

  @staticmethod
  def create_table_if_not_exists():
    sql = """
      CREATE TABLE IF NOT EXISTS mutations (
        mts_id integer primary key, 
        mts_date integer, 
        mts_amount real, 
        mts_start real, 
        mts_category integer, 
        mts_description text,
        UNIQUE(mts_date,mts_amount,mts_start,mts_description)
      )
    """
    Database.query( sql )

  @staticmethod
  def select() -> list:
    sql = "SELECT * FROM mutations ORDER BY mts_date DESC"
    return Database.query( sql )

  @staticmethod
  def record( id: int ) -> list:
    sql = "SELECT * FROM mutations WHERE mts_id = :mts_id"
    execute = { "mts_id": id }
    return Database.query( sql, execute )

  @staticmethod
  def insert( record: Dict ):
    sql = "INSERT INTO mutations(mts_date, mts_amount, mts_start, mts_description, mts_category) VALUES(:mts_date, :mts_amount, :mts_start, :mts_description, :mts_category)"
    Database.query( sql, record )

  @staticmethod
  def update( record: Dict ):
    sql = "UPDATE mutations SET mts_date = :mts_date, mts_amount = :mts_amount, mts_description = :mts_description, mts_category = :mts_category WHERE mts_id = :mts_id"
    Database.query( sql, record )

  @staticmethod
  def delete( id: int ):
    sql = "DELETE FROM mutations WHERE mts_id = :mts_id"
    execute = { "mts_id": id }
    Database.query( sql, execute )

  @staticmethod
  def sum() -> float:
    sql = "select sum(mts_amount) as mts_total from mutations"

    mts = Database.query( sql )

    mts_total = mts[ 0 ][ "mts_total" ]
    return 0 if mts_total is None else round( mts_total, 2 )

  @staticmethod
  def sum_category_year( category: int ) -> float:
    last_year = datetime.datetime.now() - datetime.timedelta( days = 365 )

    mts_date = last_year.strftime( "%Y%m01" )

    sql = "select sum(mts_amount) as mts_total from mutations WHERE mts_category = :mts_category AND mts_date >= :mts_date"
    execute = { "mts_category": category, "mts_date": mts_date }
    mts_total = Database.query( sql, execute )

    return round( mts_total[ 0 ][ "mts_total" ] if mts_total[ 0 ][ "mts_total" ] is not None else 0, 2 )

  @staticmethod
  def sum_category_month( category: int ) -> float:
    mts_date = datetime.datetime.now().strftime( "%Y%m01" )

    sql = "select sum(mts_amount) as mts_total from mutations WHERE mts_category = :mts_category AND mts_date >= :mts_date"
    execute = { "mts_category": category, "mts_date": mts_date }
    mts_total = Database.query( sql, execute )

    return round( mts_total[ 0 ][ "mts_total" ] if mts_total[ 0 ][ "mts_total" ] is not None else 0, 2 )
