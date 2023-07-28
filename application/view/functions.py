from application.view.bank import View_Bank
from application.view.year import View_Year
from application.view.graph import View_Graph
from application.view.month import View_Month
from application.view.navigation import Navigation


def view_update():
  Navigation.update()
  View_Bank.update()
  View_Year.update()
  View_Month.update()
  View_Graph.update()
