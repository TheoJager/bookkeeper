from typing import Dict
from database.database import Database


class Database_Search:

  @staticmethod
  def create_table_if_not_exists():
    sql = """
      CREATE TABLE IF NOT EXISTS search (
        src_id integer primary key, 
        src_name text, 
        src_match text, 
        src_text text,
        ctr_id integer, 
        UNIQUE(src_match)
      )
    """
    Database.query( sql )

  @staticmethod
  def select() -> list:
    sql = 'SELECT * FROM search ORDER BY src_name'
    return Database.query( sql )

  @staticmethod
  def record( id: int ) -> list:
    sql = 'SELECT * FROM search WHERE src_id = :src_id'
    record = { 'src_id': id }
    return Database.query( sql, record )

  @staticmethod
  def insert( record: Dict ) -> int:
    sql = """
      INSERT INTO search(
        src_name, 
        src_match, 
        src_text,
        ctr_id
      ) VALUES (
        :src_name, 
        :src_match, 
        :src_text,
        :ctr_id
      )
    """
    Database.query( sql, record )
    return Database.last_inserted_id

  @staticmethod
  def update( record: Dict ):
    sql = """
      UPDATE 
        search 
      SET 
        src_name  = :src_name, 
        src_match = :src_match, 
        src_text  = :src_text, 
        ctr_id    = :ctr_id 
      WHERE 
        src_id = :src_id
    """
    Database.query( sql, record )

  @staticmethod
  def delete( id: int ):
    sql = 'DELETE FROM search WHERE src_id = :src_id'
    record = { 'src_id': id }
    Database.query( sql, record )

  @staticmethod
  def count_unsearched() -> int:
    sql = """
      SELECT 
        count( * ) as count
      FROM 
        mutations
      WHERE ctr_id >= 0
        AND mts_id NOT IN (
        SELECT 
          mts_id
        FROM 
          mutations LEFT JOIN search
        WHERE 
          mts_text LIKE '%' || src_match || '%'
        )
    """
    rec = Database.query( sql )
    return int( rec[ 0 ][ 'count' ] )

  @staticmethod
  def select_unsearched():
    sql = """
      SELECT 
        mts_id, 
        mts_date, 
        mts_amount, 
        mts_text
      FROM 
        mutations
      WHERE ctr_id >= 0
        AND mts_id NOT IN (
        SELECT 
          mts_id
        FROM 
          mutations LEFT JOIN search
        WHERE 
          mts_text LIKE '%' || src_match || '%'
        )
      ORDER BY
        mts_text
      LIMIT 20
    """
    return Database.query( sql )
