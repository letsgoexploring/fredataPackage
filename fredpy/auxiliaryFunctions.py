import dateutil, pylab, datetime
import numpy as np

def quickplot(x,year_mult=10,show=True,recess=False,save=False,name='file',width=2):

    '''Create a plot of a FRED data series'''

    fig = pylab.figure()

    years  = pylab.YearLocator(year_mult)
    ax = fig.add_subplot(111)
    ax.plot_date(x.datenumbers,x.data,'b-',lw=width)
    ax.xaxis.set_major_locator(years)
    ax.set_title(x.title)
    ax.set_ylabel(x.units)
    fig.autofmt_xdate()
    if recess != False:
        x.recessions()
    ax.grid(True)
    if show==True:
        pylab.show()
    if save !=False:
        fullname = name+'.png'
        fig.savefig(fullname,bbox_inches='tight')

def window_equalize(series_list):

    '''Takes a list of FRED objects and adjusts the date windows for each to the smallest common window.'''

    minimums = [ k.datenumbers[0].date() for k in fred_list]
    maximums = [ k.datenumbers[-1].date() for k in fred_list]
    win_min =  max(minimums).strftime('%Y-%m-%d')
    win_max =  min(maximums).strftime('%Y-%m-%d')
    windo = [win_min,win_max]
    for x in fred_list:
        x.window(windo)
        
def date_numbers(date_strings):

    '''Converts a list of date strings in yyy-mm-dd format to date numbers.'''
    datenumbers = [dateutil.parser.parse(s) for s in date_strings]
    return datenumbers

def toFredSeries(data,dates,pandasDates=False,title=None,t=None,season=None,freq=None,source=None,units=None,daterange=None, idCode=None,updated=None):
    '''function for creating a FRED object from a set of data.'''
    f = series('UNRATE')
    f.data = data
    if pandasDates==True:
        f.dates = [ str(d.to_datetime())[0:10] for d in  dates]
    else:
        f.dates = dates
    if type(f.dates[0])==str:
        f.datenumbers = [dateutil.parser.parse(s) for s in f.dates]
    f.title = title
    f.t = t
    f.season = season
    f.freq = freq
    f.source = source
    f.units = units
    f.daterange = daterange
    f.idCode = idCode
    f.updated = updated
    return f