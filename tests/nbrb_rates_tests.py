from client import HttpClient
from rates import NbrbRates
import datetime

client = HttpClient(timeout=5)
nbrb_rates = NbrbRates(client)

print nbrb_rates.get_rate('USD', datetime.date(2017, 3, 12))
print nbrb_rates.get_today_rate('USD')
print nbrb_rates.get_rates_dynamics('USD', datetime.date(2017, 3, 1), datetime.date(2017, 3, 31))
print nbrb_rates.get_currencies()
