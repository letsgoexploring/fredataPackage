
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

.. py:function:: fredpy.quickplot(fred_series,year_mult=10,show=True,recess=False,save=False,filename='file',linewidth=2,alpha = 0.75)

    Create a plot of a FRED data series.

    :param fred_series: A :py:class:`fredpy.series` object.
    :type fred_series: fredpy.series
    :param int year_mult: Interval between year ticks on the x-axis. Default: 10.
    :param bool show: Show the plot? Default: True.
    :param bool recess: Show recession bars in plot? Default: False.
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

.. py:function:: fredpy.toFredSeries(data,dates,title='',freq='',source='',units='',updated='')

            Create a :py:class:`fredpy.series` from time series data not obtained from FRED.

            :param data: Data values.
            :type data: numpy.ndarray, Pandas.Series, or list
            :param dates: Array or list of dates. Elements formatted as either string (YYYY-MM-DD or MM-DD-YYYY) or :py:class:`pandas.tslib.Timestamp`.
            :type dates: list or numpy.ndarry
            :param str title: Name of the series. Default: empty string.
            :param str freq: Options: empty string, `'Daily'`, `'Weekly'`, `'Monthly'`, `'Quarterly'`, or 'Annual'. Default: empty string
            :param str source: Source of the data. Default: empty string.
            :param str units: Units of the data. Default: empty string.
            :return: :py:class:`fredpy.series`

.. py:function:: fredpy.window_equalize(series_list)

	Adjusts the date windows for a collection of fredpy.series objects to the smallest common window.

	:param list series_list: A list of :py:class:`fredpy.series` objects
	:return: 