from customtkinter import *


class Elements:

  @staticmethod
  def grid( element: CTkBaseClass, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1, padx: int = 0, pady: int = 0 ) -> CTkBaseClass:
    element.grid( column = column, row = row, columnspan = columnspan, rowspan = rowspan, padx = padx, pady = pady, sticky = "nsew" )
    return element

  @staticmethod
  def frame( append: CTkBaseClass, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1, padx: int = 0, pady: int = 0 ) -> CTkFrame:
    return Elements.grid( CTkFrame( append ), column, row, columnspan, rowspan, padx, pady )

  @staticmethod
  def scroll( append: CTkBaseClass, column: int = 0, row: int = 0, columnspan: int = 1, rowspan: int = 1, padx: int = 0, pady: int = 0 ) -> CTkScrollableFrame:
    return Elements.grid( CTkScrollableFrame( append ), column, row, columnspan, rowspan, padx, pady )

  @staticmethod
  def title( append: CTkBaseClass, text: str, column: int = 0, row: int = 0, padx: int = 0, pady: int = 0 ) -> CTkLabel:
    return Elements.grid( CTkLabel( append, text = text, font = CTkFont( size = 24, weight = "bold" ) ), column, row, 1, 1, padx, pady )

  @staticmethod
  def header( append: CTkBaseClass, text: str, column: int = 0, row: int = 0, padx: int = 0, pady: int = 0 ) -> CTkLabel:
    elements = Elements.grid( CTkLabel( append, text = text, font = CTkFont( size = 13, weight = "bold" ) ), column, row, 1, 1, padx, pady )
    elements.grid( sticky = "nsw" )
    return elements

  @staticmethod
  def label( append: CTkBaseClass, text: str, column: int = 0, row: int = 0, padx: int = 0, pady: int = 0 ) -> CTkLabel:
    elements = Elements.grid( CTkLabel( append, text = text, font = CTkFont( size = 13 ) ), column, row, 1, 1, padx, pady )
    elements.grid( sticky = "nsw" )
    return elements

  @staticmethod
  def progressbar( append: CTkBaseClass, column: int = 0, row: int = 0, padx: int = 0, pady: int = 0 ) -> CTkProgressBar:
    elements = Elements.grid( CTkProgressBar( append, orientation = "vertical" ), column, row, 1, 1, padx, pady )
    elements.grid( sticky = "nsw" )
    return elements

  @staticmethod
  def button( append: CTkBaseClass, text: str, command: callable, column: int = 0, row: int = 0, padx: int = 0, pady: int = 0 ) -> CTkButton:
    return Elements.grid( CTkButton( append, text = text, command = command ), column, row, 1, 1, padx, pady )

  @staticmethod
  def button_inverse( append: CTkBaseClass, text: str, command: callable, column: int = 0, row: int = 0, padx: int = 0, pady: int = 0 ) -> CTkButton:
    element = Elements.grid( CTkButton( append, text = text, command = command ), column, row, 1, 1, padx, pady )
    element.configure( fg_color = "transparent", text_color = ("gray10", "#DCE4EE"), border_width = 1 )
    return element
