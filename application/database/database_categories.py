import sqlite3

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
        ctr_sequence integer, 
        UNIQUE(ctr_name)
      )
    """
    Database.query( sql )

  @staticmethod
  def create_default_records():
    cat_records = [
      { 'ctr_income': 0, 'ctr_sequence': 1, 'ctr_name': 'Incidenteel' },
      { 'ctr_income': 0, 'ctr_sequence': 2, 'ctr_name': 'Eten' },
      { 'ctr_income': 0, 'ctr_sequence': 3, 'ctr_name': 'Boodschappen' },
      { 'ctr_income': 0, 'ctr_sequence': 4, 'ctr_name': 'Abonnementen' },
      { 'ctr_income': 0, 'ctr_sequence': 5, 'ctr_name': 'Kosten' },
      { 'ctr_income': 0, 'ctr_sequence': 6, 'ctr_name': 'Sparen' },
      { 'ctr_income': 0, 'ctr_sequence': 7, 'ctr_name': 'Beleggingen' },
      { 'ctr_income': 1, 'ctr_sequence': 8, 'ctr_name': 'Salaris' },
    ]
    for cat_record in cat_records:
      try:
        Database_Categories.insert( cat_record )
      except sqlite3.IntegrityError:
        break

  @staticmethod
  def select() -> list:
    sql = 'SELECT * FROM categories ORDER BY ctr_id ASC'
    return Database.query( sql )

  @staticmethod
  def record( id: int ) -> list:
    sql = 'SELECT * FROM categories WHERE ctr_id = :ctr_id'
    execute = { 'ctr_id': id }
    return Database.query( sql, execute )

  @staticmethod
  def insert( record: Dict ):
    sql = 'INSERT INTO categories(ctr_name, ctr_income, ctr_sequence) VALUES(:ctr_name, :ctr_income, :ctr_sequence)'
    execute = {
      'ctr_name'    : record[ 'ctr_name' ],
      'ctr_income'  : record[ 'ctr_income' ],
      'ctr_sequence': record[ 'ctr_sequence' ],
    }
    Database.query( sql, execute )

  @staticmethod
  def update( record: Dict ):
    sql = 'UPDATE categories SET ctr_name = :ctr_name, ctr_income = :ctr_income, ctr_sequence = :ctr_sequence WHERE ctr_id = :ctr_id'
    execute = {
      'ctr_id'      : record[ 'ctr_id' ],
      'ctr_name'    : record[ 'ctr_name' ],
      'ctr_income'  : record[ 'ctr_income' ],
      'ctr_sequence': record[ 'ctr_sequence' ],
    }
    Database.query( sql, execute )

  @staticmethod
  def delete( id: int ):
    sql = 'DELETE FROM categories WHERE ctr_id = :ctr_id'
    execute = { 'ctr_id': id }
    Database.query( sql, execute )
