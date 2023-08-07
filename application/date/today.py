import datetime


class Today:

  @staticmethod
  def year() ->int:
    x = datetime.datetime.now()
    return int( x.strftime( "%Y" ) )

  @staticmethod
  def month() ->int:
    x = datetime.datetime.now()
    return int( x.strftime( "%m" ) )
