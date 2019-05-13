import requests,dateutil, pylab, datetime, os
import numpy as np
import pandas as pd
import warnings
import statsmodels.api as sm
import numbers
tsa = sm.tsa

# API key attribute needs to be set

# Try to find file in OSX home directory
try:
    items = os.getcwd().split('/')[:3]
    items.append('fred_api_key.txt')
    path = '/'.join(items)
    with open(path,'r') as api_key_file:
        api_key = api_key_file.readline()

except:
    api_key=None

def load_api_key(path):
    try:
        # Try to load file from currect working directory
        with open(path,'r') as api_key_file:
            return api_key_file.readline()
    except:

        try:
            # Try to find file in OSX home directory
            items = os.getcwd().split('/')[:3]
            items.append(path)
            path = '/'.join(items)
            with open(path,'r') as api_key_file:
                return api_key_file.readline()

        except:
            path = os.path.join(os.getcwd(),path)
            with open(path,'r') as api_key_file:
                return api_key_file.readline()


######################################################################################################
# The series class and methods

class series:

    '''Defines a class for downloading, storing, and manipulating data from FRED.'''

    def __init__(self,series_id=None):

        '''Initializes an instance of the series class.

        Args:
            series_id (string): unique FRED series ID. If series_id equals None, an empty series 
                                object is created.

        Returns:
            None

        Attributes:
            data:                       (Pandas Series) data values with dates as index.
            date_range:                 (string) specifies the dates of the first and last observations.
            frequency:                  (string) data frequency. 'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Semiannual', or 'Annual'.
            frequency_short:            (string) data frequency. Abbreviated. 'D', 'W', 'M', 'Q', 'SA, or 'A'.
            last_updated:               (string) date series was last updated.
            notes:                      (string) details about series. Not available for all series.
            release:                    (string) statistical release containing data.
            seasonal_adjustment:        (string) specifies whether the data has been seasonally adjusted.
            seasonal_adjustment_short:  (string) specifies whether the data has been seasonally adjusted. Abbreviated.
            series_id:                  (string) unique FRED series ID code.
            source:                     (string) original source of the data.
            t:                          (int) number corresponding to frequency: 365 for daily, 52 for weekly, 12 for monthly, 4 for quarterly, and 1 for annual.
            title:                      (string) title of the data series.
            units:                      (string) units of the data series.
            units_short:                (string) units of the data series. Abbreviated.
        '''

        if api_key==None:
            raise ValueError('fredpy.api_key value not assigned. You need to provide your key for the FRED API.')

        if type(series_id) == str:

            request_url = 'https://api.stlouisfed.org/fred/series?series_id='+series_id+'&api_key='+api_key+'&file_type=json'
            r = requests.get(request_url)
            results = r.json()

            self.series_id = series_id
            self.title = results['seriess'][0]['title']
            self.frequency = results['seriess'][0]['frequency']
            self.frequency_short = results['seriess'][0]['frequency_short']
            self.units = results['seriess'][0]['units']
            self.units_short = results['seriess'][0]['units_short']
            self.seasonal_adjustment = results['seriess'][0]['seasonal_adjustment']
            self.seasonal_adjustment_short = results['seriess'][0]['seasonal_adjustment_short']
            self.last_updated = results['seriess'][0]['last_updated']
            try:
                self.notes = results['seriess'][0]['notes']
            except:
                self.notes = ''

            obs_per_year = {'D':365,'W':52,'M':12,'Q':4,'SA':2,'A':1}
            try:
                self.t = obs_per_year[self.frequency_short]
            except:
                self.t = np.nan


            request_url = 'https://api.stlouisfed.org/fred/series/observations?series_id='+series_id+'&api_key='+api_key+'&file_type=json'
            r = requests.get(request_url)
            results = r.json()

            count = results['count']

            data = np.zeros(count)
            dates = [None]*count
            for i in range(count):
                try:
                    data[i] = results['observations'][i]['value']
                except:
                    data[i] = np.nan
                dates[i] = results['observations'][i]['date']

            if np.isnan(data[0]):
                index =0
                for i,value in enumerate(data):
                    if np.isnan(value):
                        index+=1
                    else:
                        break
                data = data[index:]
                dates = dates[index:]
                
            self.data = pd.Series(data,pd.to_datetime(dates))
            self.date_range = 'Range: '+str(self.data.index[0])[:10]+' to '+str(self.data.index[-1])[:10]


            request_url =  'https://api.stlouisfed.org/fred/series/release?series_id='+series_id+'&api_key='+api_key+'&file_type=json'
            r = requests.get(request_url)
            results = r.json()
            self.release = results['releases'][0]['name']
            release_id = results['releases'][0]['id']


            request_url =  'https://api.stlouisfed.org/fred/release/sources?release_id='+str(release_id)+'&api_key='+api_key+'&file_type=json'
            r = requests.get(request_url)
            results = r.json()
            self.source = results['sources'][0]['name']

        else:

            self.date_range = ''
            self.data = pd.Series([],pd.to_datetime([]))
            self.frequency = ''
            self.frequency_short = ''
            self.last_updated = ''
            self.notes = ''
            self.release = ''
            self.seasonal_adjustment = ''
            self.seasonal_adjustment_short = ''
            self.series_id = ''
            self.source = ''
            self.t = 0
            self.title = ''
            self.units = ''
            self.units_short = ''

    
    def apc(self,log=False,method='backward'):

        '''Computes the percentage change in the data over one year.

        Args:
            log (bool):         If True, computes the percentage change as 100⋅log[x(t)/x(t-k)], where k is
                                    the number of observations per year.
                                If False (default), compute the percentage change as 100⋅[x(t)/x(k−1)−1].
            method (string):    If ‘backward’ (default), compute percentage change from the previous period. 
                                If ‘forward’, compute percentage change from current to subsequent period.

        Returns:
            fredpy series
        '''

        new_series = self.copy()
        
        T = len(self.data)
        t = self.t

        if log==True:
            if method=='backward':
                new_series.data = 100*np.log(self.data/self.data.shift(t)).dropna()
            else:
                new_series.data = 100*np.log(self.data.shift(-t)/self.data).dropna()
        

        else:
            if method=='backward':
                new_series.data = 100*(self.data/self.data.shift(t)-1).dropna()
            else:
                new_series.data = 100*(self.data.shift(-t)/self.data-1).dropna()


        new_series.units = 'Percent'
        new_series.units_short = '%'
        new_series.title = 'Annual Percentage Change in '+self.title
        new_series.date_range = 'Range: '+str(new_series.data.index[0])[:10]+' to '+str(new_series.data.index[-1])[:10]

        return new_series

    
    def as_frequency(self,freq=None,method='mean'):

        '''Convert a fredpy series to a lower frequency.

        Args:
            freq (string):      Abbreviation of desired frequency: 'D','W','M','Q','A'
            method (string):    How to resample the data: 'first', 'last', 'mean' (default), 'median',
                                    'min', 'max', 'sum'
        Returns:
            fredpy series
        '''

        new_series = self.copy()

        obs_per_year = {'D':365,'W':52,'M':12,'Q':4,'A':1}
        map_of_freqency_abbreviations = {'D':'Daily','W':'Weekly','M':'Monthly','Q':'Quarterly','A':'Annual'}


        try:
            new_series.t = obs_per_year[freq]
            new_series.frequency_short=freq
            new_series.frequency=map_of_freqency_abbreviations[freq]

        except:
            raise ValueError("freq must be 'D', 'W', 'M', 'Q', or 'A'")

        if self.t<new_series.t:
            warnings.warn('Warning: You are converting series to a higher frequency and this method may not behave as you expect.')

        map_to_pandas_frequencies = {'D':'D','W':'W','M':'MS','Q':'QS','A':'AS'}

        if method == 'first':

            new_series.data = self.data.resample(map_to_pandas_frequencies[freq]).first()

        elif method == 'last':

            new_series.data = self.data.resample(map_to_pandas_frequencies[freq]).last()

        elif method == 'mean':

            new_series.data = self.data.resample(map_to_pandas_frequencies[freq]).mean()

        elif method == 'median':

            new_series.data = self.data.resample(map_to_pandas_frequencies[freq]).median()

        elif method == 'min':

            new_series.data = self.data.resample(map_to_pandas_frequencies[freq]).min()

        elif method == 'max':

            new_series.data = self.data.resample(map_to_pandas_frequencies[freq]).max()

        elif method == 'sum':

            new_series.data = self.data.resample(map_to_pandas_frequencies[freq]).sum()

        new_series.date_range = 'Range: '+str(new_series.data.index[0])[:10]+' to '+str(new_series.data.index[-1])[:10]

        return new_series

    
    def bp_filter(self,low=6,high=32,K=12):

        '''Computes the bandpass (Baxter-King) filter of the data. Returns two fredpy.series
        instances containing the cyclical and trend components of the data:

            new_series_cycle,new_series_trend

        .. Note: 
            In computing the bandpass filter, K observations are lost from each end of the
            original series to the data are 2K elements shorter than in the original series.

        Args:
            low (int):  Minimum period for oscillations. Select 24 for monthly data, 6 for quarterly 
                        data (default), and 3 for annual data.
            high (int): Maximum period for oscillations.  Select 84 for monthly data, 32 for quarterly 
                        data (default), and 8 for annual data.
            K (int):    Lead-lag length of the filter. Select, 84 for monthly data, 12 for for quarterly
                        data (default), and 1.5 for annual data.

        Returns:
            two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        if low==6 and high==32 and K==12 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        elif low==3 and high==8 and K==1.5 and self.t !=1:
            print('Warning: data frequency is not annual!')
            
        cycle = tsa.filters.bkfilter(self.data,low=low,high=high,K=K)
        actual = self.data.iloc[K:-K]
        trend = actual - cycle
        
        new_series_cycle.data = cycle
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.title = self.title+' - deviation relative to trend (bandpass filtered)'
        new_series_cycle.date_range = 'Range: '+str(new_series_cycle.data.index[0])[:10]+' to '+str(new_series_cycle.data.index[-1])[:10]

        new_series_trend.data = trend
        new_series_trend.title = self.title+' - trend (bandpass filtered)'
        new_series_trend.date_range = 'Range: '+str(new_series_trend.data.index[0])[:10]+' to '+str(new_series_trend.data.index[-1])[:10]

        return new_series_cycle,new_series_trend


    def cf_filter(self,low=6,high=32):

        '''Computes the Christiano-Fitzgerald (CF) filter of the data. Returns two fredpy.series
        instances containing the cyclical and trend components of the data:

            new_series_cycle,new_series_trend

        Returns:
            two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        if low==6 and high==32 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        elif low==1.5 and high==8 and self.t !=4:
            print('Warning: data frequency is not quarterly!')

        actual = self.data
        cycle, trend = tsa.filters.cffilter(self.data,low=low, high=high, drift=False)

        new_series_cycle.data = cycle
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.title = self.title+' - deviation relative to trend (CF filtered)'

        new_series_trend.data = trend
        new_series_trend.title = self.title+' - trend (CF filtered)'

        return new_series_cycle,new_series_trend

    
    def copy(self):

        '''Returns a copy of a series object.

        Args:

        Returs:
            fredpy series
        '''

        new_series = series()


        new_series.data = self.data
        new_series.date_range = self.date_range
        new_series.frequency = self.frequency
        new_series.frequency_short = self.frequency_short
        new_series.last_updated = self.last_updated
        new_series.notes = self.notes
        new_series.release = self.release
        new_series.seasonal_adjustment = self.seasonal_adjustment
        new_series.seasonal_adjustment_short = self.seasonal_adjustment_short
        new_series.series_id = self.series_id
        new_series.source = self.source
        new_series.t = self.t
        new_series.title = self.title
        new_series.units = self.units
        new_series.units_short = self.units_short

        return new_series


    def diff_filter(self):

        '''Computes the first difference filter of original series. Returns two fredpy.series
        instances containing the cyclical and trend components of the data:

            new_series_cycle,new_series_trend

        Note:
            In computing the first difference filter, the first observation from the original series is
            lost so data are 1 element shorter than in the original series.

        Args:

        Returns:
            two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        new_series_cycle.data = self.data.diff().dropna() - self.data.diff().dropna().mean()
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.date_range = 'Range: '+str(new_series_cycle.data.index[0])[:10]+' to '+str(new_series_cycle.data.index[-1])[:10]

        new_series_trend.data = self.data.shift(1).dropna()
        new_series_trend.title = self.title+' - trend (first difference filtered)'
        new_series_trend.date_range = 'Range: '+str(new_series_trend.data.index[0])[:10]+' to '+str(new_series_trend.data.index[-1])[:10]

        return new_series_cycle,new_series_trend

    
    def divide(self,object2):

        '''Divides the data from the current fredpy series by the data from object2.

        Args:
            object2 (int, float, numpy ndarray, or similar or fredpy series)

        Note:
            You are responsibile for making sure that dividing the series makes sense.

        Returns:
            fredpy series
        '''

        return divide(self,object2)

    def drop_nan(self):

        '''Removes missing (NaN) values.

        Args:

        Returns:
            fredpy series
        '''

        new_series = self.copy()
        
        new_series.data = new_series.data.dropna()
        new_series.date_range = 'Range: '+str(new_series.data.index[0])[:10]+' to '+str(new_series.data.index[-1])[:10]

        return new_series


    def hp_filter(self,lamb=1600):

        '''Computes the Hodrick-Prescott (HP) filter of the data. Returns two fredpy.series
        instances containing the cyclical and trend components of the data:

            new_series_cycle,new_series_trend

        Args:
            lamb (int): The Hodrick-Prescott smoothing parameter. Select 129600 for monthly data,
                        1600 for quarterly data (default), and 6.25 for annual data.
            
        Returns:
            two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        if lamb==1600 and self.t !=4:
            print('Warning: data frequency is not quarterly!')
        elif lamb==129600 and self.t !=12:
            print('Warning: data frequency is not monthly!')
        elif lamb==6.25 and self.t !=1:
            print('Warning: data frequency is not annual!')
            
        cycle, trend = tsa.filters.hpfilter(self.data,lamb=lamb)

        new_series_cycle.data = cycle
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.title = self.title+' - deviation relative to trend (HP filtered)'

        new_series_trend.title = self.title+' - trend (HP filtered)'
        new_series_trend.data = trend

        return new_series_cycle,new_series_trend

    
    def linear_filter(self):

        '''Computes a simple linear filter of the data using OLS. Returns two fredpy.series
        instances containing the cyclical and trend components of the data:

            new_series_cycle,new_series_trend

        Args:

        Returns:
            two fredpy.series instances
        '''

        new_series_cycle = self.copy()
        new_series_trend = self.copy()

        y = self.data
        time = np.arange(len(self.data))
        x = np.column_stack([time])
        x = sm.add_constant(x)
        model = sm.OLS(y,x)
        result= model.fit()
        pred  = result.predict(x)
        
        cycle= y-pred
        trend= pd.Series(pred,index=self.data.index)

        new_series_cycle.data = cycle
        new_series_cycle.units = 'Deviation relative to trend'
        new_series_cycle.units_short = 'Dev. rel. to trend'
        new_series_cycle.title = self.title+' - deviation relative to trend (linearly filtered via OLS)'

        new_series_trend.title = self.title+' - trend (linearly filtered via OLS)'
        new_series_trend.data = trend

        return new_series_cycle,new_series_trend

    
    def log(self):
        
        '''Computes the natural log of the data

        Args:

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        new_series.data = np.log(new_series.data)
        new_series.units = 'Log '+new_series.units
        new_series.units_short = 'Log '+new_series.units_short
        new_series.title = 'Log '+new_series.title

        return new_series

    def ma(self,length,center=False):

        '''Computes a moving average with window equal to length. If center is True, then the 
        two-sided moving average is computed. Otherwise, the moving average will be one-sided.

        Args:
            length (int): window length of the one-sided moving average.
            center (bool): False (default) - one-sided MA. True - two-sided MA.

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        new_series.data = new_series.data.rolling(window=length,center=center).mean().dropna()
        new_series.date_range = 'Range: '+str(new_series.data.index[0])[:10]+' to '+str(new_series.data.index[-1])[:10]
        if center:
            new_series.title = self.title+' (: one-sided moving average)'
        else:
            new_series.title = self.title+' (: two-sided moving average)'

        return new_series

    
    def minus(self,object2):

        '''Subtracts the data from object2 from the data from the current fredpy series.

        Args:
            object2 (int, float, numpy ndarray, or similar or fredpy series)

        Note:
            You are responsibile for making sure that adding the series makes sense.

        Returns:
            fredpy series
        '''

        return minus(self,object2)


    def pc(self,log=False,method='backward',annualized=False):

        '''Computes the percentage change in the data from the preceding period.

        Args:
            log (bool):        If True, computes the percentage change as 100⋅log[x(t)/x(t-1)]. 
                               If False (default), compute the percentage change as 100⋅[x(t)/x(t−1)−1].
            method (string):   If ‘backward’ (default), compute percentage change from the previous period. 
                               If ‘forward’, compute percentage change from current to subsequent period.
            annualized (bool): If True (default), percentage change is annualized by multipying the simple 
                               percentage change by the number of data observations per year. E.g., if the
                               data are monthly, then the annualized percentage change is 12⋅100⋅log[x(t)/x(t−1)].

        Returns:
            fredpy series
        '''

        new_series = self.copy()
        
        T = len(self.data)
        t = self.t

        if log==True:
            if method=='backward':
                new_series.data = 100*np.log(self.data/self.data.shift(1)).dropna()
            else:
                new_series.data = 100*np.log(self.data.shift(-1)/self.data).dropna()
        

        else:
            if method=='backward':
                new_series.data = 100*(self.data/self.data.shift(1)-1).dropna()
            else:
                new_series.data = 100*(self.data.shift(-1)/self.data-1).dropna()

        if annualized:
            new_series.data = t*new_series.data

        new_series.units = 'Percent'
        new_series.units_short = '%'
        new_series.title = 'Percentage Change in '+self.title
        new_series.date_range = 'Range: '+str(new_series.data.index[0])[:10]+' to '+str(new_series.data.index[-1])[:10]

        return new_series

    
    def per_capita(self,civ_pop = True):

        '''Transforms the data into per capita terms (US) by dividing by a measure of the total population:

        Args:
            civ_pop (string): If civ_pop == True, use Civilian noninstitutional population defined as 
                                persons 16 years of age and older (Default). Else, use the total US 
                                population.

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        if civ_pop ==True:
            population= series('CNP16OV').as_frequency(new_series.frequency_short)
        else:
            population= series('POP').as_frequency(new_series.frequency_short)
    
        new_series,population = window_equalize([new_series,population])

        new_series.data = new_series.data/population.data

        new_series.title = new_series.title+' Per Capita'
        new_series.units = new_series.units+' Per Thousand People'
        new_series.units_short = new_series.units_short+' Per Thousand People'
        new_series.date_range = 'Range: '+str(new_series.data.index[0])[:10]+' to '+str(new_series.data.index[-1])[:10]

        return new_series

    
    def plot(self,**kwargs):

        self.data.plot(**kwargs)


    def plus(self,object2):

        '''Adds the data from the current fredpy series to the data from object2.

        Args:
            object2 (int, float, numpy ndarray, or similar or fredpy series)

        Note:
            You are responsibile for making sure that adding the series makes sense.

        Returns:
            fredpy series
        '''

        return plus(self,object2)

    
    def recent(self,N):

        '''Restrict the data to the most recent N observations.

        Args:
            N (int): Number of periods to include in the data window.

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        new_series.data  =new_series.data.iloc[-N:]
        new_series.date_range = 'Range: '+str(new_series.data.index[0])[:10]+' to '+str(new_series.data.index[-1])[:10]

        return new_series

    
    def recessions(self,color='0.5',alpha = 0.5):
        
        '''Creates recession bars for plots. Should be used after a plot has been made but
            before either (1) a new plot is created or (2) a show command is issued.

        Args:
            color (string): Color of the bars. Default: '0.5'
            alpha (float):  Transparency of the recession bars. Must be between 0 and 1
                            Default: 0.5

        Returns:
        '''

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

        date_num    = pylab.date2num([dateutil.parser.parse(s) for s in self.data.index.strftime('%Y-%m-%d')])
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
                peaks2.insert(0,self.data.index[0])
                troughs2 = troughs[min0:max0]
                troughs2.append(self.data.index[-1])
                troughs2.insert(0,troughs[min0-1])

                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])

            elif peaks_num[max0]<datesmax and troughs_num[min0-1]<datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.append(peaks[max0])
                troughs2 = troughs[min0:max0]
                troughs2.append(self.data.index[-1])

                peaks2num  = pylab.date2num([dateutil.parser.parse(s) for s in peaks2])
                troughs2num = pylab.date2num([dateutil.parser.parse(s) for s in troughs2])

            elif peaks_num[max0]>datesmax and troughs_num[min0]>datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.insert(0,self.data.index[0])

                troughs2 = troughs[min0:max0]
                troughs2.insert(0,troughs[min0-1])

                peaks2num  =  peaks2
                troughs2num = troughs2


            else:
                peaks2 = peaks[min0:max0+1]
                troughs2 = troughs[min0:max0+1]
                peaks2num  = peaks_num[min0:max0+1]
                troughs2num= troughs_num[min0:max0+1]


        else:
            if peaks_num[max0]>datesmax and troughs_num[min0]>datesmin:
                peaks2 = peaks[min0:max0]
                peaks2.insert(0,self.data.index[0])
                troughs2 = troughs[min0:max0]
                troughs2.insert(0,troughs[min0+1])

                peaks2num  =  peaks2
                troughs2num = troughs2

            else:
                peaks2 = peaks[min0:max0+1]
                troughs2 = troughs[min0:max0+1]
                peaks2num  = peaks_num[min0:max0+1]
                troughs2num= troughs_num[min0:max0+1]
                
        peaks2num  =  pd.to_datetime(peaks2)
        troughs2num = pd.to_datetime(troughs2)
        
        for k in range(len(peaks2)):
            pylab.axvspan(peaks2num[k], troughs2num[k], edgecolor= color, facecolor=color, alpha=alpha)

    
    def times(self,object2):

        '''Multiplies the data from the current fredpy series with the data from object2.

        Args:
            object2 (int, float, numpy ndarray, or similar or fredpy series)

        Note:
            You are responsibile for making sure that adding the series makes sense.

        Returns:
            fredpy series
        '''

        return times(self,object2)


    def window(self,start_end):

        '''Restricts the data to a specified date window.

        Args:

            start_end (list):   is an ordered pair: start_end = [start, end]

                                    start is the date of the minimum date
                                    end is the date of the maximum date
        
                                both are strings in either 'yyyy-mm-dd' or 'mm-dd-yyyy' format

        Returns:
            fredpy series
        '''

        new_series = self.copy()

        new_series.data = new_series.data.loc[start_end[0]:start_end[1]]

        if len(new_series.data)>0:
            new_series.date_range = 'Range: '+str(new_series.data.index[0])[:10]+' to '+str(new_series.data.index[-1])[:10]
        else:
            new_series.date_range = 'Range: Null'


        return new_series

