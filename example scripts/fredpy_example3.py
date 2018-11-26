'''This program creates a plot of HP and BP filtered real GDP for the US.

Created by: Brian C Jenkins. Email comments and suggestions to bcjenkin@uci.edu. Version date: November 26, 2018'''

import matplotlib.pyplot as plt
plt.style.use('classic')
import fredpy as fp
fp.api_key = fp.load_api_key('fred_api_key.txt')
import matplotlib.dates as dts

# download GDP data from FRED and convert into log per capita units
gdp = fp.series('GDPC96')
gdp = gdp.percapita()
gdp.data = gdp.data/1000
gdp = gdp.log()

# apply filters
gdp_hp_cycle, gdp_hp_trend = gdp.hpfilter()
gdp_bp_cycle, gdp_bp_trend = gdp.bpfilter()


# create figure and define x-axis tick locator for every 10 years
fig = plt.figure()
years10  = dts.YearLocator(10)

ax1 = fig.add_subplot(111)
ax1.plot_date(gdp_hp_cycle.datetimes,gdp_hp_cycle.data,'b-',lw = 3,alpha = 0.7,label='HP filter')
ax1.plot_date(gdp_bp_cycle.datetimes,gdp_bp_cycle.data,'r-',lw = 3,alpha = 0.7,label='BP filter')
ax1.xaxis.set_major_locator(years10)
ax1.set_ylabel('Percent')
fig.autofmt_xdate()
fig.tight_layout()
ax1.grid(True)
gdp.recessions()
ax1.legend(loc='lower right')
ax1.set_title('Quarterly GDP per Capita')

plt.savefig('fig_fredpy_example3.png',bbox_inches='tight')
plt.show()