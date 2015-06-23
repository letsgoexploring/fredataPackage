'''This program creates a plot of HP and BP filtered real GDP for the US.

Created by: Brian C Jenkins. Email comments and suggestions to bcjenkin@uci.edu. Version date: August 29, 2014'''

from __future__ import division
import matplotlib.pyplot as plt
from fredclass import fred, window_equalize
import matplotlib.dates as dts

# download GDP data from FRED and convert into log per capita units
gdp = series('GDPC96')
gdp.percapita()
gdp.data = gdp.data/1000
gdp.log()

# apply filters
gdp.bpfilter()
gdp.hpfilter()

# create figure and define x-axis tick locator for every 10 years
fig = plt.figure()
years10  = dts.YearLocator(10)

ax1 = fig.add_subplot(111)
ax1.plot_date(gdp.datenums,gdp.hpcycle,'b-',lw = 2)
ax1.plot_date(gdp.bpdatenums,gdp.bpcycle,'r--',lw = 2)
ax1.xaxis.set_major_locator(years10)
ax1.set_ylabel('Percent')
fig.autofmt_xdate()
ax1.grid(True)
gdp.recessions()
ax1.legend(['HP','BP'],loc='lower right')

plt.savefig('fig_fredclass_example3.png',bbox_inches='tight')
plt.show()