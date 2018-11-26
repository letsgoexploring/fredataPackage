import fredpy as fp
'''This program downloads and plots current unemployment data from FRED.

Created by: Brian C Jenkins. Email comments and suggestions to bcjenkin@uci.edu. Version date: November 26, 2018'''

fp.api_key = fp.load_api_key('fred_api_key.txt')

unemp = fp.series('UNRATE')

fp.quickplot(unemp,recess=True,save=True,style='classic',filename='fig_fredpy_example1')