######################################################################################################
# Additional functions

def divide(object1,object2):

    '''Divides the data from the object1 by the data from object2.

    Args:
        object1 (int, float, numpy ndarray, or similar or fredpy series)
        object2 (int, float, numpy ndarray, or similar or fredpy series)

    Note:
        You are responsibile for making sure that adding the series makes sense.

    Returns:
        fredpy series
    '''

    if not isinstance(object1, series) and not isinstance(object2, series):

        return object1/object2

    elif not isinstance(object1, series) and isinstance(object2, series):

        new_series = object2.copy()
        new_series.data = object1/new_series.data

        return new_series

    elif not isinstance(object2, series) and isinstance(object1, series):

        new_series = object1.copy()
        new_series.data = new_series.data/object2

        return new_series

    else:

        if not object1.data.index.equals(object2.data.index):

            raise ValueError('object1 and object2 do not have the same observation dates')

        else:

            new_series = series()

            new_series.title = object1.title +' divided by '+object2.title
            if object1.source == object2.source:
                new_series.source = object1.source
            else:
                new_series.source = object1.source +' and '+object2.source
            new_series.frequency = object1.frequency
            new_series.frequency_short = object1.frequency_short
            new_series.units = object1.units +' / '+object2.units
            new_series.units_short = object1.units_short +' / '+object2.units_short
            new_series.t = object1.t
            new_series.date_range = object1.date_range

            if object1.seasonal_adjustment == object2.seasonal_adjustment:
                new_series.seasonal_adjustment = object1.seasonal_adjustment
                new_series.seasonal_adjustment_short = object1.seasonal_adjustment_short
            else:
                new_series.seasonal_adjustment = object1.seasonal_adjustment +' and '+object2.seasonal_adjustment
                new_series.seasonal_adjustment_short = object1.seasonal_adjustment_short +' and '+object2.seasonal_adjustment_short

            if object1.last_updated == object2.last_updated:
                new_series.last_updated = object1.last_updated
            else:
                new_series.last_updated = object1.last_updated +' and '+object2.last_updated

            if object1.release == object2.release:
                new_series.release = object1.release
            else:
                new_series.release = object1.release +' and '+object2.release
                
            new_series.series_id = object1.series_id +' and '+object2.series_id
            new_series.data  = object1.data/object2.data

            return new_series


