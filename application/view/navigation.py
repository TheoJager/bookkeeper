from application.constants import W10
from application.view.view import View
from application.date.today import Today
from application.ui.elements import Elements
from customtkinter import CTkFrame, CTkLabel


class Navigation:
  MONTH: int = 1
  ELEMENT: CTkLabel

  @staticmethod
  def next():
    Navigation.MONTH = 1 if Navigation.MONTH + 1 > 12 else Navigation.MONTH + 1
    View.update( Navigation.MONTH )

  @staticmethod
  def previous():
    Navigation.MONTH = 12 if Navigation.MONTH - 1 < 1 else Navigation.MONTH - 1
    View.update( Navigation.MONTH )

  @staticmethod
  def current():
    Navigation.MONTH = Today.month()
    View.update( Navigation.MONTH )


  @staticmethod
  def create( append: CTkFrame, column: int = 0, row: int = 0 ):
    frame = Elements.frame( append, column, row )
    frame.configure( fg_color = "transparent" )
    Elements.button_inverse( frame, "<<", Navigation.previous, 0, 0, (20, 0), W10 ).configure( width = 40 )
    Elements.button_inverse( frame, "now", Navigation.current, 1, 0, W10, W10 ).configure( width = 40 )
    Elements.button_inverse( frame, ">>", Navigation.next, 2, 0, W10, W10 ).configure( width = 40 )
    Elements.label( frame, "", 3, 0, W10, W10 )
