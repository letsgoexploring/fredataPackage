from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import os,subprocess
from fredclass import fred
# import time
from datetime import date
# import scikits.statsmodels.api as sm
# tsa = sm.tsa

today = date.today()
today_string = today.strftime("%B %d, %Y")
years10    = dts.YearLocator(10)
def func(x, pos):  # formatter function takes tick label and tick position
   s = '{:0,d}'.format(int(x))
   return s

y_format = plt.FuncFormatter(func)  # make formatter



# Assets

# Loans
total_loans_leases= fred('LOANS')
ci_loans          = fred('BUSLOANS')
re_loans          = fred('REALLN')
consumer_loans    = fred('CONSUMER')
other_loans_leases= fred('OLLACBM027SBOG')

# Securities
total_securities  = fred('INVEST')
treas_agency      = fred('USGSEC')
other_securities  = fred('OTHSEC')

# Additioanl Assets
loan_loss_allow   = fred('ALLACBM027NBOG')
interbank_loans   = fred('IBLACBM027SBOG')
cash_assets       = fred('CASACBM027SBOG')
trading_assets    = fred('TDAACBM027SBOG')
other_assets      = fred('OATACBM027SBOG')

total_assets      = fred('TLAACBM027SBOG')


# Liabilities

# Deposits
total_deposits    = fred('DPSACBM027SBOG')
large_time        = fred('LTDACBM027SBOG')
other_deposits    = fred('ODSACBM027SBOG')

#Additional Liabilities
borrowings        = fred('BOWACBM027SBOG')
trading_liabs     = fred('TLSACBM027SBOG')
net_due_foreign   = fred('NDFACBM027SBOG')
other_liabs       = fred('OLSACBM027SBOG')

total_liabilities = fred('TLBACBM027SBOG')

# Capital
residual          = fred('RALACBM027SBOG')




# Create values for entery in LaTeX tables

assets_loans = '{0:,}'.format(round(total_loans_leases.data[-1],1))
assets_secs  = '{0:,}'.format(round(total_securities.data[-1],1))
assets_loss  = '{0:,}'.format(round(-loan_loss_allow.data[-1],1))
assets_ib    = '{0:,}'.format(round(interbank_loans.data[-1],1))
assets_cash  = '{0:,}'.format(round(cash_assets.data[-1],1))
assets_other = '{0:,}'.format(round(other_assets.data[-1]+trading_assets.data[-1],1))
assets_total = '{0:,}'.format(round(total_assets.data[-1],1))

assets_loans_share= round(100*total_loans_leases.data[-1]/total_assets.data[-1],1)
assets_secs_share = round(100*total_securities.data[-1]/total_assets.data[-1],1)
assets_loss_share = round(-100*loan_loss_allow.data[-1]/total_assets.data[-1],1)
assets_ib_share   = round(100*interbank_loans.data[-1]/total_assets.data[-1],1)
assets_cash_share = round(100*cash_assets.data[-1]/total_assets.data[-1],1)
assets_other_share= round(100*(other_assets.data[-1]+trading_assets.data[-1])/total_assets.data[-1],1)



loans_ci    = '{0:,}'.format(round(ci_loans.data[-1],1))
loans_re    = '{0:,}'.format(round(re_loans.data[-1],1)) 
loans_con   = '{0:,}'.format(round(consumer_loans.data[-1],1))
loans_other = '{0:,}'.format(round(other_loans_leases.data[-1],1))
loans_total = '{0:,}'.format(round(total_loans_leases.data[-1],1))

loans_ci_share    = round(100*ci_loans.data[-1]/total_loans_leases.data[-1],1)
loans_re_share    = round(100*re_loans.data[-1]/total_loans_leases.data[-1],1)
loans_con_share   = round(100*consumer_loans.data[-1]/total_loans_leases.data[-1],1)
loans_other_share = round(100*other_loans_leases.data[-1]/total_loans_leases.data[-1],1)

liabilities_dep    = '{0:,}'.format(round(total_deposits.data[-1],1))
liabilities_bor    = '{0:,}'.format(round(borrowings.data[-1],1))
liabilities_other  = '{0:,}'.format(round(other_liabs.data[-1],1))
liabilities_total  = '{0:,}'.format(round(total_liabilities.data[-1],1))
liabilities_cap    = '{0:,}'.format(round(residual.data[-1],1))