def minus(object1,object2):

    '''Subtracts the data from object2 from the data from object1.

    Args:
        object1 (int, float, numpy ndarray, or similar or fredpy series)
        object2 (int, float, numpy ndarray, or similar or fredpy series)

    Note:
        You are responsibile for making sure that adding the series makes sense.

    Returns:
        fredpy series
    '''

    if not isinstance(object1, series) and not isinstance(object2, series):

        return object1-object2

    elif not isinstance(object1, series) and isinstance(object2, series):

        new_series = object2.copy()
        new_series.data = object1-new_series.data

        return new_series

    elif not isinstance(object2, series) and isinstance(object1, series):

        new_series = object1.copy()
        new_series.data = new_series.data-object2

        return new_series

    else:

        if not object1.data.index.equals(object2.data.index):

            raise ValueError('object1 and object2 do not have the same observation dates')

        else:

            new_series = series()

            new_series.title = object1.title +' minus '+object2.title
            if object1.source == object2.source:
                new_series.source = object1.source
            else:
                new_series.source = object1.source +' and '+object2.source
            new_series.frequency = object1.frequency
            new_series.frequency_short = object1.frequency_short
            new_series.units = object1.units +' - '+object2.units
            new_series.units_short = object1.units_short +' - '+object2.units_short
            new_series.t = object1.t
            new_series.date_range = object1.date_range

            if object1.seasonal_adjustment == object2.seasonal_adjustment:
                new_series.seasonal_adjustment = object1.seasonal_adjustment
                new_series.seasonal_adjustment_short = object1.seasonal_adjustment_short
            else:
                new_series.seasonal_adjustment = object1.seasonal_adjustment +' and '+object2.seasonal_adjustment
                new_series.seasonal_adjustment_short = object1.seasonal_adjustment_short +' and '+object2.seasonal_adjustment_short

            if object1.last_updated == object2.last_updated:
                new_series.last_updated = object1.last_updated
            else:
                new_series.last_updated = object1.last_updated +' and '+object2.last_updated

            if object1.release == object2.release:
                new_series.release = object1.release
            else:
                new_series.release = object1.release +' and '+object2.release
                
            new_series.series_id = object1.series_id +' and '+object2.series_id
            new_series.data  = object1.data-object2.data

            return new_series


