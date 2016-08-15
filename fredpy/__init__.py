import urllib, dateutil, pylab, datetime
import numpy as np
import statsmodels.api as sm
tsa = sm.tsa

class series:

    def __init__(self,series_id):
        
        # download fred series from FRED and save information about the series
        series_url = 'http://research.stlouisfed.org/fred2/data/' + series_id + '.txt'

        # Compensate for urllib differences in Python 2 and 3
        try:
            webs = urllib.request.urlopen(series_url)
        except:
            webs = urllib.urlopen(series_url)
        
        raw = [line.decode('utf-8') for line in webs]

        for k, val in enumerate(raw):
            if raw[k][0:5] == 'Title':
                self.title = " ".join(x for x in raw[k].split()[1:])
            elif raw[k][0:3] == 'Sou':
                self.source = " ".join(x for x in raw[k].split()[1:])
            elif raw[k][0:3] == 'Sea':
                self.season = " ".join(x for x in raw[k].split()[1:])
            elif raw[k][0:3] == 'Fre':
                self.freq = " ".join(x for x in raw[k].split()[1:])
                if self.freq[0:5] == 'Daily':
                    self.t=365
                elif self.freq[0:6] == 'Weekly':
                    self.t=52
                elif self.freq[0:7] == 'Monthly':
                    self.t=12
                elif self.freq[0:9] == 'Quarterly':
                    self.t=4
                elif self.freq[0:6] == 'Annual':
                    self.t=1
            elif raw[k][0:3] == 'Uni':
                self.units    = " ".join(x for x in raw[k].split()[1:])
            elif raw[k][0:3] == 'Dat':
                self.daterange = " ".join(x for x in raw[k].split()[1:])
            elif raw[k][0:3] == 'Las':
                self.updated  = " ".join(x for x in raw[k].split()[1:])
            elif raw[k][0:3] == 'DAT':
                raw2 = list(raw[k+1:])
                break

        date=list(range(len(raw2)))
        data=list(range(len(raw2)))

        # Create data for FRED object. Replace missing values with np.nan
        for k,n in enumerate(raw2):
            date[k] = raw2[k].split()[0]
            if raw2[k].split()[1] != '.':
                data[k] = float(raw2[k].split()[1])
            else:
                data[k] = np.nan

        self.idCode    = series_id
        self.data  = np.array(data)
        self.dates = date
        self.datetimes = [dateutil.parser.parse(s) for s in self.dates]

    def pc(self,log=True,method='backward',annualized=False):

        '''Transforms data into percent change'''
        
        T = len(self.data)
        t = self.t
        if log==True:
            pct = 100*np.log(self.data[1:]/self.data[0:-1])
        else:
            pct = 100*(self.data[1:]/self.data[0:-1] - 1)
        if annualized==True:
            pct = np.array([t*x for x in pct])
        if method=='backward':
            dte = self.dates[1:]
        elif method=='forward':
            dte = self.dates[:-1]
        self.data  =pct
        self.dates =dte
        self.datetimes = [dateutil.parser.parse(s) for s in self.dates]
        self.units = 'Percent'
        self.title = 'Percentage Change in '+self.title

    def apc(self,log=True,method='backward'):

        '''Transforms data into percent change from year ago'''
        
        T = len(self.data)
        t = self.t
        if log==True:
            pct = 100 * np.log(self.data[t:]/ self.data[0:-t])
        else:
            pct = 100 * (self.data[t:]/self.data[0:-t] - 1)
        if method=='backward':
            dte = self.dates[t:]
        elif method=='forward':
            dte = self.dates[:T-t]
        self.data  =pct
        self.dates =dte
        self.datetimes = [dateutil.parser.parse(s) for s in self.dates]
        self.units = 'Percent'
        self.title = 'Annual Percentage Change in '+self.title

    def ma2side(self,length):

        '''Transforms data into a two-sided moving average with window equal to 2x length'''
        
        length=int(length)
        z = np.array([])
        for s in range(len(self.data)-2*length):
            z = np.append(z,np.mean(self.data[s+0:s+2*length]))
        
        self.ma2data = z
        self.ma2dates =self.dates[length:-length]
        self.ma2datetimes = [dateutil.parser.parse(s) for s in self.ma2dates]
        self.ma2daterange = self.ma2dates[0]+' to '+self.ma2dates[-1]

    def ma1side(self,length):

        '''Transforms data into a one-sided moving average with window equal to length'''
        
        length=int(length)
        z = np.array([])
        for s in range(len(self.data)-length+1):
            z = np.append(z,np.mean(self.data[s+0:s+length]))

        self.ma1data = z
        self.ma1dates =self.dates[length-1:]
        self.ma1datetimes = [dateutil.parser.parse(s) for s in self.ma1dates]
        self.ma1daterange = self.ma1dates[0]+' to '+self.ma1dates[-1]


    def recent(self,N=10):

        '''lag is the number of obs to include in the window'''

        t = self.t
        self.data  =self.data[-N:]
        self.dates =self.dates[-N:]
        self.datetimes = [dateutil.parser.parse(s) for s in self.dates]
        self.daterange = self.dates[0]+' to '+self.dates[-1]

    def window(self,win):

        '''Constrains the data to a specified date window.

        win is an ordered pair: win = [win_min, win_max]

            win_min is the date of the minimum date
            win_max is the date of the maximum date
        
        both are strings in either 'yyyy-mm-dd' or 'mm-dd-yyyy' format'''

        T = len(self.data)
        win_min = win[0]
        win_max = win[1]
        win_min_num = pylab.date2num(dateutil.parser.parse(win_min))
        win_max_num = pylab.date2num(dateutil.parser.parse(win_max))
        date_num    = pylab.date2num([dateutil.parser.parse(s) for s in self.dates])
        dumpy       = date_num.tolist()
        min0 = 0
        max0 = T
        t = self.t

        if win_min_num > min(date_num):
            for k in range(T):
                if win_min_num <= dumpy[k]:
                    min0 = k
                    break
                                              
        if win_max_num < max(date_num):
            'Or here'
            for k in range(T):
                if win_max_num < dumpy[k]:
                    max0 = k
                    break

        self.data = self.data[min0:max0]
        self.dates = self.dates[min0:max0]
        self.datetimes = [dateutil.parser.parse(s) for s in self.dates]
        if len(self.dates)>0:
            self.daterange = self.dates[0]+' to '+self.dates[-1]
        else:
            self.daterange = 'Null'

    def log(self):
        
        '''Tansforms data into natural log of original series'''

        self.data = np.log(self.data)
        self.units= 'log '+self.units
        self.title = 'Log '+self.title

    def bpfilter(self,low=6,high=32,K=12):

        '''Computes the bandpass (Baxter-King) filter of the series. Adds attributes:

            self.bpcycle : cyclical component of series
            self.bpdates : dates of bp filtered data
            self.bpdatetimes : date numbers of bp filtered data
            
            default is for quarterly data.

        '''

        if low==6 and high==32 and K==12 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        elif low==3 and high==8 and K==1.5 and self.t !=1:
            print('Warning: data frequency is not annual!')
            
        self.bpcycle = tsa.filters.bkfilter(self.data,low=low,high=high,K=K)
        self.bpdates = self.dates[K:-K]
        self.bpdatetimes = [dateutil.parser.parse(s) for s in self.bpdates]
        
    def hpfilter(self,lamb=1600):

        '''Computes the Hodrick-Prescott filter of original series. Adds attributes:

            self.hpcycle : cyclical component of series
            self.hptrend :trend component of series

        '''
        if lamb==1600 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        elif lamb==129600 and self.t !=12:
            print('Warning: data frequency is not monthly!')
        elif lamb==6.25 and self.t !=1:
            print('Warning: data frequency is not annual!')
            
        self.hpcycle, self.hptrend = tsa.filters.hpfilter(self.data,lamb=lamb)

    def cffilter(self,low=6,high=32,drift=True):

        '''Computes the Christiano-Fitzgerald filter of original series. Adds attributes:

            self.cffcycle : cyclical component of series
            self.cfftrend :trend component of series

        '''

        if low==6 and high==32 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        elif low==1.5 and high==8 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        self.cfcycle, self.cftrend = tsa.filters.cffilter(self.data,low=low, high=high, drift=drift)

    def lintrend(self):

        '''Computes the linear trend of original series. Adds attributes:

            self.lincycle : cyclical component of series
            self.lintrend :trend component of series

        '''

        y = self.data
        time = np.arange(len(self.data))
        x = np.column_stack([time])
        x = sm.add_constant(x)
        model = sm.OLS(y,x)
        result= model.fit()
        pred  = result.predict(x)
        self.lincycle= y-pred
        self.lintrend= pred

    def firstdiff(self):

        '''Computes the first difference of original series. Adds attributes:

            self.diffcycle : cyclical component of series
            self.difftrend :trend component of series
            self.diffdates : shorter date sequence
            self.diffdatetimes : shorter date numbers
            self.diffdata  : shorter data series

        '''

        dy    = self.data[1:] - self.data[0:-1]
        gam   = np.mean(dy)
        self.diffcycle = dy - gam
        self.diffdates = self.dates[1:]
        self.diffdatetimes= self.datetimes[1:]
        self.diffdata  = self.data[1:]
        self.difftrend = self.data[0:-1]


    def monthtoquarter(self,method='average'):
        
        '''Converts monthly data to quarterly data using one of three methods:

            average :average of three months (default)
            sum :sum of three months
            end :third month value only

        '''

        if self.t !=12:
            print('Warning: data frequency is not monthly!')
        T = len(self.data)
        temp_data = self.data[0:0]
        temp_dates = self.datetimes[0:0]
        if method == 'average':
            for k in range(1,T-1):
                if (self.datetimes[k].month == 2) or (self.datetimes[k].month == 5) or (self.datetimes[k].month == 8) or (self.datetimes[k].month == 11):
                    temp_data = np.append(temp_data,(self.data[k-1]+self.data[k]+self.data[k+1])/3)
                    temp_dates.append(self.dates[k-1])
        elif method == 'sum':
            for k in range(1,T-1):
                if (self.datetimes[k].month == 2) or (self.datetimes[k].month == 5) or (self.datetimes[k].month == 8) or (self.datetimes[k].month == 11):
                    temp_data = np.append(temp_data,(self.data[k-1]+self.data[k]+self.data[k+1]))
                    temp_dates.append(self.dates[k-1])
        elif method== 'end':
            for k in range(1,T-1):
                if (self.datetimes[k].month == 2) or (self.datetimes[k].month == 5) or (self.datetimes[k].month == 8) or (self.datetimes[k].month == 11):
                    temp_data = np.append(temp_data,self.data[k+1])
                    temp_dates.append(self.dates[k-1])
        self.data = temp_data
        self.dates = temp_dates
        self.datetimes = [dateutil.parser.parse(s) for s in self.dates]
        self.t = 4

    def quartertoannual(self,method='average'):

        '''Converts quaterly data to annual using one of three methods:

            average :average of three months (default)
            sum :sum of three months
            end :third month value only

        '''

        if self.t !=4:
            print('Warning: data frequency is not quarterly!')
        T = len(self.data)
        temp_data = self.data[0:0]
        temp_dates = self.datetimes[0:0]
        if method =='average':
            for k in range(0,T):
                '''Annual data is the average of monthly data'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>3):
                    temp_data = np.append(temp_data,(self.data[k]+self.data[k+1]+self.data[k+2]+self.data[k+3])/4)
                    temp_dates.append(self.dates[k])
        elif method=='sum':
            for k in range(0,T):
                '''Annual data is the sum of monthly data'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>3):
                    temp_data = np.append(temp_data,self.data[k]+self.data[k+1]+self.data[k+2]+self.data[k+3])
                    temp_dates.append(self.dates[k])
        elif method == 'end':
            for k in range(0,T):
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>3):
                    '''Annual data is the end of month value'''
                    temp_data = np.append(temp_data,self.data[k+3])
                    temp_dates.append(self.dates[k])
        self.data = temp_data
        self.dates = temp_dates
        self.datetimes = [dateutil.parser.parse(s) for s in self.dates]
        self.t = 1

    def monthtoannual(self,method='average'):

        '''Converts monthly data to annual data using one of three methods:

            average :average of three months (default)
            sum :sum of three months
            end :third month value only

        '''

        if self.t !=12:
            print('Warning: data frequency is not monthly!')
        T = len(self.data)
        temp_data = self.data[0:0]
        temp_dates = self.datetimes[0:0]
        if method =='average':
            for k in range(0,T):
                '''Annual data is the average of monthly data'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>11):
                    temp_data = np.append(temp_data,(self.data[k]+self.data[k+1]+self.data[k+2]+ self.data[k+3] + self.data[k+4] + self.data[k+5]
                        + self.data[k+6] + self.data[k+7] + self.data[k+8] + self.data[k+9] + self.data[k+10] + self.data[k+11])/12)  
                    temp_dates.append(self.dates[k])
        elif method =='sum':
            for k in range(0,T):
                '''Annual data is the sum of monthly data'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>11):
                    temp_data = np.append(temp_data,(self.data[k]+self.data[k+1]+self.data[k+2]+ self.data[k+3] + self.data[k+4] + self.data[k+5]
                        + self.data[k+6] + self.data[k+7] + self.data[k+8] + self.data[k+9] + self.data[k+10] + self.data[k+11]))
                    temp_dates.append(self.dates[k])
        elif method=='end':
            for k in range(0,T):
                '''Annual data is the end of year value'''
                if (self.datetimes[k].month == 1) and (len(self.datetimes[k:])>11):
                    temp_data = np.append(temp_data,self.data[k+11])
                    temp_dates.append(self.dates[k])
        self.data = temp_data
        self.dates = temp_dates
        self.datetimes = [dateutil.parser.parse(s) for s in self.dates]
        self.t = 1


    def percapita(self,total_pop = True):

        '''Converts data to per capita (US) using one of two methods:

            total_pop == True : Civilian noninstitutional population is defined as persons 16 years of
                                    age and older (default)
            total_pop =! True : Total population US population

        '''

        T = len(self.data)
        temp_data   = self.data[0:0]
        temp_dates  = self.dates[0:0]
        if total_pop ==False:
            populate= series('CNP16OV')
        else:
            populate= series('POP')
        T2 = len(populate.data)

        # Generate quarterly population data.
        if self.t == 4:
            for k in range(1,T2-1):
                if (populate.datetimes[k].month == 2) or (populate.datetimes[k].month == 5) or (populate.datetimes[k].month == 8) or \
                (populate.datetimes[k].month == 11):
                    temp_data = np.append(temp_data,(populate.data[k-1]+populate.data[k]+populate.data[k+1])/3)
                    temp_dates.append(populate.dates[k])

        # Generate annual population data.
        if self.t == 1:
            for k in range(0,T2):
                if (populate.datetimes[k].month == 1) and (len(populate.datetimes[k:])>11):
                    temp_data = np.append(temp_data,(populate.data[k]+populate.data[k+1]+populate.data[k+2]+populate.data[k+3]+populate.data[k+4]+populate.data[k+5] \
                        +populate.data[k+6]+populate.data[k+7]+populate.data[k+8]+populate.data[k+9]+populate.data[k+10]+populate.data[k+11])/12) 
                    temp_dates.append(populate.dates[k])

        if self.t == 12:
            temp_data  = populate.data
            temp_dates = populate.dates
        
        # form the population objects.    
        populate.data     = temp_data
        populate.dates    = temp_dates
        populate.datetimes = [dateutil.parser.parse(s) for s in populate.dates]


        # find the minimum of data window:
        if populate.datetimes[0].date() <= self.datetimes[0].date():
            win_min = self.datetimes[0].strftime('%Y-%m-%d')
        else:
            win_min = populate.datetimes[0].strftime('%Y-%m-%d')

        # find the maximum of data window:
        if populate.datetimes[-1].date() <= self.datetimes[-1].date():
            win_max = populate.datetimes[-1].strftime('%Y-%m-%d')
        else:
            win_max = self.datetimes[-1].strftime('%Y-%m-%d')

        # set data window
        windo = [win_min,win_max]

        populate.window(windo)
        self.window(windo)
        self.data = self.data/populate.data
        self.title = self.title+' Per Capita'
        self.units = self.units+' Per Thousand People'

    def recessions(self):
        
        '''Method creates gray recession bars for plots. Should be used after a plot has been made but
            before either (1) a new plot is created or (2) a show command is issued.'''

        peaks =[
        '1857-06-01',
        '1860-10-01',
        '1865-04-01',
        '1869-06-01',
        '1873-10-01',
        '1882-03-01',
        '1887-03-01',
        '1890-07-01',
        '1893-01-01',
        '1895-12-01',
        '1899-06-01',
        '1902-09-01',
        '1907-05-01',
        '1910-01-01',
        '1913-01-01',
        '1918-08-01',
        '1920-01-01',
        '1923-05-01',
        '1926-10-01',
        '1929-08-01',
        '1937-05-01',
        '1945-02-01',
        '1948-11-01',
        '1953-07-01',
        '1957-08-01',
        '1960-04-01',
        '1969-12-01',
        '1973-11-01',
        '1980-01-01',
        '1981-07-01',
        '1990-07-01',
        '2001-03-01',
        '2007-12-01']

        troughs =[
        '1858-12-01',
        '1861-06-01',
        '1867-12-01',
        '1870-12-01',
        '1879-03-01',
        '1885-05-01',
        '1888-04-01',
        '1891-05-01',
        '1894-06-01',
        '1897-06-01',
        '1900-12-01',
        '1904-08-01',
        '1908-06-01',
        '1912-01-01',
        '1914-12-01',
        '1919-03-01',
        '1921-07-01',
        '1924-07-01',
        '1927-11-01',
        '1933-03-01',
        '1938-06-01',
        '1945-10-01',
        '1949-10-01',
        '1954-05-01',
        '1958-04-01',
        '1961-02-01',
        '1970-11-01',
        '1975-03-01',
        '1980-07-01',
        '1982-11-01',
        '1991-03-01',
        '2001-11-01',
        '2009-06-01']

        if len(troughs) < len(peaks):
            today = datetime.date.today()
            troughs.append(str(today))

        T = len(self.data)
        S = len(peaks)

        date_num    = pylab.date2num([dateutil.parser.parse(s) for s in self.dates])
        peaks_num   = pylab.date2num([dateutil.parser.parse(s) for s in peaks])
        troughs_num = pylab.date2num([dateutil.parser.parse(s) for s in troughs])

        datesmin = min(date_num)
        datesmax = max(date_num)
        peaksmin = min(peaks_num)
        peaksax = max(peaks_num)
        troughsmin=min(troughs_num)
        troughsmax=max(troughs_num)
        
        if datesmin <= peaksmin:
            'Nothing to see here'
            min0 = 0
        else:
            'Or here'
            for k in range(S):
                if datesmin <= peaks_num[k]:
                    min0 = k
                    break
                                              
        if datesmax >= troughsmax:
            max0 = len(troughs)-1
        else:
            'Or here'
            for k in range(S):
                if datesmax < troughs_num[k]:
                    max0 = k
                    break

        if datesmax < troughsmax:
            if peaks_num[max0]<datesmax and troughs_num[min0-1]>datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.append(peaks[max0])
                peaks2.insert(0,self.dates[0])
                troughs2 = troughs[min0:max0]
                troughs2.append(self.dates[-1])
                troughs2.insert(0,troughs[min0-1])
            
                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])

            elif peaks_num[max0]<datesmax and troughs_num[min0-1]<datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.append(peaks[max0])
                troughs2 = troughs[min0:max0]
                troughs2.append(self.dates[-1])
            
                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])

            elif peaks_num[max0]>datesmax and troughs_num[min0]>datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.insert(0,self.dates[0])
                
                troughs2 = troughs[min0:max0]
                troughs2.insert(0,troughs[min0-1])
                
                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])


            else:
                peaks2 = peaks[min0:max0+1]
                troughs2 = troughs[min0:max0+1]
                peaks2num  = peaks_num[min0:max0+1]
                troughs2num= troughs_num[min0:max0+1]


        else:
            if peaks_num[max0]>datesmax and troughs_num[min0]>datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.insert(0,self.dates[0])
                troughs2 = troughs[min0:max0]
                troughs2.insert(0,troughs[min0+1])
        
                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])

            else:
                peaks2 = peaks[min0:max0+1]
                troughs2 = troughs[min0:max0+1]
                peaks2num  = peaks_num[min0:max0+1]
                troughs2num= troughs_num[min0:max0+1]

        self.pks = peaks2
        self.trs = troughs2
        self.recess_bars = pylab.plot()
        self.peaks = peaks
        
        for k in range(len(peaks2)):
            pylab.axvspan(peaks2num[k], troughs2num[k], edgecolor= '0.5', facecolor='0.5', alpha=0.5)