liabilities_dep_share   = round(100*total_deposits.data[-1]/total_liabilities.data[-1],1)
liabilities_bor_share   = round(100*borrowings.data[-1]/total_liabilities.data[-1],1)
liabilities_other_share = round(100*other_liabs.data[-1]/total_liabilities.data[-1],1)
# liabilities_total_share = round(100*total_deposits.data[-1]/total_liabilities.data[-1],1)
# liabilities_cap_share   = round(100*total_deposits.data[-1]/total_liabilities.data[-1],1)


# Form tables for LaTeX

# Banking System Balance Sheet
nf = open('table_slides_012_bank_system_balance_sheet.tex', 'w')

nf.write('\\fr{\n')
nf.write('\\ft{Assets and liabilities of Commercial Banks in the US as of '),nf.write(today_string),nf.write('}\n')
nf.write('\\begin{center}\\begin{tabular}{|lp{3cm}c|} \\hline && \\\\ && \\textbf{Billions of \\$} \\\\\\hline &&\\\\\n')
nf.write('\\textbf{Assets} &&'),     nf.write(assets_total),     nf.write('\\\\&&\\\\\n')
nf.write('\\textbf{Liabilities} &&'),nf.write(liabilities_total),nf.write('\\\\&&\\\\\\hline && \\\\\n')
nf.write('\\textbf{Capital} &&'),nf.write(liabilities_cap),nf.write('\\\\&&\\\\\hline\n')
nf.write('\\end{tabular}\\end{center}\n')
nf.write('\n\\\n\n')
nf.write('Source: Data for this table and for subsequent tables and figures obtained from the Federal Reserve Economic Database (FRED) at \\href{http://research.stlouisfed.org/fred2/}{http://research.stlouisfed.org/fred2/}.\n')
nf.write('}')

nf.close()


# Banking System Assets
nf = open('table_slides_012_bank_system_assets.tex', 'w')

nf.write('\\fr{\n')
nf.write('\\ft{Assets of Commercial Banks in the US as of '),nf.write(today_string),nf.write('}\n')
nf.write('\\begin{tabular}{p{5cm}cc} \\hline & \\textbf{Billions of \\$} & \\textbf{Percent of Total}\\\\\\hline\\\\\n')
nf.write('\\textbf{Loans and Leases} & '),         nf.write(assets_loans),nf.write('& '),nf.write(str(assets_loans_share)+'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Securities} & '),               nf.write(assets_secs), nf.write('& '),nf.write(str(assets_secs_share) +'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Loan/Lease Loss Allowance} & '),nf.write(assets_loss), nf.write('& '),nf.write(str(assets_loss_share) +'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Interbank Loans} & '),          nf.write(assets_ib),   nf.write('& '),nf.write(str(assets_ib_share)   +'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Cash Assets} & '),              nf.write(assets_cash), nf.write('& '),nf.write(str(assets_cash_share) +'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Other Assets} & '),             nf.write(assets_other),nf.write('& '),nf.write(str(assets_other_share)+'\\%'),nf.write('\\\\\\\\\\hline\n')
nf.write('\\textbf{Total Assets} & '),             nf.write(assets_total),nf.write('& '),nf.write('100\\%'),                     nf.write('\\\\\\\\\n')
nf.write('\\end{tabular}\n')
nf.write('}')

nf.close()

# Banking System Loans
nf = open('table_slides_012_bank_system_loans.tex', 'w')

nf.write('\\fr{\n')
nf.write('\\ft{Loans and Leases of Banks in the US as of '),nf.write(today_string),nf.write('}\n')
nf.write('\\begin{tabular}{p{5cm}cc} \\hline & \\textbf{Billions of \\$} & \\textbf{Percent of Total}\\\\\\hline\\\\\n')
nf.write('\\textbf{Commerical/Industrial} & '),nf.write(loans_ci),   nf.write('& '),nf.write(str(loans_ci_share)   +'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Real Estate} & '),          nf.write(loans_re),   nf.write('& '),nf.write(str(loans_re_share)   +'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Consumer} & '),             nf.write(loans_con),  nf.write('& '),nf.write(str(loans_con_share)  +'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Other} & '),                nf.write(loans_other),nf.write('& '),nf.write(str(loans_other_share)+'\\%'),nf.write('\\\\\\\\\\hline\n')
nf.write('\\textbf{Total Loans / Leases} & '), nf.write(loans_total),nf.write('& '),nf.write('100\\%'),                    nf.write('\\\\\\\\\n')
nf.write('\\end{tabular}\n')
nf.write('}')

