import datetime


class Today:

  @staticmethod
  def year():
    x = datetime.datetime.now()
    return int( x.strftime( "%Y" ) )

  @staticmethod
  def month():
    x = datetime.datetime.now()
    return int( x.strftime( "%m" ) )