def plus(object1,object2):

    '''Adds the data from object1 to the data from object2.

    Args:
        object1 (int, float, numpy ndarray, or similar or fredpy series)
        object2 (int, float, numpy ndarray, or similar or fredpy series)

    Note:
        You are responsibile for making sure that adding the series makes sense.

    Returns:
        fredpy series
    '''

    if not isinstance(object1, series) and not isinstance(object2, series):

        return object1+object2

    elif not isinstance(object1, series) and isinstance(object2, series):

        new_series = object2.copy()
        new_series.data = new_series.data+object1

        return new_series

    elif not isinstance(object2, series) and isinstance(object1, series):

        new_series = object1.copy()
        new_series.data = new_series.data+object2

        return new_series

    else:

        if not object1.data.index.equals(object2.data.index):

            raise ValueError('object1 and object2 do not have the same observation dates')

        else:

            new_series = series()

            new_series.title = object1.title +' plus '+object2.title
            if object1.source == object2.source:
                new_series.source = object1.source
            else:
                new_series.source = object1.source +' and '+object2.source
            new_series.frequency = object1.frequency
            new_series.frequency_short = object1.frequency_short
            new_series.units = object1.units +' + '+object2.units
            new_series.units_short = object1.units_short +' + '+object2.units_short
            new_series.t = object1.t
            new_series.date_range = object1.date_range

            if object1.seasonal_adjustment == object2.seasonal_adjustment:
                new_series.seasonal_adjustment = object1.seasonal_adjustment
                new_series.seasonal_adjustment_short = object1.seasonal_adjustment_short
            else:
                new_series.seasonal_adjustment = object1.seasonal_adjustment +' and '+object2.seasonal_adjustment
                new_series.seasonal_adjustment_short = object1.seasonal_adjustment_short +' and '+object2.seasonal_adjustment_short

            if object1.last_updated == object2.last_updated:
                new_series.last_updated = object1.last_updated
            else:
                new_series.last_updated = object1.last_updated +' and '+object2.last_updated

            if object1.release == object2.release:
                new_series.release = object1.release
            else:
                new_series.release = object1.release +' and '+object2.release
                
            new_series.series_id = object1.series_id +' and '+object2.series_id
            new_series.data  = object1.data+object2.data

            return new_series


