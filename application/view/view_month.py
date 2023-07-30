import application.globals as glb

from customtkinter import CTkFrame
from application.ui.elements import Elements
from application.constants import W20, W10, CATEGORY_INCOME
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories
from application.functions import format_amount, format_percentage
from application.view.view_table import View_Table


class View_Month:
  ELEMENTS = { }

  @staticmethod
  def create( append: CTkFrame ):
    row = 0
    for category in Database_Categories.select():
      ctr_id = category[ "ctr_id" ]

      Elements.label( append, "€", 1, row, W20, W20 )
      s = Elements.label( append, "0.00", 2, row, W10, W20 )
      p = Elements.label( append, "0.00", 3, row, W10, W20 )
      Elements.label( append, "%", 4, row, (10, 10), W20 )
      Elements.button( append, "@", lambda ctr_id = ctr_id: View_Table.update_category_month( ctr_id, glb.SELECTED_MONTH ), 5, row, (20, 20) ).configure( width = 25 )

      s.configure( anchor = "e", width = 60 )
      p.configure( anchor = "e", width = 60 )

      View_Month.ELEMENTS[ category[ "ctr_name" ] ] = [ s, p ]
      row += 1

  @staticmethod
  def update( month: int ):
    income = Database_Mutations.sum_category_month( CATEGORY_INCOME, month )

    for category in Database_Categories.select():
      current = Database_Mutations.sum_category_month( category[ "ctr_id" ], month )
      percent = View_Month.calculate_percentage( current, income )

      s, p = View_Month.ELEMENTS[ category[ "ctr_name" ] ]
      s.configure( text = format_amount( current ) )
      p.configure( text = format_percentage( percent ) )

  @staticmethod
  def calculate_percentage( amount: float, income: float ) -> float:
    return 0 if income == 0 else round( (amount / income) * 100, 1 )