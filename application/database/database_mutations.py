from typing import Dict
from application.database.database import Database


class Database_Mutations:

    @staticmethod
    def create_table_if_not_exists():
        sql = 'CREATE TABLE IF NOT EXISTS mutations (mts_id integer primary key, mts_date text, mts_amount real, mts_category integer, mts_description text)'
        Database.query(sql)

    @staticmethod
    def records() -> list:
        sql = 'SELECT mts_id, mts_date, mts_amount, mts_category, mts_description FROM mutations'
        return Database.query(sql)

    @staticmethod
    def record_by_id(id: int) -> list:
        sql = 'SELECT mts_id, mts_date, mts_amount, mts_description, mts_category FROM mutations WHERE mts_id = :mts_id'
        execute = {'mts_id': id}
        return Database.query(sql, execute)

    @staticmethod
    def insert_record(fields: Dict):
        sql = 'INSERT INTO mutations(mts_date, mts_amount, mts_description) VALUES(:mts_date, :mts_amount, :mts_description)'
        execute = {
            'mts_date': fields['mts_date'],
            'mts_amount': fields['mts_amount'],
            'mts_description': fields['mts_description']
        }
        Database.query(sql, execute)

    @staticmethod
    def update_record(fields: Dict):
        sql = 'UPDATE mutations SET mts_date = :mts_date, mts_amount = :mts_amount, mts_description = :mts_description, mts_category = :mts_category WHERE mts_id = :mts_id'
        execute = {
            'mts_id': fields['mts_id'],
            'mts_date': fields['mts_date'],
            'mts_amount': fields['mts_amount'],
            'mts_description': fields['mts_description'],
            'mts_category': fields['mts_category']
        }
        Database.query(sql, execute)

    @staticmethod
    def delete_record(id: int):
        sql = 'DELETE FROM addresses WHERE mts_id = :mts_id'
        execute = {'mts_id': id}
        Database.query(sql, execute)
