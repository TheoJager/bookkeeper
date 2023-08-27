from typing import Dict
from customtkinter import CTkFrame
from constants import W20, W10
from functions import format_amount
from ui.elements import Elements
from database.database_mutations import Database_Mutations


class View_Table:
  ELEMENT: CTkFrame = None
  ELEMENT_PARENT: CTkFrame = None

  @staticmethod
  def reset():
    View_Table.ELEMENT = None
    View_Table.ELEMENT_PARENT = None

  @staticmethod
  def create( append: CTkFrame ):
    View_Table.ELEMENT_PARENT = append
    View_Table.create_headers()

  @staticmethod
  def create_frame_headers( append: CTkFrame ) -> CTkFrame:
    frame = Elements.frame( append, 0, 1 )
    frame.configure( width = 550, fg_color = "transparent" )
    return frame

  @staticmethod
  def create_frame_rows( append: CTkFrame ) -> CTkFrame:
    frame = Elements.scroll( append, 0, 2 )
    frame.configure( width = 550, fg_color = "transparent", height = 375 )
    View_Table.ELEMENT = frame
    return frame

  @staticmethod
  def create_row( append: CTkFrame, record: Dict, row: int, pady: int ):
    val1, val2, val3, val4, val5 = record
    Elements.label( append, val1, 0, row, W20, pady ).configure( width = 70 )  # date
    Elements.label( append, val2, 1, row, W10, pady ).configure( width = 250 )  # product
    Elements.label( append, val3, 2, row, W10, pady ).configure( width = 90 )  # category
    Elements.label( append, val4, 3, row, W10, pady ).configure( width = 5 )
    Elements.label( append, val5, 4, row, W10, pady ).configure( width = 40, anchor = "e" )  # amount

  @staticmethod
  def create_headers():
    View_Table.create_row(
      View_Table.create_frame_headers( View_Table.ELEMENT_PARENT ),
      [ "date", "product", "category", "", "amount" ],
      0, (20, 10) )

  @staticmethod
  def update_rows( records: Dict ):
    append = View_Table.reset_frame_rows()

    row = 0
    for record in records:
      data = [
        record[ "mts_date" ],
        record[ "src_name" ],
        record[ "ctr_name" ],
        "€",
        format_amount( record[ "mts_amount" ] )
      ]

      View_Table.create_row( append, data, row, 3 )
      row += 1

  @staticmethod
  def update( month: int ):
    View_Table.update_rows( Database_Mutations.select_month( month ) )

  @staticmethod
  def update_category_month( ctr_id: int, month: int ):
    View_Table.update_rows( Database_Mutations.select_category_month( ctr_id, month ) )

  @staticmethod
  def update_category_year( ctr_id: int ):
    View_Table.update_rows( Database_Mutations.select_category_year( ctr_id ) )

  @staticmethod
  def reset_frame_rows():
    View_Table.remove_frame( View_Table.ELEMENT )
    return View_Table.create_frame_rows( View_Table.ELEMENT_PARENT )

  @staticmethod
  def remove_frame( append: CTkFrame = None ):
    if append is not None:
      append.destroy()
