from customtkinter import CTkFrame, CTkLabel
from application.constants import W20
from application.ui.elements import Elements
from application.database.database_mutations import Database_Mutations
from application.functions import format_amount


class View_Bank:
  ELEMENT_BANK_TOTAL: CTkLabel = None

  @staticmethod
  def create( append: CTkFrame, column: int = 0, row: int = 0 ):
    View_Bank.ELEMENT_BANK_TOTAL = Elements.header( append, "€ 0.00", column, row, W20, W20 )

  @staticmethod
  def update():
    View_Bank.ELEMENT_BANK_TOTAL.configure( text = "€ " + format_amount( Database_Mutations.sum() ) )
