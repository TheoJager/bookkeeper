from typing import Dict
from application.constants import CATEGORY_INCOME
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
        mts_text text,
        UNIQUE(mts_date,mts_amount,mts_start,mts_text)
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
        mts_text, 
        ctr_id
      ) VALUES (
        :mts_date, 
        :mts_amount, 
        :mts_start, 
        :mts_text, 
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
        mts_date   = :mts_date, 
        mts_amount = :mts_amount, 
        mts_text   = :mts_text, 
        ctr_id     = :ctr_id
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
        'mts_date'  : "19700101",
        'mts_amount': record[ 'mts_start' ],
        'mts_start' : 0,
        'mts_text'  : 'start',
        'ctr_id'    : -1,
      } )

  @staticmethod
  def sum() -> float:
    sql = "SELECT sum(mts_amount) AS mts_total FROM mutations"

    mts = Database.query( sql )

    mts_total = mts[ 0 ][ "mts_total" ]
    return 0 if mts_total is None else round( mts_total, 2 )

  @staticmethod
  def select_month( month: int ) -> list:
    year = Today.year() - (1 if month > Today.month() else 0)

    record = {
      "mts_date_start": date( year, month ),
      "mts_date_end"  : date( year, month + 1 )
    }
    return Database.query( Database_Mutations.SELECT_DATE, record )

  @staticmethod
  def sum_month( month: int ) -> list:
    year = Today.year() - (1 if month > Today.month() else 0)

    record = {
      "mts_date_start": date( year, month ),
      "mts_date_end"  : date( year, month + 1 )
    }
    mts = Database.query( Database_Mutations.SUM_DATE, record )

    mts_total = mts[ 0 ][ "mts_total" ]
    return 0 if mts_total is None else round( mts_total, 2 )

  @staticmethod
  def sum_months() -> list:
    response = [ ]
    for i in range( 12 ):
      response.append( Database_Mutations.sum_month( i + 1 ) )
    return response

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
    multiplier = 1 if ctr_id == CATEGORY_INCOME else -1
    response = [ ]
    for i in range( 12 ):
      response.append( Database_Mutations.sum_category_month( ctr_id, i + 1 ) * multiplier )
    return response

  SUM_DATE = """
    SELECT 
      sum(mts_amount) as mts_total
    FROM 
      mutations 
      LEFT JOIN ( 
        search
        LEFT JOIN categories USING(ctr_id) )
    WHERE mts_text LIKE '%' || src_match || '%'
      AND mts_date >= :mts_date_start 
      AND mts_date <  :mts_date_end
  """

  SELECT_DATE = """
    SELECT 
      src_name, 
      ctr_name, 
      mutations.*
    FROM 
      mutations 
      LEFT JOIN ( 
        search
        LEFT JOIN categories USING(ctr_id) )
    WHERE mts_text LIKE '%' || src_match || '%'
      AND mts_date >= :mts_date_start 
      AND mts_date <  :mts_date_end
    ORDER BY
      ctr_name, src_name
  """

  SUM_CATEGORY_DATE = """
    SELECT 
      sum(mts_amount) as mts_total
    FROM 
      mutations 
      LEFT JOIN ( 
        search
        LEFT JOIN categories USING(ctr_id) )
    WHERE mts_text LIKE '%' || src_match || '%'
      AND search.ctr_id = :ctr_id 
      AND mts_date >= :mts_date_start 
      AND mts_date <  :mts_date_end
  """

  SELECT_CATEGORY_DATE = """
    SELECT 
      src_name, 
      ctr_name, 
      mutations.*
    FROM 
      mutations 
      LEFT JOIN ( 
        search
        LEFT JOIN categories USING(ctr_id) )
    WHERE mts_text LIKE '%' || src_match || '%'
      AND search.ctr_id = :ctr_id 
      AND mts_date >= :mts_date_start 
      AND mts_date <  :mts_date_end
    ORDER BY
      ctr_name, src_name
  """