nf.close()

# Banking System Liabilities
nf = open('table_slides_012_bank_system_liabilities.tex', 'w')

nf.write('\\fr{\n')
nf.write('\\ft{Liabilities of Commercial Banks in the US as of '),nf.write(today_string),nf.write('}\n')
nf.write('\\begin{tabular}{p{5cm}cc} \\hline & \\textbf{Billions of \\$} & \\textbf{Percent of Total}\\\\\\hline\\\\\n')
nf.write('\\textbf{Total Deposits} & '),    nf.write(liabilities_dep),  nf.write('& '),nf.write(str(liabilities_dep_share)  +'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Borrowings} & '),        nf.write(liabilities_bor),  nf.write('& '),nf.write(str(liabilities_bor_share)  +'\\%'),nf.write('\\\\\\\\\n')
nf.write('\\textbf{Other Liabilities} & '), nf.write(liabilities_other),nf.write('& '),nf.write(str(liabilities_other_share)+'\\%'),nf.write('\\\\\\\\\\hline\n')
nf.write('\\textbf{Total Liabilities} & '), nf.write(liabilities_total),nf.write('& '),nf.write('100\\%'),                          nf.write('\\\\\\\\\n')
nf.write('\\end{tabular}\n')
nf.write('}')

nf.close()

'''Plot bank system assets'''

win = ['1975-01-01','2015-01-01']
total_assets.window(win)
total_loans_leases.window(win)
total_securities.window(win)
cash_assets.window(win)
other_assets.window(win)
interbank_loans.window(win)

# other_stack= [i + o for i,o in zip(interbank_loans.data,other_assets.data)]
# cash_stack = [c + o for c,o in zip(cash_assets.data,other_stack)]
# secs_stack = [s + c for s,c in zip(total_securities.data,cash_stack)]
# loans_stack= [l + s for l,s in zip(total_loans_leases.data,secs_stack)]
# zero       = [0     for i   in interbank_loans.data]

# other_stack= [i + o for i,o in zip(interbank_loans.data,other_assets.data)]
# cash_stack = [c + o for c,o in zip(cash_assets.data,other_stack)]
# secs_stack = [s + c for s,c in zip(total_securities.data,cash_stack)]



zero       = [0     for i   in interbank_loans.data]
loans_stack= [l     for l   in total_loans_leases.data]
secs_stack = [s + l for s,l in zip(total_securities.data,loans_stack)]
cash_stack = [c + s for c,s in zip(cash_assets.data,secs_stack)]
other_stack= [o + c for o,c in zip(other_assets.data,cash_stack)]
ib_stack   = [i + o for i,o in zip(interbank_loans.data,other_stack)]



# 3.2 plot Trade balance
fig, ax = plt.subplots()
# i = ax.fill_between(total_loans_leases.datenums,interbank_loans.data, zero,facecolor='yellow', alpha=0.25,label='other')
# o = ax.fill_between(total_loans_leases.datenums,other_stack,interbank_loans.data, facecolor='magenta', alpha=0.25,label='other')
# c = ax.fill_between(total_loans_leases.datenums, cash_stack,other_stack,facecolor='green', alpha=0.25,label='Cash')
# s = ax.fill_between(total_loans_leases.datenums, secs_stack, cash_stack,facecolor='red', alpha=0.25,label='Securities')
# l = ax.fill_between(total_loans_leases.datenums, loans_stack, secs_stack,facecolor='blue', alpha=0.25,label='Loans')

l = ax.fill_between(total_loans_leases.datenums, loans_stack, zero,facecolor='blue', alpha=0.25,label='Loans')
s = ax.fill_between(total_loans_leases.datenums, secs_stack, loans_stack,facecolor='red', alpha=0.25,label='Securities')
c = ax.fill_between(total_loans_leases.datenums, cash_stack,secs_stack,facecolor='green', alpha=0.25,label='Cash')
o = ax.fill_between(total_loans_leases.datenums, other_stack,cash_stack, facecolor='magenta', alpha=0.25,label='other')
i = ax.fill_between(total_loans_leases.datenums, ib_stack,other_stack, facecolor='yellow', alpha=0.25,label='other')