def quickplot(x,year_mult=10,show=True,recess=False,save=False,name='file',width=2):

    '''Create a plot of a FRED data series'''

    fig = pylab.figure()

    years  = pylab.YearLocator(year_mult)
    ax = fig.add_subplot(111)
    ax.plot_date(x.datetimes,x.data,'b-',lw=width)
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

def window_equalize(fred_list):

    '''Takes a list of FRED objects and adjusts the date windows for each to the smallest common window.'''

    minimums = [ k.datetimes[0].date() for k in fred_list]
    maximums = [ k.datetimes[-1].date() for k in fred_list]
    win_min =  max(minimums).strftime('%Y-%m-%d')
    win_max =  min(maximums).strftime('%Y-%m-%d')
    windo = [win_min,win_max]
    for x in fred_list:
        x.window(windo)
        
def date_numbers(date_strings):

    '''Converts a list of date strings in yyy-mm-dd format to date numbers.'''
    datetimes = [dateutil.parser.parse(s) for s in date_strings]
    return datetimes

def toFredSeries(data,dates,pandasDates=False,title=None,t=None,season=None,freq=None,source=None,units=None,daterange=None, idCode=None,updated=None):
    '''function for creating a FRED object from a set of data.'''
    f = series('UNRATE')
    f.data = data
    if pandasDates==True:
        f.dates = [ str(d.to_datetime())[0:10] for d in  dates]
    else:
        f.dates = dates
    if type(f.dates[0])==str:
        f.datetimes = [dateutil.parser.parse(s) for s in f.dates]
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