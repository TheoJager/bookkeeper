from customtkinter import CTkFrame
from application.constants import W20
from application.functions import format_amount
from application.ui.elements import Elements
from application.view.navigation import Navigation
from application.database.database_mutations import Database_Mutations


class View_Table:
  ELEMENT: CTkFrame = None
  ELEMENT_PARENT: CTkFrame = None

  @staticmethod
  def create_headers( append: CTkFrame ):
    View_Table.ELEMENT_PARENT = append
    Elements.header( append, "date", 0, 0, W20, W20 )
    Elements.header( append, "product", 1, 0, W20, W20 )
    Elements.header( append, "category", 2, 0, W20, W20 )
    Elements.header( append, "amount", 3, 0, (20, 20), W20 )

  @staticmethod
  def create_table( append: CTkFrame ):
    # View_Table.ELEMENT_TABLE = Elements.scroll( append, 0, 1, 5, 4, 0, 0 )
    View_Table.ELEMENT = Elements.frame( append, 0, 1, 5, 4, 0, 0 )
    View_Table.ELEMENT.configure( fg_color = "transparent" )

  @staticmethod
  def remove_table():
    if View_Table.ELEMENT is not None:
      View_Table.ELEMENT.destroy()

  @staticmethod
  def update_rows_month( ctr_id: int ):
    View_Table.remove_table()
    View_Table.create_table( View_Table.ELEMENT_PARENT )

    row = 0
    for record in Database_Mutations.select_category_month( ctr_id, Navigation.MONTH ):
      Elements.label( View_Table.ELEMENT, record[ "mts_date" ], 0, row, W20, W20 )
      Elements.label( View_Table.ELEMENT, "src_name", 1, row, W20, W20 )
      Elements.label( View_Table.ELEMENT, record[ "ctr_name" ], 2, row, W20, W20 )
      Elements.label( View_Table.ELEMENT, format_amount( record[ "mts_amount" ], ), 3, row, W20, W20 )
      row += 1

  @staticmethod
  def update_rows_year( ctr_id: int ):
    View_Table.remove_table()
    View_Table.create_table( View_Table.ELEMENT_PARENT )

    row = 0
    for record in Database_Mutations.select_category_year( ctr_id ):
      Elements.label( View_Table.ELEMENT, record[ "mts_date" ], 0, row, W20, W20 )
      Elements.label( View_Table.ELEMENT, "src_name", 1, row, W20, W20 )
      Elements.label( View_Table.ELEMENT, record[ "ctr_name" ], 2, row, W20, W20 )
      Elements.label( View_Table.ELEMENT, format_amount( record[ "mts_amount" ], ), 3, row, W20, W20 )
      row += 1
