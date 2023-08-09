import matplotlib.pyplot as plt

from typing import Dict
from customtkinter import CTkFrame, CTkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants import COLOR_1, COLOR_BACKGROUND_1, COLOR_BACKGROUND_2, W10, COLOR_CONTRAST, COLOR_CURRENT
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

    View_Graph.create_bars( append, 100, 100, { "p": [ 0 ], "n": [ 0 ] }, (0, 0) )

  @staticmethod
  def create_graph( append: CTkFrame, ctr: Dict, data: Dict, column: int ):
    View_Graph.create_header( append, ctr[ "ctr_name" ], column, 0 )

    View_Graph.create_bars( append, column, 1, data )

    View_Graph.create_buttons( append, ctr[ "ctr_id" ], column, 2, View_Graph.update_screen )

  @staticmethod
  def create_frame( append: CTkFrame, column: int, row: int ) -> CTkFrame:
    frame = Elements.frame( append, column, row )
    frame.configure( fg_color = "transparent" )
    return frame

  @staticmethod
  def create_header( append: CTkFrame, ctr_name: str, column: int, row: int ):
    append = View_Graph.create_frame( append, column, row )
    append.grid( padx = W10 )

    header = Elements.header( append, ctr_name, 0, 0, (2, 0) )
    header.grid( columnspan = 12 )

  @staticmethod
  def create_bars( append: CTkFrame, column: int, row: int, data: Dict, demension: list = (1.5, 2) ):
    append = View_Graph.create_frame( append, column, row )

    plt.axis( 'off' )

    maximum = round( max( data[ "p" ] ) ) + 1
    minimum = round( min( data[ "n" ] ) ) - 1
    size = max( abs( maximum ), abs( minimum ) )

    fig = plt.figure( figsize = demension, facecolor = COLOR_BACKGROUND_1 )
    fig.subplots_adjust( left = 0, bottom = 0, right = 0.97, top = 0.97, wspace = 0, hspace = 0 )

    today_month = Today.month()

    p = data[ "p" ][ today_month: ] + data[ "p" ][ :today_month ]
    n = data[ "n" ][ today_month: ] + data[ "n" ][ :today_month ]

    x = range( 12 )
    ax = plt.subplot( 111 )
    ax.bar( x, p, width = 0.8, color = COLOR_1 )
    ax.bar( x, n, width = 0.8, color = COLOR_BACKGROUND_2 )

    ax.bar( 13, +size, width = 0.8, color = COLOR_BACKGROUND_1 )
    ax.bar( 13, -size, width = 0.8, color = COLOR_BACKGROUND_1 )

    canvas = FigureCanvasTkAgg( fig, master = append )
    canvas.get_tk_widget().grid( ipadx = 0, ipady = 0, sticky = "nw" )
    canvas.draw()

  @staticmethod
  def create_buttons( append: CTkFrame, ctr_id: int, column: int, row: int, command: callable ):
    append = View_Graph.create_frame( append, column, row )
    append.grid( padx = (13, 0) )

    View_Graph.ELEMENTS[ ctr_id ] = { }

    today_month = Today.month()
    m = [ "J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D" ]
    a = list( range( today_month, 12 ) ) + list( range( today_month ) )

    column = 0
    for i in a:  # range( 12 ):
      View_Graph.ELEMENTS[ ctr_id ][ i ] = View_Graph.create_buttons_button(
        append, column, lambda i = i: command( i + 1, ctr_id )
      )
      View_Graph.create_buttons_label(
        append, column, m[ i ]
      )
      column += 1

  @staticmethod
  def create_buttons_button( append: CTkFrame, column: int, command: callable ):
    button = Elements.button( append, " ", command, column, 0, 0, 0 )
    button.configure( width = 1, height = 1, corner_radius = 0 )
    return button

  @staticmethod
  def create_buttons_label( append: CTkFrame, column: int, value: str ):
    label = Elements.label( append, value, column, 1, 0, 0 )
    label.configure( width = 2, height = 1, corner_radius = 0, font = CTkFont( size = 8 ) )
    label.grid( padx = (1, 0) )
    return label

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
