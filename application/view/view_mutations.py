from typing import Dict
from customtkinter import CTkFrame
from application.constants import W20, W10
from application.functions import format_amount
from application.ui.elements import Elements
from application.database.database_mutations import Database_Mutations


class View_Mutations:

  @staticmethod
  def create_row( append: CTkFrame, record: Dict, row: int, pady: int, command: callable = None ):
    val1, val2, val3, val4, val5, val6 = record
    Elements.label( append, val1, 0, row, W20, pady ).configure( width = 70 )
    Elements.label( append, val2, 1, row, W20, pady ).configure( width = 115 )
    if type( val3 ) is str:
      Elements.label( append, val3, 2, row, W20, pady ).configure( width = 200 )
    else:
      Elements.segmented_buttons( append, val3, command, 2, row, W20, pady ).configure( width = 200 )
    Elements.label( append, val4, 3, row, W20, pady ).configure( width = 5 )
    Elements.label( append, val5, 4, row, W20, pady ).configure( width = 50, anchor = "e" )
    label = Elements.label( append, val6, 5, row, W20, pady )
    label.configure( wraplength = 550 )

  @staticmethod
  def create_headers( append: CTkFrame ):
    View_Mutations.create_row( append,
      [ "date", "product", "category", "", "amount", "description" ],
      0, (20, 10) )

  @staticmethod
  def create_records( append: CTkFrame ):
    row = 0
    for record in Database_Mutations.select_uncategorized_year():
      data = [
        record[ "mts_date" ],
        "src_name",
        [ "in", "et", "bd", "ab", "ks", "sp", "sa" ],
        "€",
        format_amount( record[ "mts_amount" ] ),
        record[ "mts_description" ]
      ]

      View_Mutations.create_row( append, data, row, 3, View_Mutations.set_category )
      row += 1

  @staticmethod
  def set_category( value: str ):
    pass
