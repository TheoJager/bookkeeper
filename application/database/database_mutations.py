import datetime

from typing import Dict
from date.date import date
from application.database.database import Database


class Database_Mutations:

  @staticmethod
  def create_table_if_not_exists():
    sql = """
      CREATE TABLE IF NOT EXISTS mutations (
        mts_id integer primary key, 
        ctr_id integer, 
        mts_date integer, 
        mts_amount real, 
        mts_start real, 
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
    record = { "mts_id": id }
    return Database.query( sql, record )

  @staticmethod
  def insert( record: Dict ):
    sql = """
      INSERT INTO mutations(
        mts_date, 
        mts_amount, 
        mts_start, 
        mts_description, 
        ctr_id
      ) VALUES (
        :mts_date, 
        :mts_amount, 
        :mts_start, 
        :mts_description, 
        :ctr_id
      )
    """

    Database.query( sql, record )

  @staticmethod
  def update( record: Dict ):
    sql = """
      UPDATE 
        mutations 
      SET 
        mts_date        = :mts_date, 
        mts_amount      = :mts_amount, 
        mts_description = :mts_description, 
        ctr_id          = :ctr_id
      WHERE 
        mts_id = :mts_id
    """

    Database.query( sql, record )

  @staticmethod
  def delete( id: int ):
    sql = "DELETE FROM mutations WHERE mts_id = :mts_id"
    record = { "mts_id": id }
    Database.query( sql, record )

  @staticmethod
  def insert_base_value( record: list ):
    if len( Database_Mutations.select() ) == 0:
      Database_Mutations.insert( {
        'mts_date'       : "19700101",
        'mts_amount'     : record[ 'mts_start' ],
        'mts_start'      : 0,
        'mts_description': 'start',
        'ctr_id'   : 8,
      } )

  @staticmethod
  def sum() -> float:
    sql = "select sum(mts_amount) as mts_total from mutations"

    mts = Database.query( sql )

    mts_total = mts[ 0 ][ "mts_total" ]
    return 0 if mts_total is None else round( mts_total, 2 )

  @staticmethod
  def sum_category_year( category: int ) -> float:
    x = datetime.datetime.now()
    month = int( x.strftime( "%m" ) )

    x = datetime.datetime.now()
    year = int( x.strftime( "%Y" ) )

    mts_date_start= date(year - 1, month + 1, 1)
    mts_date_end= date(year, month + 1, 1)

    sql = """
      SELECT 
        sum(mts_amount) as mts_total
      FROM 
        mutations 
      WHERE ctr_id    = :ctr_id 
        AND mts_date >= :mts_date_start 
        AND mts_date <  :mts_date_end
      ORDER BY 
        mts_date DESC
    """

    record = { "ctr_id": category, "mts_date_start": mts_date_start, "mts_date_end": mts_date_end }
    mts_total = Database.query( sql, record )

    return round( mts_total[ 0 ][ "mts_total" ] if mts_total[ 0 ][ "mts_total" ] is not None else 0, 2 )


  @staticmethod
  def sum_category_month( category: int ) -> float:
    x = datetime.datetime.now()
    month = int( x.strftime( "%m" ) )

    x = datetime.datetime.now()
    year = int( x.strftime( "%Y" ) )

    mts_date_start= date(year, month, 1)
    mts_date_end= date(year, month + 1, 1)

    sql = """
      SELECT 
        sum(mts_amount) as mts_total
      FROM 
        mutations 
      WHERE ctr_id    = :ctr_id 
        AND mts_date >= :mts_date_start 
        AND mts_date <  :mts_date_end
      ORDER BY 
        mts_date DESC
    """

    record = { "ctr_id": category, "mts_date_start": mts_date_start, "mts_date_end": mts_date_end }
    mts_total = Database.query( sql, record )

    return round( mts_total[ 0 ][ "mts_total" ] if mts_total[ 0 ][ "mts_total" ] is not None else 0, 2 )

  @staticmethod
  def select_category_month( category: int, month: int ) -> list:
    x = datetime.datetime.now()
    year = int( x.strftime( "%Y" ) )

    mts_date_start= date(year, month, 1)
    mts_date_end= date(year, month + 1, 1)

    sql = """
      SELECT 
        ctr_name, 
        mutations.*
      FROM 
        mutations 
        LEFT JOIN categories USING(ctr_id)
      WHERE ctr_id    = :ctr_id 
        AND mts_date >= :mts_date_start 
        AND mts_date <  :mts_date_end
      ORDER BY 
        mts_date DESC
    """

    record = { "ctr_id": category, "mts_date_start": mts_date_start, "mts_date_end": mts_date_end }
    return Database.query( sql, record )

  @staticmethod
  def select_category_year( category: int ) -> list:
    x = datetime.datetime.now()
    month = int( x.strftime( "%m" ) )

    x = datetime.datetime.now()
    year = int( x.strftime( "%Y" ) )

    mts_date_start= date(year - 1, month + 1, 1)
    mts_date_end= date(year, month + 1, 1)

    sql = """
      SELECT 
        ctr_name, 
        mutations.*
      FROM 
        mutations 
        LEFT JOIN categories USING(ctr_id)
      WHERE ctr_id    = :ctr_id 
        AND mts_date >= :mts_date_start 
        AND mts_date <  :mts_date_end
      ORDER BY 
        mts_date DESC
    """

    record = { "ctr_id": category, "mts_date_start": mts_date_start, "mts_date_end": mts_date_end }
    return Database.query( sql, record )
