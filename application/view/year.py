from customtkinter import CTkFrame
from application.ui.elements import Elements
from application.constants import W20, CATEGORY_INCOME
from application.categories.categories import paint_category_year
from application.database.database_mutations import Database_Mutations
from application.database.database_categories import Database_Categories

# GLOBALS
#######################################

ELEMENT_VIEW_TOTAL = {}

# CLASS
#######################################

class View_Year:

  @staticmethod
  def create(append: CTkFrame):
    row = 0
    for category in Database_Categories.select():
      Elements.label(append, category["ctr_name"], 1, row, W20, W20).configure(anchor="w", width=125)
      Elements.label(append, "€", 2, row, W20, W20)
      s = Elements.label(append, "0.00", 3, row, (10,0), W20)
      p = Elements.label(append, "0.00", 4, row, (10,0), W20)
      Elements.label(append, "%", 5, row, (10, 10), W20)
      Elements.button(append, "@", paint_category_year, 6, row, (20, 20), W20).configure(width=25)

      s.configure(anchor="e", width=60)
      p.configure(anchor="e", width=60)

      ELEMENT_VIEW_TOTAL[category["ctr_name"]] = [s, p]
      row += 1

  @staticmethod
  def update():
    income = Database_Mutations.sum_category_year(CATEGORY_INCOME)

    for category in Database_Categories.select():
      current = Database_Mutations.sum_category_year(category["ctr_id"])
      percent = View_Year.calculate_percentage(current, income)

      s, p = ELEMENT_VIEW_TOTAL[category["ctr_name"]]
      s.configure(text=View_Year.format_amount(current))
      p.configure(text=View_Year.format_percentage(percent))

  @staticmethod
  def calculate_percentage(amount, income) -> float:
    return 0 if income == 0 else round((amount / income) * 100, 1)

  @staticmethod
  def format_amount(amount: float):
    return "{:.2f}".format(amount)

  @staticmethod
  def format_percentage(percentage: float):
    return "{:.1f}".format(percentage)
