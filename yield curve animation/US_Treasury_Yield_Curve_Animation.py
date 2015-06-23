'''This program produces an mp4-format video of daily US Treasury yield curves for the US from January 1, 1965 to July 31, 2014.'''

from __future__ import division
import matplotlib
matplotlib.use("Agg")
import fredpy, dateutil, datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as dts
from yield_curve import yc

# Initial and final dates for video
date_alpha = '1965-01-01'
date_omega = '2014-07-31'
win        = [date_alpha,date_omega]
dateT      = dateutil.parser.parse(date_omega)
t          = dateutil.parser.parse(date_alpha)
N          = 0
day        = datetime.timedelta(days =1)
dates, date_strs, maturities, yield_curves,masks = [],[],[],[],[]

# Create Fred objects
y1m= fredpy.series('DTB4WK')
y3m= fredpy.series('DTB3')
y6m= fredpy.series('DTB6')
y1 = fredpy.series('DGS1')
y5 = fredpy.series('DGS5')
y10= fredpy.series('DGS10')
y20= fredpy.series('DGS20')
y30= fredpy.series('DGS30')

# Limit all data series to the same date windows
y1m.window(win)
y3m.window(win)
y6m.window(win)
y1.window(win)
y5.window(win)
y10.window(win)
y20.window(win)
y30.window(win)

all_yields = [y1m,y3m,y6m,y1,y5,y10,y20,y30] 

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=50, metadata=dict(artist='Brian C Jenkins'), bitrate=50000)

# Initialize figure
fig = plt.figure(figsize=(16,9))
years    = dts.YearLocator(10)

ax1 = fig.add_subplot(1, 1, 1)
line1, = ax1.plot([], [], lw=8)
ax1.grid()

ax1.set_xlim(0,6)
ax1.set_ylim(0,18)

ax1.set_xticks(range(7))
ax1.set_yticks([2,4,6,8,10,12,14,16,18])

xlabels = ['1m','3m','6m','2y','5y','10y','30y']
ylabels = [2,4,6,8,10,12,14,16,18]

ax1.set_xticklabels(xlabels,fontsize=20)
ax1.set_yticklabels(ylabels,fontsize=20)

figure_title = 'U.S. Treasury Bond Yield Curve'
figure_xlabel = 'Time to Maturity'
figure_ylabel = '%'

plt.text(0.5, 1.03, figure_title,horizontalalignment='center',fontsize=30,transform = ax1.transAxes)
plt.text(0.5, -.1, figure_xlabel,horizontalalignment='center',fontsize=25,transform = ax1.transAxes)
plt.text(-0.05, .5, figure_ylabel,horizontalalignment='center',fontsize=25,rotation='vertical',transform = ax1.transAxes)

ax1.text(3.75,.25, 'Created by Brian C Jenkins',fontsize=11, color='black',alpha=0.5)#,
date_text = ax1.text(0.1, 16.625, '',fontsize=18)


# Form the animation and save
while t <= dateT:
	date, maturity, yield_curve, ymask = yc(t.strftime('%Y-%m-%d'),all_yields)
	while all(y =='NaN' for y in yield_curve):
		t +=day
		date, maturity, yield_curve, ymask = yc(t.strftime('%Y-%m-%d'),all_yields)
	dates.append(t)
	date_strs.append(date)
	maturities.append(maturity)
	yield_curves.append(yield_curve)
	masks.append(ymask)
	t+=day
	N+=1


k=0
def run(*args):
    global dates, date_strs,maturities, yield_curves,masks,k
    # print k
    maturity = maturities[k]
    yield_curve = yield_curves[k]
    ymask = masks[k]
    line1.set_data(maturity[ymask], yield_curve[ymask])
    date_text.set_text(date_strs[k])
    k +=1
    return line1, date_text


ani = animation.FuncAnimation(fig, run, N-1, blit=False,repeat=False,interval=1)
ani.save('US_Treasury_Yield_Curve_Animation.mp4',writer=writer)