import datetime

# CONSTANTS
#######################################

FEBRUARY: int = 2

DAYS_FEBRUARY_LEAPYEAR: int = 29
DAYS_FEBRUARY_NON_LEAPYEAR: int = 28

MONTHS_PER_YEAR: int = 12

DAYS_IN_MONTH: list = [ -1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]


# WRAPPER FUNCTION
#######################################

def date( year: int, month: int = 1, day: int = 1 ) -> str:
  d = RolloverDate( year, month, day )
  return str( d )


# CLASS
#######################################

class RolloverDate:
  year: int = 1
  month: int = 1,
  day: int = 1

  def __init__( self, year: int, month: int = 1, day: int = 1 ):
    self.year, self.month = self._rollover_months( year, month )
    self.year, self.month, self.day = self._rollover_days( self.year, self.month, day )

  def __str__( self ) -> str:
    d = datetime.date( self.year, self.month, self.day )
    return d.strftime( "%Y%m%d" )

  def _is_leap( self, year ) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

  def _get_days_in_month( self, year, month ) -> int:
    assert 1 <= month <= MONTHS_PER_YEAR, month
    if month == FEBRUARY and self._is_leap( year ):
      return DAYS_FEBRUARY_LEAPYEAR
    return DAYS_IN_MONTH[ month ]

  def _rollover_months( self, year, month ) -> list:
    while month < 1:
      month = -1 if month == 0 else month
      month += MONTHS_PER_YEAR + 1
      year -= 1

    while month > MONTHS_PER_YEAR:
      month -= MONTHS_PER_YEAR
      year += 1

    return [ year, month ]

  def _rollover_days( self, year, month, day ) -> list:
    days_in_month = self._get_days_in_month( year, month )

    while day < 1:
      month -= 1
      year, month = self._rollover_months( year, month )
      days_in_month = self._get_days_in_month( year, month )

      day = -1 if day == 0 else day
      day += days_in_month + 1

    while day > days_in_month:
      day -= days_in_month

      month += 1
      year, month = self._rollover_months( year, month )
      days_in_month = self._get_days_in_month( year, month )

    return [ year, month, day ]
