import math


def format_amount( amount: float ) -> str:
  return "{:.2f}".format( amount )


def format_percentage( percentage: float ) -> str:
  return "{:.1f}".format( percentage )


def round_up( value: int ) -> int:
  length = len( str( round( value ) ) ) - 1

  minimum = math.floor( value / pow( 10, length ) )
  minimum += 1

  return minimum * pow( 10, length )