def times(object1,object2):

    '''Multiplies the data from object1 with the data from object2.

    Args:
        object1 (int, float, numpy ndarray, or similar or fredpy series)
        object2 (int, float, numpy ndarray, or similar or fredpy series)


    Note:
        You are responsibile for making sure that multipying the series makes sense.

    Returns:
        fredpy series
    '''

    if not isinstance(object1, series) and not isinstance(object2, series):

        return object1*object2

    elif not isinstance(object1, series) and isinstance(object2, series):

        new_series = object2.copy()
        new_series.data = new_series.data*object1

        return new_series

    elif not isinstance(object2, series) and isinstance(object1, series):

        new_series = object1.copy()
        new_series.data = new_series.data*object2

        return new_series

    else:

        if not object1.data.index.equals(object2.data.index):

            raise ValueError('object1 and object2 do not have the same observation dates')

        else:

            new_series = series()

            new_series.title = object1.title +' times '+object2.title
            if object1.source == object2.source:
                new_series.source = object1.source
            else:
                new_series.source = object1.source +' and '+object2.source
            new_series.frequency = object1.frequency
            new_series.frequency_short = object1.frequency_short
            new_series.units = object1.units +' * '+object2.units
            new_series.units_short = object1.units_short +' * '+object2.units_short
            new_series.t = object1.t
            new_series.date_range = object1.date_range

            if object1.seasonal_adjustment == object2.seasonal_adjustment:
                new_series.seasonal_adjustment = object1.seasonal_adjustment
                new_series.seasonal_adjustment_short = object1.seasonal_adjustment_short
            else:
                new_series.seasonal_adjustment = object1.seasonal_adjustment +' and '+object2.seasonal_adjustment
                new_series.seasonal_adjustment_short = object1.seasonal_adjustment_short +' and '+object2.seasonal_adjustment_short

            if object1.last_updated == object2.last_updated:
                new_series.last_updated = object1.last_updated
            else:
                new_series.last_updated = object1.last_updated +' and '+object2.last_updated

            if object1.release == object2.release:
                new_series.release = object1.release
            else:
                new_series.release = object1.release +' and '+object2.release
                
            new_series.series_id = object1.series_id +' and '+object2.series_id
            new_series.data  = object1.data*object2.data

            return new_series


