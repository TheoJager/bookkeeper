from customtkinter import CTkFrame
from application.constants import W20
from application.ui.elements import Elements
from application.database.database_categories import Database_Categories

# GLOBALS
#######################################

ELEMENT_GRAPH = { }


# CLASS
#######################################

class View_Graph:

  @staticmethod
  def create_header( append: CTkFrame, column: int, name: str ):
    header = Elements.header( append, name, column, 0, (2, 0), W20 )
    header.grid( columnspan = 12 )

  @staticmethod
  def create_bars( append: CTkFrame, column: int, i: int ):
    progressbar = Elements.progressbar( append, column, 1, (1, 0), 20 )
    progressbar.set( i / 12 )

  @staticmethod
  def create( append: CTkFrame ):
    column = 0

    spacer = Elements.label( append, " ", column, 1, W20, W20 )
    spacer.grid( rowspan = 2 )

    column += 1

    for category in Database_Categories.select():
      View_Graph.create_header( append, column, category[ "ctr_name" ] )
      column += 1
      for i in range( 12 ):
        View_Graph.create_bars( append, column, i )
        column += 1

  @staticmethod
  def update():
    pass
