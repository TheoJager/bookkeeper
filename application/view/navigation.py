import locale
import datetime

from application.constants import W20
from application.ui.elements import Elements
from customtkinter import CTkFrame, CTkLabel

# SETTINGS
#######################################

locale.setlocale(locale.LC_TIME, "nl_NL")


# FUNCTIONS
#######################################

def next_month():
  global CURRENT_MONTH
  CURRENT_MONTH = 1 if CURRENT_MONTH + 1 > 12 else CURRENT_MONTH + 1
  update_month()


def previous_month():
  global CURRENT_MONTH
  CURRENT_MONTH = 12 if CURRENT_MONTH - 1 < 1 else CURRENT_MONTH - 1
  update_month()


def current_month():
  global CURRENT_MONTH
  CURRENT_MONTH = get_current_month()
  update_month()


def update_month():
  ELEMENT_CURRENT_MONTH.configure(text=create_date())


def get_current_year() -> int:
  x = datetime.datetime.now()
  return int(x.strftime("%Y"))


def get_current_month() -> int:
  x = datetime.datetime.now()
  return int(x.strftime("%m"))


def create_date() -> str:
  current_year = get_current_year()
  year = current_year if CURRENT_MONTH >= NOW_MONTH else current_year - 1

  d = datetime.date(year, CURRENT_MONTH, 1)
  return d.strftime("%B %Y")


def create_element_date(append: CTkFrame, column: int = 0, row: int = 0):
  global ELEMENT_CURRENT_MONTH

  ELEMENT_CURRENT_MONTH = Elements.header(append, "januari 1970", column, row, W20, W20)


def create_navigation(append: CTkFrame, column: int = 0, row: int = 0):
  frame = Elements.frame(append, column, row)
  frame.configure(fg_color="transparent")
  Elements.button_inverse(frame, "<<", previous_month, 0, 0, W20, W20).configure(width=50)
  Elements.button_inverse(frame, "NU", current_month, 1, 0, W20, W20).configure(width=50)
  Elements.button_inverse(frame, ">>", next_month, 2, 0, W20, W20).configure(width=50)
  Elements.label(frame, "", 3, 0, W20, W20)


# GLOBALS
#######################################
CURRENT_MONTH = get_current_month()
NOW_MONTH = get_current_month()
ELEMENT_CURRENT_MONTH: CTkLabel