def to_fred_series(data,dates,frequency='',frequency_short='',last_updated='',notes='',release='',seasonal_adjustment='',seasonal_adjustment_short='',series_id='',source='',t=0,title='',units='',units_short=''):
    
    '''Create a FRED object from a set of data obtained from a different source.

    Args:
        data (numpy ndarray):                   Data
        dates (list or numpy ndarray):          Elements must be strings in 'MM-DD-YYYY' format
        frequency (string):                     Observation frequency. Options: '', 'Daily', 'Weekly', 'Monthly', 'Quarterly', or 'Annual'. Default: ''
        frequency_short (string):               Observation frequency abbreviated. Options: '', 'D', 'W', 'M', 'Q', or 'A'. Default: ''
        last_updated (string):                  Date data was last updated. Default = ''
        notes (string):                         Default: ''
        release (string):                       Notes about data. Default: ''
        seasonal_adjustment (string):           Default: ''
        seasonal_adjustment_short (string):     Default: ''
        series_id (string):                     FRED series ID. Default: ''
        source (string):                        Original source of data. Default: ''
        t (int):                                Number of observations per year. Default: 0
        title (string):                         Title of the data. Default: ''
        units (string):                         Default: ''
        units_short (string):                   Default: ''
        '''
    

    f = series()
    f.data = pd.Series(data,pd.to_datetime(dates))

    if frequency in ['Daily','Weekly','Monthly','Quarterly','Annual']:

        if frequency == 'Daily':
            t=365
            frequency_short = 'D'
        elif frequency == 'Weekly':
            t=52
            frequency_short = 'W'
        elif frequency == 'Monthly':
            t=12
            frequency_short = 'M'
        elif frequency == 'Quarterly':
            t=4
            frequency_short = 'Q'
        else:
            t=1
            frequency_short = 'A'

    elif frequency_short in ['D','W','M','Q','A']:

        if frequency_short == 'D':
            t=365
            frequency = 'Daily'
        elif frequency_short == 'W':
            t=52
            frequency = 'Weekly'
        elif frequency_short == 'M':
            t=12
            frequency = 'Monthly'
        elif frequency_short == 'Q':
            t=4
            frequency = 'Quarterly'
        else:
            t=1
            frequency = 'Annual'

    f.frequency = frequency
    f.frequency_short = frequency_short
    f.last_updated = last_updated
    f.notes = notes
    f.release = release
    f.seasonal_adjustment = seasonal_adjustment
    f.seasonal_adjustment_short = seasonal_adjustment_short
    f.series_id = series_id
    f.source = source
    f.title = title
    f.units = units
    f.units_short = units_short
    f.t = t
    f.date_range = 'Range: '+str(f.data.index[0])[:10]+' to '+str(f.data.index[-1])[:10]
    return f

def window_equalize(series_list):

    '''Adjusts the date windows for a collection of fredpy.series objects to the 
    smallest common date window.

    Args:
        series_list (list): A list of fredpy.series objects

    Returns:
        list
    '''

    minimums = []
    maximums = []
    for s in series_list:
        minimums.append(s.data.index[0])
        maximums.append(s.data.index[-1])

    start_end = [np.max(minimums),np.min(maximums)]

    new_list = []
    for s in series_list:

        new_list.append(s.window(start_end))

    return new_list