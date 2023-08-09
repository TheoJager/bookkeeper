import globals as glb

from customtkinter import CTkFrame

from date.date import date
from date.today import Today
from ui.elements import Elements
from constants import W20, W10, CATEGORY_INCOME, COLOR_CONTRAST, CATEGORY_CORRECTIE
from database.database_mutations import Database_Mutations
from database.database_categories import Database_Categories
from functions import format_amount, format_percentage
from view.view_table import View_Table


class View_Month:
  ELEMENTS = { }

  @staticmethod
  def reset():
    View_Month.ELEMENTS = { }

  @staticmethod
  def create( append: CTkFrame ):
    View_Month.create_categories( append )
    View_Month.create_total( append )

  @staticmethod
  def create_categories( append: CTkFrame ):
    row = 0
    for category in Database_Categories.select():
      ctr_id = category[ "ctr_id" ]
      ctr_name = category[ "ctr_name" ]

      Elements.label( append, "€", 1, row, W20, W20 )
      s = Elements.label( append, "0.00", 2, row, W10, W20 )
      p = Elements.label( append, "0.00", 3, row, W10, W20 )
      Elements.label( append, "%", 4, row, (10, 10), W20 )
      Elements.button( append, "@", lambda ctr_id = ctr_id: View_Table.update_category_month( ctr_id, glb.SELECTED_MONTH ), 5, row, (20, 20) ).configure( width = 25 )

      s.configure( anchor = "e", width = 60 )
      p.configure( anchor = "e", width = 60 )

      View_Month.ELEMENTS[ ctr_name ] = [ s, p ]
      row += 1

  @staticmethod
  def create_total( append: CTkFrame ):
    row = 8

    ctr_name = "totaal"

    Elements.label( append, "€", 1, row, W20, W20 )
    s = Elements.label( append, "0.00", 2, row, W10, W20 )
    Elements.button( append, "transfer", lambda: View_Month.transfer( glb.SELECTED_MONTH ), 3, row, (20, 20) ).configure( width = 25, fg_color = COLOR_CONTRAST )
    Elements.label( append, "", 4, row, (10, 10), W20 )
    Elements.button( append, "@", lambda: View_Table.update( glb.SELECTED_MONTH ), 5, row, (20, 20) ).configure( width = 25 )

    s.configure( anchor = "e", width = 60 )

    View_Month.ELEMENTS[ ctr_name ] = s

  @staticmethod
  def transfer( month: int ):
    year = Today.year() - (1 if month > Today.month() else 0)
    sum_month = Database_Mutations.sum_month( month )

    if sum_month != 0:
      date_end = date( year, month + 1, -1 )
      date_srt = date( year, month + 1, 1 )

      Database_Mutations.insert( {
        'mts_date'  : date_end,
        'mts_amount': sum_month * -1,
        'mts_start' : 0,
        'mts_text'  : 'NL51ABNA0518940136: afboeking maand',
        'ctr_id'    : CATEGORY_CORRECTIE,
      } )

      Database_Mutations.insert( {
        'mts_date'  : date_srt,
        'mts_amount': sum_month,
        'mts_start' : 0,
        'mts_text'  : 'NL51ABNA0518940136: bijboeking maand',
        'ctr_id'    : CATEGORY_CORRECTIE,
      } )

      View_Month.update( month )
      View_Table.update( month )

  @staticmethod
  def update( month: int ):
    View_Month.update_categories( month )
    View_Month.update_total( month )

  @staticmethod
  def update_categories( month: int ):
    income = Database_Mutations.sum_category_month( CATEGORY_INCOME, month )

    for category in Database_Categories.select():
      current = Database_Mutations.sum_category_month( category[ "ctr_id" ], month )
      percent = View_Month.calculate_percentage( current, income )

      s, p = View_Month.ELEMENTS[ category[ "ctr_name" ] ]
      s.configure( text = format_amount( current ) )
      p.configure( text = format_percentage( percent ) )

  @staticmethod
  def update_total( month: int ):
    current = Database_Mutations.sum_month( month )
    current = 0 if current == -0 else current

    s = View_Month.ELEMENTS[ "totaal" ]
    s.configure( text = format_amount( current ) )

  @staticmethod
  def calculate_percentage( amount: float, income: float ) -> float:
    return 0 if income == 0 else round( (amount / income) * 100, 1 )
