import locale
import datetime

from application.constants import W20, W10
from application.ui.elements import Elements
from customtkinter import CTkFrame, CTkLabel

# SETTINGS
#######################################

locale.setlocale( locale.LC_TIME, "nl_NL" )


class Navigation:
  MONTH: int = 1
  ELEMENT: CTkLabel

  @staticmethod
  def next():
    Navigation.MONTH = 1 if Navigation.MONTH + 1 > 12 else Navigation.MONTH + 1
    Navigation.update()

  @staticmethod
  def previous():
    Navigation.MONTH = 12 if Navigation.MONTH - 1 < 1 else Navigation.MONTH - 1
    Navigation.update()

  @staticmethod
  def current():
    Navigation.MONTH = Navigation.get_current_month()
    Navigation.update()

  @staticmethod
  def update():
    Navigation.ELEMENT.configure( text = Navigation.create_date() )

  @staticmethod
  def get_current_year() -> int:
    x = datetime.datetime.now()
    return int( x.strftime( "%Y" ) )

  @staticmethod
  def get_current_month() -> int:
    x = datetime.datetime.now()
    return int( x.strftime( "%m" ) )

  @staticmethod
  def create_date() -> str:
    current_year = Navigation.get_current_year()
    year = current_year if Navigation.MONTH >= Navigation.get_current_month() else current_year - 1

    d = datetime.date( year, Navigation.MONTH, 1 )
    return d.strftime( "%B %Y" )

  @staticmethod
  def create_element_date( append: CTkFrame, column: int = 0, row: int = 0 ):
    Navigation.ELEMENT = Elements.header( append, "januari 1970", column, row, W20, W20 )

  @staticmethod
  def create_navigation( append: CTkFrame, column: int = 0, row: int = 0 ):
    frame = Elements.frame( append, column, row )
    frame.configure( fg_color = "transparent" )
    Elements.button_inverse( frame, "<<", Navigation.previous, 0, 0, W10, W10 ).configure( width = 40 )
    Elements.button_inverse( frame, "now", Navigation.current, 1, 0, W10, W10 ).configure( width = 40 )
    Elements.button_inverse( frame, ">>", Navigation.next, 2, 0, W10, W10 ).configure( width = 40 )
    Elements.label( frame, "", 3, 0, W10, W10 )


# INITIALIZE
#######################################
Navigation.MONTH = Navigation.get_current_month()
