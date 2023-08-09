import datetime

from date.today import Today
from ui.elements import Elements
from customtkinter import CTkLabel, CTkFrame


class View_Date:
  ELEMENT: CTkLabel = None

  @staticmethod
  def reset():
    View_Date.ELEMENT = None

  @staticmethod
  def create( append: CTkFrame, column: int = 0, row: int = 0 ):
    View_Date.ELEMENT = Elements.header( append, "januari 1970", column, row )

  @staticmethod
  def update( month: int ):
    View_Date.ELEMENT.configure( text = View_Date.create_date( month ) )

  @staticmethod
  def create_date( month: int ) -> str:
    year = Today.year() - (1 if month > Today.month() else 0)

    d = datetime.date( year, month, 1 )
    return d.strftime( "%B %Y" )
