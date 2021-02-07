from iexfinance.stocks import Stock
import requests
import urllib.parse
import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import time

portfolio = {}
portfolio_det = {}

class iex:

    def get_df(ls, period, time, token):
        for ticker in ls:
            financials_url = f"https://sandbox.iexapis.com/stable/stock/{ticker}/financials?period={period}&last={time}&token={token}"
            financials_json = requests.get(financials_url).json()
            portfolio[ticker] = pd.DataFrame(financials_json['financials'])
            return portfolio


    def add_company(ls):
        for ticker in ls:
            company_url = f"https://sandbox.iexapis.com/stable/stock/{ticker}/company?token={token}"
            company_json = requests.get(company_url).json()
            portfolio_det[ticker] = pd.DataFrame(company_json)
            return portfolio_det

    def preprocess(dic):
        for v in dic.values():
            v.rename(str.lower, axis='columns', inplace=True)
            v['fiscaldate'] = pd.to_datetime(v['fiscaldate']).dt.strftime('%Y%m')
            v.set_index(v['fiscaldate'], inplace=True)
            v['fcf'] = v['cashflow'] + v['researchanddevelopment']
            return v

    def add_profitability(dic):
        for df in dic.values():
            df['operating_margin'] = df['operatingincome'] / df['revenue']
            df['net_margin'] = df['netincome'] / df['revenue']
            df['asset_turnover'] = df['revenue'] / df['totalassets']
            df['roa'] = df['netincome']*4/ df['totalassets']
            df['equity_multipl'] = df['totalassets'] / df['shareholderequity']
            df['roe'] = df['netincome'] / df['shareholderequity']
            df['fcf_margin'] = (df['cashflow'] + df['researchanddevelopment']) / df['revenue']
            return df

    def add_financial_strength(dic):
        for df in dic.values():
            df['cash_debt'] = df['totalcash'] / df['totaldebt']
            df['equity_asset'] = df['shareholderequity'] / df['totalassets']
            df['debt_equity'] = df['totaldebt'] / df['shareholderequity']
            df['debt_ebitda'] = df['totaldebt'] / (df['ebitda']*4)
            return df

    def graphs_financials(dic):
        for k, v in dic.items():
            fig, axes = plt.subplots(nrows=3, ncols=2)
            plt.subplots_adjust(hspace=0.3)
            fig.suptitle(f'Financials {k}', fontsize=16)
            axes[0,0].set_title('Revenue vs Net Income absolute')
            v[['revenue','netincome']].sort_index().plot(ax=axes[0,0], kind='bar',figsize=(20,20))
            axes[0,1].set_title('Revenue vs Net Income % change')
            v[['revenue','netincome']].sort_index().pct_change().plot(ax=axes[0,1],kind='line',figsize=(20,20))
            axes[1,0].set_title('Cashflow vs LT Debt absolute')
            v[['cashflow','currentlongtermdebt']].sort_index().plot(ax=axes[1,0], kind='bar',figsize=(20,20))
            axes[1,1].set_title('Cashflow vs LT Debt % change')
            v[['cashflow','currentlongtermdebt']].sort_index().pct_change().plot(ax=axes[1,1], kind='line',figsize=(20,20))
            axes[2,0].set_title('Operating Income vs Free Cash Flow absolute')
            v[['operatingincome','fcf']].sort_index().plot(ax=axes[2,0], kind='bar',figsize=(20,20))
            axes[2,1].set_title('Operating Income vs Free Cash Flow % change')
            v[['operatingincome','fcf']].sort_index().pct_change().plot(ax=axes[2,1], kind='line',figsize=(20,20))
            axes[0,0].grid(True,which="both", linestyle='--')
            axes[0,1].grid(True,which="both", linestyle='--')
            axes[1,0].grid(True,which="both", linestyle='--')
            axes[1,1].grid(True,which="both", linestyle='--')
            axes[2,0].grid(True,which="both", linestyle='--')
            axes[2,1].grid(True,which="both", linestyle='--')
            return plt.show()

    def graphs_profitability(dic):
        for k, v in dic.items():
            fig, axes = plt.subplots(nrows=3, ncols=2)
            plt.subplots_adjust(hspace=0.3)
            fig.suptitle(f'Profitability {k}', fontsize=16)
            axes[0,0].set_title('Free cashflow vs asset turnover absolute')
            v[['fcf_margin','asset_turnover']].sort_index().plot(ax=axes[0,0], kind='bar',figsize=(20,20))
            axes[0,1].set_title('Free cashflow vs asset turnover %change')
            v[['fcf_margin','asset_turnover']].sort_index().pct_change().plot(ax=axes[0,1],kind='line',figsize=(20,20))
            axes[1,0].set_title('Operating margin vs net margin absolute')
            v[['operating_margin','net_margin']].sort_index().plot(ax=axes[1,0], kind='bar',figsize=(20,20))
            axes[1,1].set_title('Operating margin vs net margin % change')
            v[['operating_margin','net_margin']].sort_index().pct_change().plot(ax=axes[1,1], kind='line',figsize=(20,20))
            axes[2,0].set_title('Return on equity vs return on assets absolute')
            v[['roe','roa']].sort_index().plot(ax=axes[2,0], kind='bar',figsize=(20,20))
            axes[2,1].set_title('Return on equity vs return on assets % change')
            v[['roe','roa']].sort_index().pct_change().plot(ax=axes[2,1], kind='line',figsize=(20,20))
            axes[0,0].grid(True,which="both", linestyle='--')
            axes[0,1].grid(True,which="both", linestyle='--')
            axes[1,1].grid(True,which="both", linestyle='--')
            axes[1,1].grid(True,which="both", linestyle='--')
            axes[2,0].grid(True,which="both", linestyle='--')
            axes[2,1].grid(True,which="both", linestyle='--')
            return plt.show()

    def graphs_security(dic):
        for k, v in dic.items():
            fig, axes = plt.subplots(nrows=4, ncols=2)
            plt.subplots_adjust(hspace=0.4)
            fig.suptitle(f'Financial Strength {k}', fontsize=16)
            axes[0,0].set_title('Cash to Debt absolute')
            v[['cash_debt']].sort_index().plot(ax=axes[0,0], kind='bar',figsize=(20,20))
            axes[0,1].set_title('Cash to Debt absolute %change')
            v[['cash_debt']].sort_index().pct_change().plot(ax=axes[0,1],kind='line',figsize=(20,20))
            axes[1,0].set_title('Equity to Assets absolute')
            v[['equity_asset']].sort_index().plot(ax=axes[1,0], kind='bar',figsize=(20,20))
            axes[1,1].set_title('Equity to Assets % change')
            v[['equity_asset']].sort_index().pct_change().plot(ax=axes[1,1], kind='line',figsize=(20,20))
            axes[2,0].set_title('Debt to Equity absolute')
            v[['debt_equity']].sort_index().plot(ax=axes[2,0], kind='bar',figsize=(20,20))
            axes[2,1].set_title('Debt to Equity absolute % change')
            v[['debt_equity']].sort_index().pct_change().plot(ax=axes[2,1], kind='line',figsize=(20,20))
            axes[3,0].set_title('Debt to EBITDA absolute')
            v[['debt_ebitda']].sort_index().plot(ax=axes[3,0], kind='bar',figsize=(20,20))
            axes[3,1].set_title('Debt to EBITDA % change')
            v[['debt_ebitda']].sort_index().pct_change().plot(ax=axes[3,1], kind='line',figsize=(20,20))
            axes[0,0].grid(True,which="both", linestyle='--')
            axes[0,1].grid(True,which="both", linestyle='--')
            axes[1,1].grid(True,which="both", linestyle='--')
            axes[1,1].grid(True,which="both", linestyle='--')
            axes[2,0].grid(True,which="both", linestyle='--')
            axes[2,1].grid(True,which="both", linestyle='--')
            axes[3,0].grid(True,which="both", linestyle='--')
            axes[3,1].grid(True,which="both", linestyle='--')
            return plt.show()
