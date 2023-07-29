from application.view.bank import View_Bank
from application.view.date import View_Date
from application.view.year import View_Year
from application.view.table import View_Table
from application.view.graph import View_Graph
from application.view.month import View_Month


class View:

  @staticmethod
  def initiate():
    View_Bank.update()
    View_Year.update()
    View_Graph.update()

  @staticmethod
  def update( month: int ):
    View_Date.update( month )
    View_Month.update( month )
    View_Table.update( month )
