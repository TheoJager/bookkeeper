import math

from customtkinter import CTkFrame
from application.constants import W20
from application.ui.elements import Elements
from application.database.database_categories import Database_Categories
from database.database_mutations import Database_Mutations


class View_Graph:
  ELEMENTS = { }

  @staticmethod
  def create_header( append: CTkFrame, column: int, name: str ):
    header = Elements.header( append, name, column, 0, (2, 0), W20 )
    header.grid( columnspan = 12 )

  @staticmethod
  def create_bars( append: CTkFrame, column: int, i: int ):
    progressbar = Elements.progressbar( append, column, 1, (1, 0), 20 )
    progressbar.set( i / 12 )
    return progressbar

  @staticmethod
  def create_spacer( append: CTkFrame, column: int ):
    spacer = Elements.label( append, " ", column, 1, W20, W20 )
    spacer.grid( rowspan = 2 )

  @staticmethod
  def create( append: CTkFrame ):
    column = 0

    View_Graph.create_spacer( append, column )

    column += 1

    for category in Database_Categories.select():
      View_Graph.create_header( append, column, category[ "ctr_name" ] )
      column += 1
      for i in range( 12 ):
        View_Graph.ELEMENTS[ category[ "ctr_name" ] ] = View_Graph.ELEMENTS[ category[ "ctr_name" ] ] if category[ "ctr_name" ] in View_Graph.ELEMENTS else { }
        View_Graph.ELEMENTS[ category[ "ctr_name" ] ][ i ] = View_Graph.create_bars( append, column, i )
        column += 1

      View_Graph.create_spacer( append, column )
      column += 1

  @staticmethod
  def update():
    for category in Database_Categories.select():
      amounts = Database_Mutations.list_sum_category_month( category[ "ctr_id" ] )
      maximum = View_Graph.calculate_upper_limit( amounts )

      bars = View_Graph.ELEMENTS[ category[ "ctr_name" ] ]
      for i in bars:
        bars[ i ].set( abs(amounts[ i ]) / maximum )

  @staticmethod
  def calculate_upper_limit( amounts ):
    maximum = round( max( amounts ) )
    length = len( str( maximum ) ) - 1

    minimum = math.floor( maximum / pow( 10, length ) )
    minimum += 1

    return minimum * pow( 10, length )
