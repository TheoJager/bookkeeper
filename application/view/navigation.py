import locale
import datetime

from application.constants import W20
from application.ui.elements import Elements
from customtkinter import CTkFrame, CTkLabel

# SETTINGS
#######################################

locale.setlocale(locale.LC_TIME, "nl_NL")


# CLASS
#######################################

class Navigation:

  @staticmethod
  def next():
    global CURRENT_MONTH
    CURRENT_MONTH = 1 if CURRENT_MONTH + 1 > 12 else CURRENT_MONTH + 1
    Navigation.update()


  @staticmethod
  def previous():
    global CURRENT_MONTH
    CURRENT_MONTH = 12 if CURRENT_MONTH - 1 < 1 else CURRENT_MONTH - 1
    Navigation.update()


  @staticmethod
  def current():
    global CURRENT_MONTH
    CURRENT_MONTH = Navigation.get_current_month()
    Navigation.update()


  @staticmethod
  def update():
    ELEMENT_CURRENT_MONTH.configure(text=Navigation.create_date())


  @staticmethod
  def get_current_year() -> int:
    x = datetime.datetime.now()
    return int(x.strftime("%Y"))


  @staticmethod
  def get_current_month() -> int:
    x = datetime.datetime.now()
    return int(x.strftime("%m"))


  @staticmethod
  def create_date() -> str:
    current_year = Navigation.get_current_year()
    year = current_year if CURRENT_MONTH >= Navigation.get_current_month() else current_year - 1

    d = datetime.date(year, CURRENT_MONTH, 1)
    return d.strftime("%B %Y")


  @staticmethod
  def create_element_date(append: CTkFrame, column: int = 0, row: int = 0):
    global ELEMENT_CURRENT_MONTH

    ELEMENT_CURRENT_MONTH = Elements.header(append, "januari 1970", column, row, W20, W20)


  @staticmethod
  def create_navigation(append: CTkFrame, column: int = 0, row: int = 0):
    frame = Elements.frame(append, column, row)
    frame.configure(fg_color="transparent")
    Elements.button_inverse(frame, "<<", Navigation.previous, 0, 0, W20, W20).configure(width=50)
    Elements.button_inverse(frame, "NU", Navigation.current, 1, 0, W20, W20).configure(width=50)
    Elements.button_inverse(frame, ">>", Navigation.next, 2, 0, W20, W20).configure(width=50)
    Elements.label(frame, "", 3, 0, W20, W20)


# GLOBALS
#######################################
CURRENT_MONTH = Navigation.get_current_month()
ELEMENT_CURRENT_MONTH: CTkLabel