ax.plot_date(interbank_loans.datenums,ib_stack,'y-',lw = 3)
ax.plot_date(other_assets.datenums,other_stack,'m-',lw = 3)
ax.plot_date(cash_assets.datenums,cash_stack,'g-',lw = 3)
ax.plot_date(total_securities.datenums,secs_stack,'r-',lw = 3)
ax.plot_date(total_loans_leases.datenums,loans_stack,'b-',lw = 3)





ax.xaxis.set_major_locator(years10)
ax.yaxis.set_major_formatter(y_format)
ax.set_ylabel('Billions of $')
fig.autofmt_xdate()
ax.grid(True)

ax.legend(['Interbank Loans','Other','Cash','Securities','Loans'],loc='upper left')
plt.savefig('fig_012_bank_assets.png',bbox_inches='tight')

nf = open('fig_slides_012_bank_system_assets.tex', 'w')

nf.write('\\fr{\n')
nf.write('\\begin{figure}[h] \\caption{\label{fig2} \\textbf{Assets of Commercial banks in the US from January 1, 1975 through '),nf.write(today_string),nf.write('}}\n')
nf.write('\\hspace*{-.5cm}\\includegraphics[height = 7.cm]{fig_012_bank_assets.png}\n')
nf.write('\\end{figure}\n')
nf.write('}')

nf.close()


'''Plot bank system liabilities'''

win = ['1975-01-01','2015-01-01']
total_deposits.window(win)
borrowings.window(win)
trading_liabs.window(win)
net_due_foreign.window(win)
other_liabs.window(win)
total_liabilities.window(win)


borr_stack= [b + d for b,d in zip(borrowings.data,total_deposits.data)]
other_stack = [o + b for o,b in zip(other_liabs.data,borr_stack)]
zero      = [0     for d   in total_deposits.data]

# 3.2 plot Trade balance
fig, ax = plt.subplots()


d = ax.fill_between(total_deposits.datenums, total_deposits.data, zero,facecolor='blue', alpha=0.25,label='Loans')
b = ax.fill_between(total_deposits.datenums, borr_stack,total_deposits.data,facecolor='red', alpha=0.25,label='Loans')
o = ax.fill_between(total_deposits.datenums, other_stack,borr_stack,facecolor='green', alpha=0.25,label='Loans')

ax.plot_date(total_deposits.datenums,other_stack,'g-',lw = 3)
ax.plot_date(total_deposits.datenums,borr_stack,'r-',lw = 3)
ax.plot_date(total_deposits.datenums,total_deposits.data,'b-',lw = 3)

ax.xaxis.set_major_locator(years10)
ax.yaxis.set_major_formatter(y_format)
ax.set_ylabel('Billions of $')
fig.autofmt_xdate()
ax.grid(True)

ax.legend(['Other','Borrowings','Deposits'],loc='upper left')
plt.savefig('fig_012_bank_liabilities.png',bbox_inches='tight')

nf = open('fig_slides_012_bank_system_liabilities.tex', 'w')

nf.write('\\fr{\n')
nf.write('\\begin{figure}[h] \\caption{\label{fig2} \\textbf{Liabilities of Commercial banks in the US from January 1, 1975 through '),nf.write(today_string),nf.write('}}\n')
nf.write('\\hspace*{-.5cm}\\includegraphics[height = 7.cm]{fig_012_bank_liabilities.png}\n')
nf.write('\\end{figure}\n')
nf.write('}')

nf.close()

# plt.show()

def tex():

    FNULL = open(os.devnull, 'w')
    os.chdir(os.getcwd())

    for files in os.listdir('.'):
        if files.endswith('Slides_012_Bank_Assets_Liabilities.tex'):
            texfile = 'pdflatex '+files
            subprocess.call(texfile,shell=True,stdout=FNULL)
            subprocess.call(texfile,shell=True,stdout=FNULL)

    for files in os.listdir('.'):
        if files.endswith('.aux') or files.endswith('.log') or files.endswith('.out') or files.endswith('.gz') or files.endswith('.nav') or files.endswith('.snm') or files.endswith('.toc'):
            os.remove(files)

tex()