
Additional ``fredpy`` Functions
==================================




.. py:function:: fredpy.date_times(date_strings)

	Converts a list of date strings in yyyy-mm-dd format to datetime.

	:param list date_strings: a list of date strings formated as: 'yyyy-mm-dd'.
 	:return: :py:class:`numpy.ndarray`

.. py:function:: fredpy.divide(series1,series2)

            Divides the data from :py:data:`series1` by the data from :py:data:`series2`.

            :param series1: A :py:class:`fredpy.series` object.
            :type series1: fredpy.series
            :param series2: A :py:class:`fredpy.series` object.
            :type series2: fredpy.series
            :return: :py:class:`fredpy.series`

.. py:function:: fredpy.plus(series1,series2)

            Adds the data from :py:data:`series1` to the data from :py:data:`series2`.

            :param series1: A :py:class:`fredpy.series` object.
            :type series1: fredpy.series
            :param series2: A :py:class:`fredpy.series` object.
            :type series2: fredpy.series
            :return: :py:class:`fredpy.series`

.. py:function:: fredpy.quickplot(fred_series,year_mult=10,show=True,recess=False,style='default',save=False,filename='file',linewidth=2,alpha = 0.7)

    Create a plot of a FRED data series.

    :param fred_series: A :py:class:`fredpy.series` object.
    :type fred_series: fredpy.series
    :param int year_mult: Interval between year ticks on the x-axis. Default: 10.
    :param bool show: Show the plot? Default: True.
    :param bool recess: Show recession bars in plot? Default: False.
    :param bool style: Matplotlib style. Default: 'default'.
    :param bool save: Save the image to file? Default: False.
    :param string filename: Name of file to which image is saved *without an extension*. Default: ``'file'``.
    :param float linewidth: Width of plotted line. Default: 2.
    :param float alpha: Transparency of the recession bars. Must be between 0 and 1. Default: 0.7.
    :returns:

.. py:function:: fredpy.minus(series1,series2)

            Subtracts the data from :py:data:`series2` from the data from :py:data:`series1`.

            :param series1: A :py:class:`fredpy.series` object.
            :type series1: fredpy.series
            :param series2: A :py:class:`fredpy.series` object.
            :type series2: fredpy.series
            :return: :py:class:`fredpy.series`

.. py:function:: fredpy.times(series1,series2)

            Multiplies the data from :py:data:`series1` with the data from :py:data:`series2`.

            :param series1: A :py:class:`fredpy.series` object.
            :type series1: fredpy.series
            :param series2: A :py:class:`fredpy.series` object.
            :type series2: fredpy.series
            :return: :py:class:`fredpy.series`

.. py:function:: fredpy.toFredSeries(data,dates,frequency='',frequency_short='',last_updated='',notes='',release='',seasonal_adjustment='',seasonal_adjustment_short='',series_id='',source='',t=0,title='',units='',units_short='')

            Create a :py:class:`fredpy.series` from time series data not obtained from FRED.

            :param data: Data values.
            :type data: numpy.ndarray, Pandas.Series, or list
            :param dates: Array or list of dates. Elements formatted as either string (YYYY-MM-DD or MM-DD-YYYY) or :py:class:`pandas.tslib.Timestamp`.
            :type dates: list or numpy.ndarry
            :param str frequency: Observation frequency. Options: '', 'Daily', 'Weekly', 'Monthly', 'Quarterly', or 'Annual'. Default: empty string.
            :param str frequency_short: Observation frequency abbreviated. Options: '', 'D', 'W', 'M', 'Q', or 'A'. Default: empty string.
            :param str last_updated: Date data was last updated. Default: empty string.
            :param str notes: Default: empty string.
            :param str release: Notes about data. Default: empty string.
            :param str seasonal_adjustment: Default: empty string.
            :param str seasonal_adjustment_short: Default: empty string.
            :param str series_id: FRED series ID. Default: empty string.
            :param str source: Source of the data. Default: empty string.
            :param int t: Number of observations per year. Default: 0
            :param str title: Title of the data. Default: empty string.
            :param str units: Units of the data. Default: empty string.
            :param str units_short: Units of the data. Abbreviated. Default: empty string.
            :return: :py:class:`fredpy.series`

.. py:function:: fredpy.window_equalize(series_list)

	Adjusts the date windows for a collection of fredpy.series objects to the smallest common window.

	:param list series_list: A list of :py:class:`fredpy.series` objects
	:return: 