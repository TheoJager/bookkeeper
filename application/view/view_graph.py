from typing import Dict
from customtkinter import CTkFrame
from constants import COLOR_1, COLOR_2, COLOR_BACKGROUND_2, COLOR_CONTRAST, COLOR_CURRENT, W20
from date.today import Today
from ui.elements import Elements
from view.view_date import View_Date
from view.view_month import View_Month
from view.view_table import View_Table
from database.database_mutations import Database_Mutations
from database.database_categories import Database_Categories


class View_Graph:
  ELEMENTS = { }

  @staticmethod
  def reset():
    View_Graph.ELEMENTS = { }

  @staticmethod
  def update_screen( month: int, ctr_id: int ):
    View_Date.update( month )
    View_Month.update( month )
    View_Table.update_category_month( ctr_id, month )

  @staticmethod
  def create( append: CTkFrame ):
    column = 0
    for ctr in Database_Categories.select():
      data = View_Graph.get_data_category( ctr[ "ctr_id" ] )

      View_Graph.create_graph( append, ctr, data, column )

      column += 1

  @staticmethod
  def create_graph( append: CTkFrame, ctr: Dict, data: Dict, column: int ):
    View_Graph.create_header( append, ctr[ "ctr_name" ], column, 0 )

    View_Graph.create_bars( append, column, 1, data, ctr[ "ctr_id" ] )

  @staticmethod
  def create_frame( append: CTkFrame, column: int, row: int ) -> CTkFrame:
    frame = Elements.frame( append, column, row )
    frame.configure( fg_color = "transparent" )
    return frame

  @staticmethod
  def create_header( append: CTkFrame, ctr_name: str, column: int, row: int ):
    append = View_Graph.create_frame( append, column, row )
    append.grid( padx = W20 )

    header = Elements.header( append, ctr_name, 0, 0, 0 )
    header.grid( columnspan = 12 )

  @staticmethod
  def create_bars( append: CTkFrame, column: int, row: int, data: Dict, ctr_id: int ):
    append = View_Graph.create_frame( append, column, row )
    append.grid( padx = W20 )

    maximum = round( max( data[ "p" ] ) ) + 1
    minimum = round( min( data[ "n" ] ) ) - 1
    size = max( abs( maximum ), abs( minimum ) )

    today_month = Today.month()
    months = list( range( today_month, 12 ) ) + list( range( today_month ) )

    column = 0
    for month in months:
      height_p = (data[ "p" ][ month ] / size) * 100

      label = Elements.button( append, "", lambda i = month: View_Graph.update_screen( i + 1, ctr_id ), column, 0, 1, 0 )
      label.configure( width = 6, height = height_p, bg_color = COLOR_1 )
      label.grid( sticky = "s" )

      if month == today_month - 1:
        label.configure( fg_color = COLOR_CONTRAST, bg_color = COLOR_CONTRAST )
      if height_p == 0:
        label.configure( fg_color = "transparent" )

      height_n = (abs( data[ "n" ][ month ] ) / size) * 100

      label = Elements.button( append, "", lambda i = month: View_Graph.update_screen( i + 1, ctr_id ), column, 1, 1, 0 )
      label.configure( width = 6, height = height_n, fg_color = COLOR_BACKGROUND_2 )
      label.grid( sticky = "n" )
      if height_n == 0:
        label.configure( fg_color = "transparent" )

      column += 1

  @staticmethod
  def update( month: int ):
    today_month = Today.month()
    for ctr_id in View_Graph.ELEMENTS:
      for i in View_Graph.ELEMENTS[ ctr_id ]:
        button = View_Graph.ELEMENTS[ ctr_id ][ i ]
        if i + 1 == today_month:
          button.configure( fg_color = COLOR_CONTRAST )
        elif i + 1 == month:
          button.configure( fg_color = COLOR_CURRENT )
        else:
          button.configure( fg_color = COLOR_1 )

  @staticmethod
  def get_data_category( ctr_id: int ):
    amounts = Database_Mutations.sum_category_months( ctr_id )

    data = { "p": [ 0 ] * 12, "n": [ 0 ] * 12 }

    for i in range( 12 ):
      if amounts[ i ] >= 0:
        data[ "p" ][ i ] = amounts[ i ]
      else:
        data[ "n" ][ i ] = amounts[ i ]

    return data
