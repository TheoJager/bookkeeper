import math
import matplotlib.pyplot as plt

from customtkinter import CTkFrame, CTkProgressBar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from application.constants import COLOR_CONTRAST, COLOR_CURRENT_BAR, COLOR_BACKGROUND, COLOR_BACKGROUND_BAR
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
  def register_bar( bar: CTkProgressBar, name: str, i: int ):
    View_Graph.ELEMENTS[ name ] = View_Graph.ELEMENTS[ name ] if name in View_Graph.ELEMENTS else { }
    View_Graph.ELEMENTS[ name ][ i ] = bar
    return bar

  @staticmethod
  def create_spacer( append: CTkFrame, column: int ):
    spacer = Elements.label( append, " ", column, 1 )
    spacer.grid( rowspan = 2 )

  @staticmethod
  def create_frame( append: CTkFrame, column:int, row:int, height:int ) -> CTkFrame:
    frame = Elements.frame( append, column, row )
    frame.configure( width = 300, height = height, fg_color = "transparent" )
    return frame

  @staticmethod
  def create( append: CTkFrame ):
    column = 0

    View_Graph.create_spacer( append, column )

    for category in Database_Categories.select():
      View_Graph.create_header( append, column, category[ "ctr_name" ] )

      amounts = Database_Mutations.sum_category_months( category[ "ctr_id" ] )
      # maximum = View_Graph.calculate_upper_limit( amounts )

      data_positive = [0] * 12
      data_negative = [0] * 12

      for i in range( 12 ):
        if amounts[i] >= 0:
          data_positive[i] = amounts[i]
        else:
          data_negative[i] = amounts[i]

      View_Graph.draw_graph(append, column, 2, data_positive, data_negative )

      for i in range( 12 ):
        button = Elements.button( append, " ", lambda i = i: View_Graph.update_screen( i + 1 ), column, 1, 0, 0 )
        button.configure( width = 1, height = 1, corner_radius = 0 )
        column += 1

      View_Graph.create_spacer( append, column )
      column += 1

  @staticmethod
  def update_screen( month: int ):
    # View_Graph.update( month )
    View_Date.update( month )
    View_Month.update( month )
    View_Table.update( month )

  @staticmethod
  def update( month: int ):
    for category in Database_Categories.select():
      bars = View_Graph.ELEMENTS[ category[ "ctr_name" ] ]
      for i in bars:
        if i + 1 == month:
          bars[ i ].configure( progress_color = COLOR_CURRENT_BAR )
        else:
          bars[ i ].configure( progress_color = COLOR_CONTRAST )

  @staticmethod
  def draw_graph( append: CTkFrame, column: int, row: int, data_positive: list, data_negative: list ):
    plt.axis( 'off' )

    maximum = round( max( data_positive ) )
    minimum = round( max( data_negative ) )
    size = max(abs(maximum), abs(minimum))

    fig = plt.figure( figsize = (1.5, 2), facecolor = COLOR_BACKGROUND )
    fig.subplots_adjust( left = 0, bottom = 0, right = 0.97, top = 0.97, wspace = 0, hspace = 0 )

    x = range( 12 )
    ax = plt.subplot( 111 )
    ax.bar( x, data_negative, width = 0.8, color = COLOR_BACKGROUND_BAR )
    ax.bar( x, data_positive, width = 0.8, color = COLOR_CONTRAST )

    ax.bar( 13, +size, width = 0.8, color = COLOR_BACKGROUND )
    ax.bar( 13, -size, width = 0.8, color = COLOR_BACKGROUND )

    canvas = FigureCanvasTkAgg( fig, master = append )
    canvas.get_tk_widget().grid( row = row, column = column, ipadx = 0, ipady = 0, sticky = "nw", columnspan=12 )
    canvas.draw()
