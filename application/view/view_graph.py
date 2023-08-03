from typing import Dict

import matplotlib.pyplot as plt

from customtkinter import CTkFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from application.constants import COLOR_1, COLOR_BACKGROUND_1, COLOR_BACKGROUND_2, W10, COLOR_CONTRAST, COLOR_2
from application.date.today import Today
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
  def update_screen( month: int, ctr_id: int ):
    View_Date.update( month )
    View_Month.update( month )
    View_Table.update_category_month( ctr_id, month )

  @staticmethod
  def update_screen_total( month: int ):
    View_Date.update( month )
    View_Month.update( month )
    View_Table.update( month )

  @staticmethod
  def create( append: CTkFrame ):
    column = 0

    View_Graph.create_graph_total( append, "totaal", View_Graph.get_data_months(), column )

    column += 1
    for ctr in Database_Categories.select():
      data = View_Graph.get_data_category( ctr[ "ctr_id" ] )

      View_Graph.create_graph( append, ctr, data, column )

      column += 1

    View_Graph.create_bars( append, 100, 100, { "p": [ 0 ] * 12, "n": [ 0 ] * 12 }, (0, 0) )

  @staticmethod
  def create_graph( append: CTkFrame, ctr: Dict, data: Dict, column: int ):
    View_Graph.create_header( append, ctr[ "ctr_name" ], column, 0 )

    View_Graph.create_bars( append, column, 1, data )

    View_Graph.create_buttons( append, ctr[ "ctr_id" ], column, 2 )

  @staticmethod
  def create_graph_total( append: CTkFrame, ctr_name: str, data: Dict, column: int ):
    View_Graph.create_header( append, ctr_name, column, 0 )

    View_Graph.create_bars( append, column, 1, data )

    View_Graph.create_buttons_total( append, column, 2 )

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

    maximum = round( max( data[ "p" ] ) )
    minimum = round( max( data[ "n" ] ) )
    size = max( abs( maximum ), abs( minimum ) )

    fig = plt.figure( figsize = demension, facecolor = COLOR_BACKGROUND_1 )
    fig.subplots_adjust( left = 0, bottom = 0, right = 0.97, top = 0.97, wspace = 0, hspace = 0 )

    x = range( 12 )
    ax = plt.subplot( 111 )
    ax.bar( x, data[ "p" ], width = 0.8, color = COLOR_1 )
    ax.bar( x, data[ "n" ], width = 0.8, color = COLOR_BACKGROUND_2 )

    ax.bar( 13, +size, width = 0.8, color = COLOR_BACKGROUND_1 )
    ax.bar( 13, -size, width = 0.8, color = COLOR_BACKGROUND_1 )

    canvas = FigureCanvasTkAgg( fig, master = append )
    canvas.get_tk_widget().grid( ipadx = 0, ipady = 0, sticky = "nw" )
    canvas.draw()

  @staticmethod
  def create_buttons( append: CTkFrame, ctr_id: int, column: int, row: int ):
    append = View_Graph.create_frame( append, column, row )
    append.grid( padx = (13, 0) )

    today_month = Today.month()
    for i in range( 12 ):
      button = Elements.button( append, " ", lambda i = i: View_Graph.update_screen( i + 1, ctr_id ), i, 0, 0, 0 )
      button.configure( width = 1, height = 1, corner_radius = 0 )
      if i in (3, 4, 5):
        button.configure( fg_color = COLOR_2 )
      elif i in (9, 10, 11):
        button.configure( fg_color = COLOR_2 )

      if i + 1 == today_month:
        button.configure( fg_color = COLOR_CONTRAST )

  @staticmethod
  def create_buttons_total( append: CTkFrame, column: int, row: int ):
    append = View_Graph.create_frame( append, column, row )
    append.grid( padx = (13, 0) )

    today_month = Today.month()
    for i in range( 12 ):
      button = Elements.button( append, " ", lambda i = i: View_Graph.update_screen_total( i + 1 ), i, 0, 0, 0 )
      button.configure( width = 1, height = 1, corner_radius = 0 )
      if i in (3, 4, 5):
        button.configure( fg_color = COLOR_2 )
      elif i in (9, 10, 11):
        button.configure( fg_color = COLOR_2 )

      if i + 1 == today_month:
        button.configure( fg_color = COLOR_CONTRAST )

  @staticmethod
  def get_data_months():
    amounts = Database_Mutations.sum_months()

    data = { "p": [ 0 ] * 12, "n": [ 0 ] * 12 }

    for i in range( 12 ):
      if amounts[ i ] >= 0:
        data[ "p" ][ i ] = amounts[ i ]
      else:
        data[ "n" ][ i ] = amounts[ i ]

    return data

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
