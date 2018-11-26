'''This program creates a plot of real GDP growth, CPI inflation, the unemployment rate, and the 3-month T-bill rate

Created by: Brian C Jenkins. Email comments and suggestions to bcjenkin@uci.edu. Version date: November 26, 2018'''

import matplotlib.pyplot as plt
plt.style.use('classic')
import fredpy as fp
fp.api_key = fp.load_api_key('fred_api_key.txt')
import matplotlib.dates as dts

# download data from FRED
gdp = fp.series('GDPC96')
cpi = fp.series('CPIAUCSL')
unemp=fp.series('UNRATE')
tbill=fp.series('TB3MS')

# express GDP in trillions by dividing original data by 1000
gdp.data = gdp.data/1000

# find the annual percentage changes in GDP and inflation
gdp = gdp.apc()
cpi = cpi.apc()

# equalize the data windows
gdp,cpi,unemp,tbill = fp.window_equalize([gdp,cpi,unemp,tbill])

# create figure and define x-axis tick locator for every 10 years
fig = plt.figure()
years10  = dts.YearLocator(10)

ax1 = fig.add_subplot(221)
ax1.plot_date(gdp.datetimes,gdp.data,'b-',lw = 2)
ax1.xaxis.set_major_locator(years10)
ax1.set_ylabel('Percent')
fig.autofmt_xdate()
ax1.grid(True)
gdp.recessions()
ax1.set_title('Real GDP')

ax2 = fig.add_subplot(222)
ax2.plot_date(cpi.datetimes,cpi.data,'b-',lw = 2)
ax2.xaxis.set_major_locator(years10)
ax2.set_ylabel('Percent')
fig.autofmt_xdate()
ax2.grid(True)
cpi.recessions()
ax2.set_title('CPI Inflation')

ax3 = fig.add_subplot(223)
ax3.plot_date(unemp.datetimes,unemp.data,'b-',lw = 2)
ax3.xaxis.set_major_locator(years10)
ax3.set_ylabel('Percent')
fig.autofmt_xdate()
ax3.grid(True)
unemp.recessions()
ax3.set_title('Unemployment Rate')

ax4 = fig.add_subplot(224)
ax4.plot_date(tbill.datetimes,tbill.data,'b-',lw = 2)
ax4.xaxis.set_major_locator(years10)
ax4.set_ylabel('Percent')
fig.autofmt_xdate()
ax4.grid(True)
tbill.recessions()
ax4.set_title('3-mo T-bill Rate')

plt.savefig('fig_fredpy_example2.png',bbox_inches='tight')
plt.show()