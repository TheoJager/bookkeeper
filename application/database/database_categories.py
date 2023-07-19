from typing import Dict
from application.database.database import Database


class Database_Categories:

  @staticmethod
  def create_table_if_not_exists():
    sql = """
      CREATE TABLE IF NOT EXISTS categories (
        ctr_id integer primary key, 
        ctr_name text, 
        ctr_income integer, 
        UNIQUE(ctr_name)
      )
    """
    Database.query( sql )

  @staticmethod
  def select() -> list:
    sql = 'SELECT ctr_id, ctr_name, ctr_income FROM categories ORDER BY ctr_id ASC'
    return Database.query( sql )

  @staticmethod
  def record( id: int ) -> list:
    sql = 'SELECT ctr_id, ctr_name, ctr_income FROM categories WHERE ctr_id = :ctr_id'
    execute = { 'ctr_id': id }
    return Database.query( sql, execute )

  @staticmethod
  def insert( record: Dict ):
    sql = 'INSERT INTO categories(ctr_name, ctr_income) VALUES(:ctr_name, :ctr_income)'
    execute = {
      'ctr_name'  : record[ 'ctr_name' ],
      'ctr_income': record[ 'ctr_income' ],
    }
    Database.query( sql, execute )

  @staticmethod
  def update( record: Dict ):
    sql = 'UPDATE categories SET ctr_name = :ctr_name, ctr_income = :ctr_income WHERE ctr_id = :ctr_id'
    execute = {
      'ctr_id'    : record[ 'ctr_id' ],
      'ctr_name'  : record[ 'ctr_name' ],
      'ctr_income': record[ 'ctr_income' ],
    }
    Database.query( sql, execute )

  @staticmethod
  def delete( id: int ):
    sql = 'DELETE FROM categories WHERE ctr_id = :ctr_id'
    execute = { 'ctr_id': id }
    Database.query( sql, execute )
