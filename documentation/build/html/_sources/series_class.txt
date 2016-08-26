.. fredpy documentation master file, created by
   sphinx-quickstart on Fri Aug 19 15:23:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

``fredpy.series`` class
==================================




.. py:class:: fredpy.series(series_id=None)
	
	Creates an instance of a :py:class:`fredpy.series` object that stores information about the specified data series from FRED with the unique series ID code given by :py:attr:`series_id`.


	:param string series_id: unique FRED series ID. If :py:attr:`series_id` equals None, an empy :py:class:`fredpy.series` object is created.

	**Attributes:**
    

		:data: (numpy ndarray) --  data values.
		:daterange: (string) -- specifies the dates of the first and last observations.
		:dates: (list) -- list of date strings in YYYY-MM-DD format.
		:datetimes: (numpy ndarray) -- array containing observation dates formatted as datetime objects.
		:freq: (string) -- data frequency. 'Daily', 'Weekly', 'Monthly', 'Quarterly', or 'Annual'.
		:idCode: (string) -- unique FRED series ID code.
		:season: (string) -- specifies whether the data has been seasonally adjusted.
		:source: (string) -- original source of the data.
		:t: (integer) -- number corresponding to frequency: 365 for daily, 52 for weekly, 12 for monthly, 4 for quarterly, and 1 for annual. 
		:title: (string) -- title of the data series.
		:units: (string) -- units of the data series.
		:updated: (string) -- date series was last updated.

	**Methods:**


		.. py:function:: apc(log=True,method='backward')

			Computes the percentage change in the data over one year.

			:param bool log: If True, computes the percentage change as :math:`100\cdot\log(x_{t}/x_{t-1})`. If False, compute the percentage change as :math:`100\cdot\left( x_{t}/x_{t-1} - 1\right)`.
			:param string method: If 'backward', compute percentage change from the previous period. If 'forward', compute percentage change from current to subsequent period.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: bpfilter(low=6,high=32,K=12)

			Computes the bandpass (Baxter-King) filter of the data. Returns a list of two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*[new_series_cycle, new_series_trend]*

			:param integer low: Minimum period for oscillations. Select 24 for monthly data, 6 for quarterly data (default), and 3 for annual data.
			:param integer high: Maximum period for oscillations. Select 84 for monthly data, 32 for quarterly data (default), and 8 for annual data.
			:param integer K: Lead-lag length of the filter. Select, 84 for monthly data, 12 for for quarterly data (default), and 1.5 for annual data.
		 	:return: :py:class:`list` of two :py:class:`fredpy.series` instances

			.. Note:: In computing the bandpass filter, K observations are lost from each end of the original series so the attributes *dates*, *datetimes*, and *data* are 2K elements shorter than their counterparts in the original series.

		.. py:function:: cffilter(low=6,high=32)

			Computes the Christiano-Fitzgerald filter of the data. Returns a list of two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*[new_series_cycle, new_series_trend]*

			:param integer low: Minimum period for oscillations. Select 6 for quarterly data (default) and 1.5 for annual data.
			:param integer high: Maximum period for oscillations. Select 32 for quarterly data (default) and 8 for annual data.
		 	:return: :py:class:`list` of two :py:class:`fredpy.series` instances

		.. py:function:: copy()

			Returns a copy of the :py:class:`fredpy.series` object.

			:Parameters: None
			:return: :py:class:`fredpy.series`

		.. py:function:: divide(series2)

			Divides the data from the current fredpy series by the data from ``series2``.

			:param series2: A ``fredpy.series`` object.
			:type series2: fredpy.series
			:return: :py:class:`fredpy.series`

		.. py:function:: firstdiff()

			Computes the first difference filter of original series. Returns a list of two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*[new_series_cycle, new_series_trend]*

			:Parameters:
		 	:return: :py:class:`list` of two :py:class:`fredpy.series` instances

		 	..

			.. Note:: In computing the first difference filter, the first observation from the original series is lost so the attributes *dates*, *datetimes*, and *data* are 1 element shorter than their counterparts in the original series.

		.. py:function:: hpfilter(lamb=1600)

			Computes the Hodrick-Prescott filter of the data. Returns a list of two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*[new_series_cycle, new_series_trend]*

			:param integer lamb: The Hodrick-Prescott smoothing parameter. Select 129600 for monthly data, 1600 for quarterly data (default), and 6.25 for annual data.
		 	:return: :py:class:`list` of two :py:class:`fredpy.series` instances

		.. py:function:: lintrend()

			Computes a simple linear filter of the data using OLS. Returns a list of two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*[new_series_cycle, new_series_trend]*

			:Parameters:
		 	:return: :py:class:`list` of two :py:class:`fredpy.series` instances

		.. py:function:: log()

			Computes the natural log of the data.

			:Parameters:
		 	:return: :py:class:`fredpy.series`


		.. py:function:: ma1side(length)

			Computes a one-sided moving average with window equal to :py:attr:`length`.

			:param integer length: :py:attr:`length` of the one-sided moving average.
		 	:return: :py:class:`fredpy.series`


		.. py:function:: ma2side(length)

			Computes a two-sided moving average with window equal to 2 times :py:attr:`length`.

			:param integer length: half of :py:attr:`length` of the two-sided moving average. For example, if :py:attr:`length = 12`, then the moving average will contain 24 the 12 periods before and the 12 periods after each observation.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: minus(series2)

			Subtracts the data from ``series2`` from the data from the current fredpy series.

			:param series2: A ``fredpy.series`` object.
			:type series2: fredpy.series
			:return: :py:class:`fredpy.series`

			..

		.. py:function:: monthtoannual(method='average')

			Converts monthly data to annual data.

			:param string method: If 'average', use the average values over each twelve month interval (default), if 'sum,' use the sum of the values over each twelve month interval, and if 'end' use the values at the end of each twelve month interval.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: monthtoquarter(method='average')

			Converts monthly data to quarterly data.

			:param string method: If 'average', use the average values over each three month interval (default), if 'sum,' use the sum of the values over each three month interval, and if 'end' use the values at the end of each three month interval.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: pc(log=True,method='backward',annualized=False)

			Computes the percentage change in the data from the preceding period.

			:param bool log: If True, computes the percentage change as :math:`100\cdot\log(x_{t}/x_{t-1})`. If False, compute the percentage change as :math:`100\cdot\left( x_{t}/x_{t-1} - 1\right)`.
			:param string method: If 'backward', compute percentage change from the previous period. If 'forward', compute percentage change from current to subsequent period.
		 	:param bool annualized: If True, percentage change is annualized by multipying the simple percentage change by the number of data observations per year. E.g., if the data are monthly, then the annualized percentage change is :math:`4\cdot 100\cdot\log(x_{t}/x_{t-1})`.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: percapita(total_pop=True)

			Transforms the data into per capita terms (US) by dividing by one of two measures of the total population.

			:param string total_pop: If ``total_pop == True``, then use the toal population (Default). Else, use Civilian noninstitutional population defined as persons 16 years of age and older.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: plus(series2)

			Adds the data from the current fredpy series to the data from ``series2``.

			:param series2: A ``fredpy.series`` object.
			:type series2: fredpy.series
			:return: :py:class:`fredpy.series`

		.. py:function:: quartertoannual(method='average')

			Converts quarterly data to annual data.

			:param string method: If 'average', use the average values over each four quarter interval (default), if 'sum,' use the sum of the values over each four quarter interval, and if 'end' use the values at the end of each four quarter interval.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: recent(N)

			Restrict the data to the most recent N observations.

			:param integer N: Number of periods to include in the data window.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: recessions(color='0.5',alpha = 0.5)

			Creates recession bars for plots. Should be used after a plot has been made but before either (1) a new plot is created or (2) a show command is issued.

			:param string color: Color of the bars. Default: '0.5'.
			:param float alpha: Transparency of the recession bars. Must be between 0 and 1. Default: 0.5.
		 	:return:

		.. py:function:: times(series2)

			Multiplies the data from the current fredpy series with the data from ``series2``.

			:param series2: A ``fredpy.series`` object.
			:type series2: fredpy.series
			:return: :py:class:`fredpy.series`

		.. py:function:: window(win)

			Restricts the data to the most recent N observations.

			:param list win: is an ordered pair: ``win = [win_min, win_max]`` where ``win_min`` is the date of the minimum date desired and ``win_max`` is the date of the maximum date. Date strings must be entered in either 'yyyy-mm-dd' or 'mm-dd-yyyy' format.
		 	:return: :py:class:`fredpy.series`

		

		

		

		
		    