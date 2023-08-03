import datetime

DAYS_IN_MONTH = [ -1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]


def is_leap( year ) -> bool:
  return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_days_in_month( year, month ) -> int:
  assert 1 <= month <= 12, month
  if month == 2 and is_leap( year ):
    return 29
  return DAYS_IN_MONTH[ month ]


def date( year: int, month: int = 1, day: int = 1 ) -> str:
  year, month = _rollover_months( year, month )
  year, month, day = _rollover_days( year, month, day )

  d = datetime.date( year, month, day )
  return d.strftime( "%Y%m%d" )


def _rollover_months( year: int, month: int ) -> list:
  while month > 12:
    month -= 12
    year += 1

  while month < 1:
    month += 12
    year -= 1

  return [ year, month ]


def _rollover_days( year: int, month: int, day: int ) -> list:
  if day > 28:
    days_in_month = get_days_in_month( year, month )
    while day > days_in_month:
      days_in_month = get_days_in_month( year, month )
      day -= days_in_month
      month += 1
  elif day == 0:
    day = 1
  elif day < 0:
    while day < 0:
      month -= 1
      year, month = _rollover_months( year, month )
      days_in_month = get_days_in_month( year, month )
      day += days_in_month + 1
      if day == 0:
        year, month = _rollover_months( year, month - 1 )
        day = get_days_in_month( year, month )

  year, month = _rollover_months( year, month )

  return [ year, month, day ]
