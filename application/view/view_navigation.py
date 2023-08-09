import globals as glb

from constants import W10, W20
from view.view import View
from date.today import Today
from ui.elements import Elements
from customtkinter import CTkFrame, CTkLabel


class Navigation:
  ELEMENT: CTkLabel = None

  @staticmethod
  def reset():
    Navigation.ELEMENT = None

  @staticmethod
  def next():
    glb.SELECTED_MONTH = 1 if glb.SELECTED_MONTH + 1 > 12 else glb.SELECTED_MONTH + 1
    View.update( glb.SELECTED_MONTH )

  @staticmethod
  def previous():
    glb.SELECTED_MONTH = 12 if glb.SELECTED_MONTH - 1 < 1 else glb.SELECTED_MONTH - 1
    View.update( glb.SELECTED_MONTH )

  @staticmethod
  def current():
    glb.SELECTED_MONTH = Today.month()
    View.update( glb.SELECTED_MONTH )

  @staticmethod
  def create( append: CTkFrame, column: int = 0, row: int = 0 ):
    frame = Elements.frame( append, column, row )
    frame.configure( fg_color = "transparent" )
    Elements.button_inverse( frame, "<<", Navigation.previous, 0, 0, W20, W10 ).configure( width = 40 )
    Elements.button_inverse( frame, "now", Navigation.current, 1, 0, W10, W10 ).configure( width = 40 )
    Elements.button_inverse( frame, ">>", Navigation.next, 2, 0, W10, W10 ).configure( width = 40 )
    Elements.label( frame, "", 3, 0, W10, W10 )
