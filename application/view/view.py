from view.view_bank import View_Bank
from view.view_date import View_Date
from view.view_year import View_Year
from view.view_table import View_Table
from view.view_graph import View_Graph
from view.view_month import View_Month


class View:

  @staticmethod
  def initiate():
    View_Bank.update()
    View_Year.update()

  @staticmethod
  def update( month: int ):
    View_Graph.update( month )
    View_Date.update( month )
    View_Month.update( month )
    View_Table.update( month )
