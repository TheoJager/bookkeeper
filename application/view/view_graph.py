from customtkinter import CTkFrame
from constants import COLOR_1, COLOR_BACKGROUND_2, COLOR_CONTRAST, COLOR_CURRENT, W20
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
  def create( append: CTkFrame ):
    column = 0
    for ctr in Database_Categories.select():
      View_Graph.create_header( append, ctr[ "ctr_name" ], column, 0 )

      View_Graph.create_bars( append, column, 1, ctr[ "ctr_id" ] )

      column += 1

  @staticmethod
  def create_header( append: CTkFrame, ctr_name: str, column: int, row: int ):
    append = View_Graph.create_frame( append, column, row )
    append.grid( padx = W20 )

    header = Elements.header( append, ctr_name, 0, 0, 0 )
    header.grid( columnspan = 12 )

  @staticmethod
  def create_frame( append: CTkFrame, column: int, row: int ) -> CTkFrame:
    frame = Elements.frame( append, column, row )
    frame.configure( fg_color = "transparent" )
    return frame

  @staticmethod
  def create_bars( append: CTkFrame, column: int, row: int, ctr_id: int ):
    View_Graph.ELEMENTS[ ctr_id ] = { "p": [ 0 ] * 12, "n": [ 0 ] * 12 }

    append = View_Graph.create_frame( append, column, row )
    append.grid( padx = W20 )

    today_month = Today.month()
    months = list( range( today_month, 12 ) ) + list( range( today_month ) )

    column = 0
    for month in months:
      button_p = Elements.button( append, "", lambda i = month: View_Graph.update_screen( i + 1, ctr_id ), column, 0, 1, 0 )
      button_p.configure( width = 6, bg_color = COLOR_1 )
      button_p.grid( sticky = "s" )

      button_n = Elements.button( append, "", lambda i = month: View_Graph.update_screen( i + 1, ctr_id ), column, 1, 1, 0 )
      button_n.configure( width = 6, fg_color = COLOR_BACKGROUND_2 )
      button_n.grid( sticky = "n" )

      View_Graph.ELEMENTS[ ctr_id ][ 'p' ][ month ] = button_p
      View_Graph.ELEMENTS[ ctr_id ][ 'n' ][ month ] = button_n

      column += 1

  @staticmethod
  def update_screen( month: int, ctr_id: int ):
    View_Date.update( month )
    View_Month.update( month )
    View_Table.update_category_month( ctr_id, month )

  @staticmethod
  def update( month: int ):
    View_Graph.update_bar_color( month )
    View_Graph.update_bar_size()

  @staticmethod
  def update_bar_color( month: int ):
    today_month = Today.month()
    for ctr_id in View_Graph.ELEMENTS:
      for i in range( 12 ):
        button_p = View_Graph.ELEMENTS[ ctr_id ][ 'p' ][ i ]
        button_n = View_Graph.ELEMENTS[ ctr_id ][ 'n' ][ i ]
        if i + 1 == today_month:
          button_p.configure( fg_color = COLOR_CONTRAST )
          button_n.configure( fg_color = COLOR_CONTRAST )
        elif i + 1 == month:
          button_p.configure( fg_color = COLOR_CURRENT )
          button_n.configure( fg_color = COLOR_CURRENT )
        else:
          button_p.configure( fg_color = COLOR_1 )
          button_n.configure( fg_color = COLOR_BACKGROUND_2 )

  @staticmethod
  def update_bar_size():
    for ctr_id in View_Graph.ELEMENTS:
      data = View_Graph.get_data_category( ctr_id )
      maximum_bar_size = View_Graph.calculate_maximum_bar_size( data )
      for i in range( 12 ):
        button_p = View_Graph.ELEMENTS[ ctr_id ][ 'p' ][ i ]
        button_n = View_Graph.ELEMENTS[ ctr_id ][ 'n' ][ i ]

        height_p = View_Graph.calculate_bar_size( data[ "p" ][ i ], maximum_bar_size )
        height_n = View_Graph.calculate_bar_size( data[ "n" ][ i ], maximum_bar_size )

        button_p.configure( height = height_p )
        button_n.configure( height = height_n )

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

  @staticmethod
  def calculate_maximum_bar_size( data ):
    maximum = round( max( data[ "p" ] ) ) + 1
    minimum = round( min( data[ "n" ] ) ) - 1
    return max( abs( maximum ), abs( minimum ) )

  @staticmethod
  def calculate_bar_size( value, maximum_bar_size ):
    return (abs( value ) / maximum_bar_size) * 100
