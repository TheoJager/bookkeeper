from customtkinter import CTkFrame, CTkLabel
from functions import format_amount
from ui.elements import Elements
from database.database_mutations import Database_Mutations


class View_Bank:
  ELEMENT: CTkLabel = None

  @staticmethod
  def reset():
    View_Bank.ELEMENT = None

  @staticmethod
  def create( append: CTkFrame, column: int = 0, row: int = 0 ):
    View_Bank.ELEMENT = Elements.header( append, "€ 0.00", column, row )

  @staticmethod
  def update():
    View_Bank.ELEMENT.configure( text = "€ " + format_amount( Database_Mutations.sum() ) )
