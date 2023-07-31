from typing import Dict
from application.date.date import date
from application.date.today import Today
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
        'ctr_id'         : 0,
      } )

  @staticmethod
  def select_month( month: int ) -> list:
    year = Today.year() - (1 if month > Today.month() else 0)

    record = {
      "mts_date_start": date( year, month ),
      "mts_date_end"  : date( year, month + 1 )
    }
    return Database.query( Database_Mutations.SELECT_DATE, record )

  @staticmethod
  def sum() -> float:
    sql = "select sum(mts_amount) as mts_total from mutations"

    mts = Database.query( sql )

    mts_total = mts[ 0 ][ "mts_total" ]
    return 0 if mts_total is None else round( mts_total, 2 )

  @staticmethod
  def select_uncategorized_year() -> list:
    year = Today.year()
    month = Today.month()

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
        mts_description
    """

    record = {
      "ctr_id"        : 0,
      "mts_date_start": date( year - 1, month + 1 ),
      "mts_date_end"  : date( year - 0, month + 1 )
    }
    return Database.query( sql, record )

  @staticmethod
  def select_category_year( ctr_id: int ) -> list:
    year = Today.year()
    month = Today.month()

    record = {
      "ctr_id"        : ctr_id,
      "mts_date_start": date( year - 1, month + 1 ),
      "mts_date_end"  : date( year - 0, month + 1 )
    }
    return Database.query( Database_Mutations.SELECT_CATEGORY_DATE, record )

  @staticmethod
  def sum_category_year( ctr_id: int ) -> float:
    year = Today.year()
    month = Today.month()

    record = {
      "ctr_id"        : ctr_id,
      "mts_date_start": date( year - 1, month + 1 ),
      "mts_date_end"  : date( year - 0, month + 1 )
    }
    mts = Database.query( Database_Mutations.SUM_CATEGORY_DATE, record )

    mts_total = mts[ 0 ][ "mts_total" ]
    return 0 if mts_total is None else round( mts_total, 2 )

  @staticmethod
  def select_category_month( ctr_id: int, month: int ) -> list:
    year = Today.year() - (1 if month > Today.month() else 0)

    record = {
      "ctr_id"        : ctr_id,
      "mts_date_start": date( year, month ),
      "mts_date_end"  : date( year, month + 1 )
    }
    return Database.query( Database_Mutations.SELECT_CATEGORY_DATE, record )

  @staticmethod
  def sum_category_month( ctr_id: int, month: int ) -> float:
    year = Today.year() - (1 if month > Today.month() else 0)

    record = {
      "ctr_id"        : ctr_id,
      "mts_date_start": date( year, month ),
      "mts_date_end"  : date( year, month + 1 )
    }
    mts = Database.query( Database_Mutations.SUM_CATEGORY_DATE, record )

    mts_total = mts[ 0 ][ "mts_total" ]
    return 0 if mts_total is None else round( mts_total, 2 )

  @staticmethod
  def sum_category_months( ctr_id: int ) -> list:
    response = [ ]
    for i in range( 12 ):
      response.append( Database_Mutations.sum_category_month( ctr_id, i + 1 ) )
    return response

  SUM_CATEGORY_DATE = """
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

  SELECT_DATE = """
    SELECT 
      ctr_name, 
      mutations.*
    FROM 
      mutations 
      LEFT JOIN categories USING(ctr_id)
    WHERE mts_date >= :mts_date_start 
      AND mts_date <  :mts_date_end
    ORDER BY 
      mts_date DESC
  """

  SELECT_CATEGORY_DATE = """
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
