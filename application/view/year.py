from customtkinter import CTkFrame
from application.ui.elements import Elements
from application.view.table import View_Table
from application.constants import W20, CATEGORY_INCOME
from application.functions import format_amount, format_percentage
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories


class View_Year:
  ELEMENTS = { }

  @staticmethod
  def create( append: CTkFrame ):
    row = 0
    for category in Database_Categories.select():
      ctr_id = category[ "ctr_id" ]

      Elements.label( append, category[ "ctr_name" ], 1, row, W20, W20 ).configure( anchor = "w", width = 125 )
      Elements.label( append, "€", 2, row, W20, W20 )
      s = Elements.label( append, "0.00", 3, row, (10, 0), W20 )
      p = Elements.label( append, "0.00", 4, row, (10, 0), W20 )
      Elements.label( append, "%", 5, row, (10, 10), W20 )
      Elements.button( append, "@", lambda ctr_id = ctr_id: View_Table.update_category_year( ctr_id ), 6, row, (20, 20) ).configure( width = 25 )

      s.configure( anchor = "e", width = 60 )
      p.configure( anchor = "e", width = 60 )

      View_Year.ELEMENTS[ category[ "ctr_name" ] ] = [ s, p ]
      row += 1

  @staticmethod
  def update():
    income = Database_Mutations.sum_category_year( CATEGORY_INCOME )

    for category in Database_Categories.select():
      current = Database_Mutations.sum_category_year( category[ "ctr_id" ] )
      percent = View_Year.calculate_percentage( current, income )

      s, p = View_Year.ELEMENTS[ category[ "ctr_name" ] ]
      s.configure( text = format_amount( current ) )
      p.configure( text = format_percentage( percent ) )

  @staticmethod
  def calculate_percentage( amount: float, income: float ) -> float:
    return 0 if income == 0 else round( (amount / income) * 100, 1 )
