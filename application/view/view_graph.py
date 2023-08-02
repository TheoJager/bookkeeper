import math

from customtkinter import CTkFrame, CTkProgressBar
from application.ui.elements import Elements
from application.view.view_date import View_Date
from application.view.view_month import View_Month
from application.view.view_table import View_Table
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories


class View_Graph:
  ELEMENTS = { }

  @staticmethod
  def reset():
    View_Graph.ELEMENTS = { }

  @staticmethod
  def create_header( append: CTkFrame, column: int, name: str ):
    header = Elements.header( append, name, column, 0, (2, 0) )
    header.grid( columnspan = 12 )

  @staticmethod
  def create_bars( append: CTkFrame, column: int, i: int ):
    progressbar = Elements.progressbar( append, column, 1, (1, 0), 20 )
    progressbar.set( i / 12 )
    return progressbar

  @staticmethod
  def register_bar( bar: CTkProgressBar, name: str, i: int ):
    View_Graph.ELEMENTS[ name ] = View_Graph.ELEMENTS[ name ] if name in View_Graph.ELEMENTS else { }
    View_Graph.ELEMENTS[ name ][ i ] = bar
    return bar

  @staticmethod
  def create_spacer( append: CTkFrame, column: int ):
    spacer = Elements.label( append, " ", column, 1 )
    spacer.grid( rowspan = 2 )

  @staticmethod
  def create( append: CTkFrame ):
    column = 0

    View_Graph.create_spacer( append, column )

    column += 1

    for category in Database_Categories.select():
      View_Graph.create_header( append, column, category[ "ctr_name" ] )

      amounts = Database_Mutations.sum_category_months( category[ "ctr_id" ] )
      maximum = View_Graph.calculate_upper_limit( amounts )

      column += 1
      for i in range( 12 ):
        bar = View_Graph.register_bar( View_Graph.create_bars( append, column, i ), category[ "ctr_name" ], i )
        bar.set( abs( amounts[ i ] ) / maximum )

        button = Elements.button( append, " ", lambda i = i: View_Graph.update_screen( i + 1 ), column, 2, 0, 0 )
        button.configure( width = 1, height = 1, corner_radius = 0 )
        column += 1

      View_Graph.create_spacer( append, column )
      column += 1

  @staticmethod
  def update_screen( month: int ):
    View_Graph.update( month )
    View_Date.update( month )
    View_Month.update( month )
    View_Table.update( month )

  @staticmethod
  def update( month: int ):
    for category in Database_Categories.select():
      bars = View_Graph.ELEMENTS[ category[ "ctr_name" ] ]
      for i in bars:
        if i + 1 == month:
          bars[ i ].configure( progress_color = "#A2972F" )
        else:
          bars[ i ].configure( progress_color = "#2FA572" )

  @staticmethod
  def calculate_upper_limit( amounts ):
    maximum = round( max( amounts ) )
    length = len( str( maximum ) ) - 1

    minimum = math.floor( maximum / pow( 10, length ) )
    minimum += 1

    return minimum * pow( 10, length )
