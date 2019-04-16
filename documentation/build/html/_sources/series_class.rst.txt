.. fredpy documentation master file, created by
   sphinx-quickstart on Fri Aug 19 15:23:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

``fredpy.series`` class
==================================




.. py:class:: fredpy.series(series_id=None)
	
	Creates an instance of a :py:class:`fredpy.series` instance that stores information about the specified data series from FRED with the unique series ID code given by :py:attr:`series_id`.


	:param str series_id: unique FRED series ID. If :py:attr:`series_id` equals None, an empty :py:class:`fredpy.series` instance is created.

	**Attributes:**
    

		:data: (Pandas Series) --  data values.
		:date_range: (string) -- specifies the dates of the first and last observations.
		:frequency: (string) -- data frequency. 'Daily', 'Weekly', 'Monthly', 'Quarterly', or 'Annual'.
		:frequency_short: (string) -- data frequency. Abbreviated. 'D', 'W', 'M', 'Q', 'SA, or 'A'.
		:last_updated: (string) -- date series was last updated.
		:notes: (string) -- details about series. Not available for all series.
		:release: (string) -- statistical release containing data.
		:seasonal_adjustment: (string) -- specifies whether the data has been seasonally adjusted.
		:seasonal_adjustment_short: (string) --specifies whether the data has been seasonally adjusted. Abbreviated.
		:series_id: (string) -- unique FRED series ID code.
		:source: (string) -- original source of the data.
		:t: (integer) -- number corresponding to frequency: 365 for daily, 52 for weekly, 12 for monthly, 4 for quarterly, and 1 for annual. 
		:title: (string) -- title of the data series.
		:units: (string) -- units of the data series.
		:units_short: (string) units of the data series. Abbreviated.


	**Methods:**


		.. py:function:: apc(log=False,method='backward')

			Computes the percentage change in the data over one year.

			:param bool log: If True, computes the percentage change as :math:`100\cdot\log(x_{t}/x_{t-k})`, where :math:`k` is the number of observations per year. If False, compute the percentage change as :math:`100\cdot\left( x_{t}/x_{t-k} - 1\right)`.
			:param str method: If 'backward', compute percentage change from the previous period. If 'forward', compute percentage change from current to subsequent period.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: as_frequency(freq=None,method='mean')

			Convert a :py:class:`fredpy.series` to a lower frequency.

			:param str freq: Abbreviation of desired frequency: 'D','W','M','Q','A'.
			:param str method: How to resample the data: 'first', 'last', 'mean' (default), 'median', 'min', 'max', 'sum'
		 	:return: :py:class:`fredpy.series`

		.. py:function:: bp_filter(low=6,high=32,K=12)

			Computes the bandpass (Baxter-King) filter of the data. Returns two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*new_series_cycle, new_series_trend*

			:param int low: Minimum period for oscillations. Select 24 for monthly data, 6 for quarterly data (default), and 3 for annual data.
			:param int high: Maximum period for oscillations. Select 84 for monthly data, 32 for quarterly data (default), and 8 for annual data.
			:param int K: Lead-lag length of the filter. Select, 84 for monthly data, 12 for for quarterly data (default), and 1.5 for annual data.
		 	:return: two :py:class:`fredpy.series` instances

			.. Note:: In computing the bandpass filter, K observations are lost from each end of the original series so the attributes *dates*, *datetimes*, and *data* are 2K elements shorter than their counterparts in the original series.

		.. py:function:: cf_filter(low=6,high=32)

			Computes the Christiano-Fitzgerald filter of the data. Returns two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*new_series_cycle, new_series_trend*

			:param int low: Minimum period for oscillations. Select 6 for quarterly data (default) and 1.5 for annual data.
			:param int high: Maximum period for oscillations. Select 32 for quarterly data (default) and 8 for annual data.
		 	:return: two :py:class:`fredpy.series` instances

		.. py:function:: copy()

			Returns a copy of the :py:class:`fredpy.series` instance.

			:Parameters: None
			:return: :py:class:`fredpy.series`

		.. py:function:: diff_filter()

			Computes the first difference filter of original series. Returns two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*new_series_cycle, new_series_trend*

			:Parameters:
		 	:return: two :py:class:`fredpy.series` instances

		 	..

			.. Note:: In computing the first difference filter, the first observation from the original series is lost so the attributes *dates*, *datetimes*, and *data* are 1 element shorter than their counterparts in the original series.

		.. py:function:: divide(object2)

			Divides the data from the current fredpy series by the data from :py:attr:`object2`.

			:param object2: A :py:class:`fredpy.series` instance.
			:type object2: fredpy.series
			:return: :py:class:`fredpy.series`

		.. py:function:: dropna()

			Removes NaN values from fredpy series.

			:return: :py:class:`fredpy.series`

		.. py:function:: hp_filter(lamb=1600)

			Computes the Hodrick-Prescott filter of the data. Returns two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*new_series_cycle, new_series_trend*

			:param int lamb: The Hodrick-Prescott smoothing parameter. Select 129600 for monthly data, 1600 for quarterly data (default), and 6.25 for annual data.
		 	:return: two :py:class:`fredpy.series` instances

		.. py:function:: linear_filter()

			Computes a simple linear filter of the data using OLS. Returns two :py:class:`fredpy.series` instances containing the cyclical and trend components of the data: 

				*new_series_cycle, new_series_trend*

			:Parameters:
		 	:return: two :py:class:`fredpy.series` instances

		.. py:function:: log()

			Computes the natural log of the data.

			:Parameters:
		 	:return: :py:class:`fredpy.series`

		.. py:function:: ma(length,center=False)

			Computes a moving average with window equal to :py:attr:`length`. If :py:attr:`center` is True, then the two-sided moving average is computed. Otherwise, the moving average will be one-sided.

			:param int length: window length of the one-sided moving average.
			:param bool center: False (default): one-sided MA. True: two-sided MA.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: minus(object2)

			Subtracts the data from :py:attr:`object2` from the data from the current fredpy series.

			:param object2: A :py:class:`fredpy.series` instance.
			:type object2: fredpy.series
			:return: :py:class:`fredpy.series`

			..

		.. py:function:: pc(log=False,method='backward',annualized=False)

			Computes the percentage change in the data from the preceding period.

			:param bool log: If True, computes the percentage change as :math:`100\cdot\log(x_{t}/x_{t-1})`. If False, compute the percentage change as :math:`100\cdot\left( x_{t}/x_{t-1} - 1\right)`.
			:param str method: If 'backward', compute percentage change from the previous period. If 'forward', compute percentage change from current to subsequent period.
		 	:param bool annualized: If True, percentage change is annualized by multipying the simple percentage change by the number of data observations per year. E.g., if the data are monthly, then the annualized percentage change is :math:`12\cdot 100\cdot\log(x_{t}/x_{t-1})`.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: per_capita(total_pop=True)

			Transforms the data into per capita terms (US) by dividing by one of two measures of the total population.

			:param str total_pop: If :py:attr:`total_pop` is True, then use the toal population (Default). Else, use civilian noninstitutional population defined as persons 16 years of age and older.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: plus(object2)

			Adds the data from the current fredpy series to the data from :py:attr:`object2`.

			:param object2: A :py:class:``fredpy.series`` instance.
			:type object2: fredpy.series
			:return: :py:class:`fredpy.series`

		.. py:function:: recent(N)

			Restrict the data to the most recent N observations.

			:param int N: Number of periods to include in the data window.
		 	:return: :py:class:`fredpy.series`

		.. py:function:: recessions(color='0.5',alpha = 0.5)

			Creates recession bars for plots. Should be used after a plot has been made but before either (1) a new plot is created or (2) a show command is issued.

			:param str color: Color of the bars. Default: '0.5'.
			:param float alpha: Transparency of the recession bars. Must be between 0 and 1. Default: 0.5.
		 	:return:

		.. py:function:: times(object2)

			Multiplies the data from the current fredpy series with the data from :py:attr:`object2`.

			:param object2: A :py:class:`fredpy.series` instance.
			:type object2: fredpy.series
			:return: :py:class:`fredpy.series`

		.. py:function:: window(win)

			Restricts the data to the most recent N observations.

			:param list win: is an ordered pair: ``win = [win_min, win_max]`` where ``win_min`` is the date of the minimum date desired and ``win_max`` is the date of the maximum date. Date strings must be entered in either YYYY-MM-DD or MM-DD-YYYY format.
		 	:return: :py:class:`fredpy.series`